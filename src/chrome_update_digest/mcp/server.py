#!/usr/bin/env python3
"""
Chrome Digest FastMCP Server packaged for uv.

The module exposes a `create_app()` entry point that returns a fully configured
`FastMCP` instance and keeps backward compatible helpers (`BASE_PATH`,
`load_prompt_from_resource`, etc.) for existing tests and scripts.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from fastmcp import Context, FastMCP

from chrome_update_digest.mcp.resources.processed_releasenotes import (
    ProcessedReleaseNotesResource,
)
from chrome_update_digest.mcp.tools._digest_runtime import DigestRuntimeRegistry
from chrome_update_digest.mcp.tools.feature_splitter import FeatureSplitterTool
from chrome_update_digest.mcp.tools.github_pages_orchestrator import (
    GithubPagesOrchestratorTool,
)
from chrome_update_digest.mcp.tools.release_monitor import ReleaseMonitorTool

LOGGER = logging.getLogger(__name__)

DEFAULT_SERVER_NAME = "DigestServer"
_ENV_BASE_PATH = "CHROME_UPDATE_DIGEST_BASE_PATH"
_ENV_PRELOAD_RESOURCES = "DIGEST_PRELOAD_RELEASE_RESOURCES"

__all__ = [
    "BASE_PATH",
    "DigestServerApp",
    "create_app",
    "load_processed_data",
    "load_prompt_from_resource",
    "main",
    "mcp",
    "register_dynamic_resources",
    "save_digest_to_file",
]


def resolve_base_path(base_path: Optional[Path | str] = None) -> Path:
    """
    Resolve the workspace path that the MCP server should operate against.

    Priority:
    1. Explicit `base_path` argument (CLI/SDK usage).
    2. `CHROME_UPDATE_DIGEST_BASE_PATH` environment variable.
    3. Repository root when working from source (detected heuristically).
    4. Current working directory.
    """

    def _normalize(path_like: Path | str) -> Path:
        return Path(path_like).expanduser().resolve()

    def _looks_like_workspace(path: Path) -> bool:
        markers = ("prompts", "config", "upstream_docs")
        return any((path / marker).exists() for marker in markers)

    candidates: list[Path] = []

    if base_path:
        candidates.append(_normalize(base_path))
    else:
        env_path = os.getenv(_ENV_BASE_PATH)
        if env_path:
            candidates.append(_normalize(env_path))

    package_root = Path(__file__).resolve().parents[1]
    repo_root = package_root.parent

    candidates.extend([repo_root, package_root, Path.cwd().resolve()])

    for candidate in candidates:
        if _looks_like_workspace(candidate):
            return candidate

    # Fallback to the first existing candidate even if markers are missing.
    for candidate in candidates:
        if candidate.exists():
            return candidate

    return Path.cwd().resolve()


class DigestServerApp:
    """Encapsulates server state, resources, and tool registrations."""

    def __init__(self, base_path: Path, server_name: str = DEFAULT_SERVER_NAME) -> None:
        self.base_path = base_path
        self.server_name = server_name

        self.mcp = FastMCP(server_name)
        self.feature_splitter = FeatureSplitterTool(base_path)
        self.release_monitor_tool = ReleaseMonitorTool(base_path)
        self.github_pages_orchestrator = GithubPagesOrchestratorTool(base_path)
        self.release_notes_resource = ProcessedReleaseNotesResource(base_path)
        self.digest_registry = DigestRuntimeRegistry(base_path)

        self.preload_release_resources = (
            os.getenv(_ENV_PRELOAD_RESOURCES, "0").strip() == "1"
        )
        self.preloaded_release_resources = 0

        self._register_static_resources()
        self._register_tools()

        if self.preload_release_resources:
            self.preloaded_release_resources = self.register_dynamic_resources(True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _jsonify(payload: Dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2)

    async def _json_tool_call(self, coro: Any) -> str:
        try:
            result = await coro
        except Exception as exc:  # pragma: no cover - defensive path
            LOGGER.exception("Tool execution failed")
            return self._jsonify({"success": False, "error": str(exc)})
        return result if isinstance(result, str) else self._jsonify(result)

    # ------------------------------------------------------------------
    # Resource loaders exposed for tests/backwards compatibility
    # ------------------------------------------------------------------
    async def load_prompt_from_resource(self, resource_name: str) -> str:
        """Load prompt content from bundled prompts directory."""
        if resource_name == "webplatform-prompt":
            file_path = (
                self.base_path
                / "prompts"
                / "webplatform-prompts"
                / "webplatform-prompt-bilingual.md"
            )
        else:
            raise ValueError(f"Unknown resource: {resource_name}")

        if not file_path.exists():
            raise FileNotFoundError(f"Resource file not found: {file_path}")
        return file_path.read_text(encoding="utf-8")

    def load_processed_data(
        self, data_type: str, version: int, channel: str = "stable"
    ) -> str:
        """Load processed release notes from the workspace."""
        if data_type != "webplatform":
            raise ValueError(f"Unknown data type: {data_type}")

        data_path = (
            self.base_path
            / "upstream_docs"
            / "processed_releasenotes"
            / "processed_forwebplatform"
            / f"{version}-webplatform-with-webgpu.md"
        )
        if not data_path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")
        return data_path.read_text(encoding="utf-8")

    async def save_digest_to_file(self, content: str, output_path: Path) -> None:
        """Persist generated digest content to disk."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

    # ------------------------------------------------------------------
    # Resource and tool registration
    # ------------------------------------------------------------------
    def _register_static_resources(self) -> None:
        base_path = self.base_path

        @self.mcp.resource("file://webplatform-prompt", mime_type="text/markdown")
        def get_webplatform_prompt() -> str:
            prompt_path = (
                base_path
                / "prompts"
                / "webplatform-prompts"
                / "webplatform-prompt-bilingual.md"
            )
            if prompt_path.exists():
                return prompt_path.read_text(encoding="utf-8")
            return "WebPlatform prompt file not found"

    def register_dynamic_resources(self, include_release_notes: bool = False) -> int:
        """Register processed release notes as resources on demand."""
        if not include_release_notes:
            return 0

        resources = self.release_notes_resource.list_resources()
        registered = 0

        for resource in resources:
            uri = resource["uri"]

            def make_resource_getter(resource_uri: str, meta: Dict[str, Any]) -> None:
                @self.mcp.resource(
                    resource_uri,
                    name=resource["name"],
                    description=resource["description"],
                    mime_type=resource["mimeType"],
                )
                def get_resource() -> str:
                    return self.release_notes_resource.read_resource(resource_uri)

                if hasattr(get_resource, "_resource"):
                    get_resource._resource._meta = meta

            make_resource_getter(uri, resource.get("_meta", {}))
            registered += 1

        return registered

    def _register_tools(self) -> None:
        digest_registry = self.digest_registry
        feature_splitter = self.feature_splitter
        release_monitor_tool = self.release_monitor_tool
        github_pages_orchestrator = self.github_pages_orchestrator
        register_dynamic_resources = self.register_dynamic_resources

        @self.mcp.tool()
        async def get_webplatform_progress() -> str:
            return await self._json_tool_call(digest_registry.summarize_progress())

        @self.mcp.tool()
        async def webplatform_digest(
            ctx: Context,
            version: str = "138",
            channel: str = "stable",
            focus_areas: Optional[str] = None,
            use_cache: bool = True,
            language: str = "bilingual",
            split_by_area: bool = True,
            target_area: Optional[str] = None,
            debug: bool = False,
            model: Optional[str] = None,
            model_preferences: Optional[Any] = None,
        ) -> str:
            result = await digest_registry.run_full_digest(
                ctx,
                version=version,
                channel=channel,
                focus_areas=focus_areas,
                use_cache=use_cache,
                language=language,
                split_by_area=split_by_area,
                target_area=target_area,
                debug=debug,
                model=model,
                model_preferences=model_preferences,
            )
            if isinstance(result, str):
                return result
            return self._jsonify({"success": True, "payload": result})

        @self.mcp.tool("digest_prepare_yaml")
        async def digest_prepare_yaml(
            ctx: Context,
            version: str,
            channel: str = "stable",
            focus_areas: Optional[str] = None,
            use_cache: bool = True,
            language: Optional[str] = "bilingual",
            split_by_area: bool = True,
            target_area: Optional[str] = None,
            debug: bool = False,
            model: Optional[str] = None,
            model_preferences: Optional[Any] = None,
        ) -> str:
            return await self._json_tool_call(
                digest_registry.prepare_yaml(
                    ctx,
                    version=version,
                    channel=channel,
                    focus_areas=focus_areas,
                    use_cache=use_cache,
                    language=language,
                    split_by_area=split_by_area,
                    target_area=target_area,
                    debug=debug,
                    model=model,
                    model_preferences=model_preferences,
                )
            )

        @self.mcp.tool("digest_generate_area")
        async def digest_generate_area(
            ctx: Context,
            run_id: str,
            area: str,
            debug: Optional[bool] = None,
        ) -> str:
            return await self._json_tool_call(
                digest_registry.generate_area(
                    ctx,
                    run_id=run_id,
                    area=area,
                    debug=debug,
                )
            )

        @self.mcp.tool("digest_translate_area")
        async def digest_translate_area(
            ctx: Context,
            run_id: str,
            area: str,
            debug: Optional[bool] = None,
        ) -> str:
            return await self._json_tool_call(
                digest_registry.translate_area(
                    ctx,
                    run_id=run_id,
                    area=area,
                    debug=debug,
                )
            )

        @self.mcp.tool("digest_write_outputs")
        async def digest_write_outputs(ctx: Context, run_id: str) -> str:
            return await self._json_tool_call(
                digest_registry.write_outputs(run_id=run_id)
            )

        @self.mcp.tool("digest_inspect_cache")
        async def digest_inspect_cache(area: Optional[str] = None) -> str:
            return await self._json_tool_call(digest_registry.inspect_cache(area=area))

        @self.mcp.tool("digest_validate_links")
        async def digest_validate_links(
            ctx: Context, version: str, channel: str = "stable"
        ) -> str:
            return await self._json_tool_call(
                digest_registry.validate_links(ctx, version=version, channel=channel)
            )

        @self.mcp.tool("digest_summarize_progress")
        async def digest_summarize_progress() -> str:
            return await self._json_tool_call(digest_registry.summarize_progress())

        @self.mcp.tool("digest_list_outputs")
        async def digest_list_outputs(run_id: Optional[str] = None) -> str:
            return await self._json_tool_call(
                digest_registry.list_outputs(run_id=run_id)
            )

        @self.mcp.tool("digest_describe_run_config")
        async def digest_describe_run_config(run_id: str) -> str:
            return await self._json_tool_call(
                digest_registry.describe_run_config(run_id)
            )

        @self.mcp.tool("digest_reset_run_state")
        async def digest_reset_run_state(
            run_id: Optional[str] = None, reset_cache: bool = False
        ) -> str:
            return await self._json_tool_call(
                digest_registry.reset_run_state(
                    run_id=run_id,
                    reset_cache=reset_cache,
                )
            )

        @self.mcp.tool("digest_available_prompts")
        async def digest_available_prompts() -> str:
            return await self._json_tool_call(digest_registry.available_prompts())

        @self.mcp.tool("digest_register_release_resources")
        async def digest_register_release_resources(
            include_release_notes: bool = True,
        ) -> str:
            count = register_dynamic_resources(include_release_notes=include_release_notes)
            payload = {
                "success": True,
                "release_resources_registered": count,
                "lazy_mode": not include_release_notes,
            }
            return self._jsonify(payload)

        @self.mcp.tool("telemetry_report_metrics")
        async def telemetry_report_metrics() -> str:
            return await self._json_tool_call(digest_registry.report_metrics())

        @self.mcp.tool("progress_watch")
        async def progress_watch() -> str:
            return await self._json_tool_call(digest_registry.summarize_progress())

        @self.mcp.tool()
        async def split_features_by_heading(
            content: str, target_heading_level: int = 3
        ) -> str:
            return await feature_splitter.split_features(
                {"content": content, "target_heading_level": target_heading_level}
            )

        @self.mcp.tool()
        async def check_latest_releases(
            ctx: Context,
            release_type: str = "webplatform",
            channel: str = "stable",
        ) -> str:
            return await release_monitor_tool.check_latest_releases(
                ctx, {"release_type": release_type, "channel": channel}
            )

        @self.mcp.tool()
        async def generate_github_pages(
            ctx: Context,
            version: str,
            channel: str = "stable",
            focus_areas: Optional[str] = None,
            language: str = "bilingual",
            force_regenerate: bool = False,
            skip_clean: bool = False,
            skip_digest: bool = False,
            skip_validation: bool = False,
            target_area: Optional[str] = None,
            debug: bool = False,
        ) -> str:
            async def handler() -> Any:
                return await github_pages_orchestrator.run(
                    ctx,
                    version=version,
                    channel=channel,
                    focus_areas=focus_areas,
                    language=language,
                    force_regenerate=force_regenerate,
                    skip_clean=skip_clean,
                    skip_digest=skip_digest,
                    skip_validation=skip_validation,
                    target_area=target_area,
                    debug=debug,
                )

            result = await digest_registry.run_serialized(
                "generate_github_pages", handler
            )
            if isinstance(result, str):
                return result
            return self._jsonify(result)

        @self.mcp.tool()
        async def crawl_missing_releases(
            ctx: Context,
            release_type: str = "webplatform",
            channel: str = "stable",
            confirmed: bool = False,
            force_redownload: bool = False,
        ) -> str:
            return await release_monitor_tool.crawl_missing_releases(
                ctx,
                {
                    "release_type": release_type,
                    "channel": channel,
                    "confirmed": confirmed,
                    "force_redownload": force_redownload,
                },
            )


# ----------------------------------------------------------------------
# Factory helpers & CLI entry point
# ----------------------------------------------------------------------

def build_server(
    base_path: Optional[Path | str] = None,
    *,
    server_name: str = DEFAULT_SERVER_NAME,
) -> DigestServerApp:
    """Instantiate a new DigestServerApp with the provided base path."""
    resolved_base = resolve_base_path(base_path)
    return DigestServerApp(resolved_base, server_name=server_name)


def create_app(
    base_path: Optional[Path | str] = None,
    *,
    server_name: str = DEFAULT_SERVER_NAME,
) -> FastMCP:
    """Public factory that returns a configured FastMCP instance."""
    return build_server(base_path, server_name=server_name).mcp


def main(argv: Optional[Sequence[str]] = None) -> None:
    """CLI entry point for running the FastMCP server."""
    parser = argparse.ArgumentParser(description="Chrome Digest FastMCP server")
    parser.add_argument(
        "--base-path",
        type=Path,
        default=None,
        help="Workspace directory containing prompts, config, and processed data.",
    )
    parser.add_argument(
        "--server-name",
        default=DEFAULT_SERVER_NAME,
        help="Optional FastMCP server name override.",
    )
    args = parser.parse_args(argv)

    app = build_server(args.base_path, server_name=args.server_name)

    LOGGER.info("Starting FastMCP Digest Server (base_path=%s)", app.base_path)
    if app.preload_release_resources:
        LOGGER.info(
            "Preloaded %s release note resources.",
            app.preloaded_release_resources,
        )
    else:
        LOGGER.info("Release note resources registered lazily on demand.")

    app.mcp.run()


# ----------------------------------------------------------------------
# Backwards compatible exports for existing tests/imports
# ----------------------------------------------------------------------

_DEFAULT_APP = build_server()
mcp = _DEFAULT_APP.mcp
BASE_PATH = _DEFAULT_APP.base_path
load_prompt_from_resource = _DEFAULT_APP.load_prompt_from_resource
load_processed_data = _DEFAULT_APP.load_processed_data
save_digest_to_file = _DEFAULT_APP.save_digest_to_file
register_dynamic_resources = _DEFAULT_APP.register_dynamic_resources
