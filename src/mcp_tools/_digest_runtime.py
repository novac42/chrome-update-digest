from __future__ import annotations

import asyncio
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional

from fastmcp import Context

from src.mcp_tools._digest_area_runner import AreaRunner
from src.mcp_tools._digest_config import DigestRunConfig
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool
from src.utils.telemetry import DigestTelemetry


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class DigestRunState:
    """Book-keeping for an in-flight digest run driven by split MCP tools."""

    run_id: str
    config: DigestRunConfig
    focus_areas: List[str]
    use_cache: bool
    debug: bool
    split_by_area: bool
    target_area: Optional[str]
    yaml_data: Optional[Dict[str, Any]] = None
    areas: List[str] = field(default_factory=list)
    progress_data: Dict[str, Any] = field(default_factory=dict)
    results: Dict[str, Any] = field(default_factory=lambda: {"outputs": {}, "errors": {}, "translation_status": {}})
    created_at: datetime = field(default_factory=_utcnow)
    last_updated: datetime = field(default_factory=_utcnow)
    progress_lock: asyncio.Lock = field(default_factory=asyncio.Lock, repr=False)


class DigestRuntimeRegistry:
    """Central runtime hub that coordinates shared digest state across MCP tools."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.tool = EnhancedWebplatformDigestTool(base_path)
        self.area_runner = AreaRunner(self.tool)
        self.telemetry: DigestTelemetry = self.tool.telemetry
        self.yaml_cache = self.tool.yaml_cache
        self.io = self.tool.io
        self.focus_manager = self.tool.focus_manager
        self.digest_dir = self.tool.digest_dir

        self._runs: Dict[str, DigestRunState] = {}
        self._runtime_lock = asyncio.Lock()
        self._pending_requests: int = 0
        self._max_queue_depth: int = 0
        self._tool_metrics: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------ #
    # Public helpers exposed to MCP layer
    # ------------------------------------------------------------------ #
    async def prepare_yaml(
        self,
        ctx: Context,
        *,
        version: str,
        channel: str,
        focus_areas: Optional[str],
        use_cache: bool,
        language: Optional[str],
        split_by_area: bool,
        target_area: Optional[str],
        debug: bool,
        model: Optional[str],
        model_preferences: Optional[Any],
    ) -> Dict[str, Any]:
        """Pre-warm YAML cache, register a run state, and enumerate areas."""

        async def _operation() -> Dict[str, Any]:
            if not split_by_area:
                raise ValueError("digest.prepare_yaml currently requires split_by_area=True")

            focus_area_list = self._parse_focus_areas(focus_areas)
            run_config = DigestRunConfig(
                version=version,
                channel=channel,
                language=language,
                split_by_area=split_by_area,
                target_area=target_area,
                model_preferences=self.tool._resolve_model_preferences(  # pylint: disable=protected-access
                    explicit_preferences=model_preferences,
                    explicit_model=model,
                ),
                explicit_model=model,
            )

            run_state = DigestRunState(
                run_id=str(uuid.uuid4()),
                config=run_config,
                focus_areas=focus_area_list,
                use_cache=use_cache,
                debug=debug,
                split_by_area=split_by_area,
                target_area=target_area,
            )

            with self.tool.run_context(run_config):
                yaml_data = await self.yaml_cache.get_yaml_data(
                    ctx,
                    version,
                    channel,
                    use_cache,
                    split_by_area,
                    target_area,
                    debug,
                )

            if not yaml_data:
                raise FileNotFoundError(
                    f"Release notes for Chrome {version} {channel} channel not found."
                )

            if focus_area_list:
                yaml_data = self.tool.yaml_pipeline.filter_by_focus_areas(yaml_data, focus_area_list)

            run_state.yaml_data = yaml_data
            run_state.areas = self.tool._get_areas_from_yaml(yaml_data)  # pylint: disable=protected-access

            languages = run_config.resolved_languages()

            per_area_status: Dict[str, Dict[str, str]] = {}
            for area in run_state.areas:
                entry: Dict[str, str] = {"en": "pending", "zh": "pending"}
                if "en" not in languages:
                    entry["en"] = "skipped"
                if "zh" not in languages:
                    entry["zh"] = "skipped"
                per_area_status[area] = entry

            run_state.progress_data = {
                "run_id": run_state.run_id,
                "mode": "per_area",
                "version": version,
                "channel": channel,
                "languages": languages,
                "focus_areas": focus_area_list,
                "areas": run_state.areas,
                "total_areas": len(run_state.areas),
                "completed_areas": 0,
                "per_area": per_area_status,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }

            await self.io.update_progress(run_state.progress_data, debug)

            self._runs[run_state.run_id] = run_state
            run_state.last_updated = _utcnow()

            cache_stats = {
                "memory_hits": self.yaml_cache.cache_hits,
                "memory_misses": self.yaml_cache.cache_misses,
            }

            return {
                "success": True,
                "run_id": run_state.run_id,
                "version": version,
                "channel": channel,
                "languages": languages,
                "area_count": len(run_state.areas),
                "areas": run_state.areas,
                "focus_areas": focus_area_list,
                "cache_stats": cache_stats,
            }

        return await self._execute("digest.prepare_yaml", _operation)

    async def run_full_digest(self, ctx: Context, **kwargs: Any) -> Any:
        """Execute the legacy monolithic digest tool under shared coordination."""

        async def _operation() -> Any:
            return await self.tool.run(ctx=ctx, **kwargs)

        return await self._execute("webplatform_digest", _operation)

    async def generate_area(
        self,
        ctx: Context,
        *,
        run_id: str,
        area: str,
        debug: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Generate English digest for a single area."""

        async def _operation() -> Dict[str, Any]:
            run_state = self._require_run(run_id)
            languages = run_state.config.resolved_languages()

            if "en" not in languages:
                raise ValueError("Run was not configured to produce English content")

            normalized_area = self.focus_manager.normalize_area(area)
            debug_mode = run_state.debug if debug is None else debug

            await self._mark_language_status(run_state, normalized_area, "en", "in_progress")

            with self.tool.run_context(run_state.config):
                area_result = await self.area_runner.process_one_area(
                    ctx,
                    normalized_area,
                    run_state.config.version,
                    run_state.config.channel,
                    ["en"],
                    debug_mode,
                    full_yaml=run_state.yaml_data,
                )

            en_path = area_result.get("paths", {}).get("en")
            status = area_result.get("status", "success")

            await self._finalize_language_status(
                run_state,
                normalized_area,
                "en",
                status if status in {"success", "fallback"} else "error",
                en_path,
            )

            return {
                "success": status in {"success", "fallback"},
                "run_id": run_id,
                "area": normalized_area,
                "status": status,
                "english_path": en_path,
            }

        return await self._execute("digest.generate_area", _operation)

    async def translate_area(
        self,
        ctx: Context,
        *,
        run_id: str,
        area: str,
        debug: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Translate previously generated English digest to Chinese."""

        async def _operation() -> Dict[str, Any]:
            import os

            run_state = self._require_run(run_id)
            languages = run_state.config.resolved_languages()

            if "zh" not in languages:
                raise ValueError("Run was not configured to produce Chinese content")

            normalized_area = self.focus_manager.normalize_area(area)
            debug_mode = run_state.debug if debug is None else debug

            english_path = run_state.results.get("outputs", {}).get(normalized_area, {}).get("en")
            if not english_path or not Path(english_path).exists():
                # Attempt to infer path using IO manager
                inferred = self.io.get_digest_path(
                    run_state.config.version,
                    run_state.config.channel,
                    normalized_area,
                    "en",
                )
                if inferred.exists():
                    english_path = str(inferred)
                else:
                    raise FileNotFoundError(
                        f"English digest not found for area '{normalized_area}'. Generate it before translation."
                    )

            await self._mark_language_status(run_state, normalized_area, "zh", "in_progress")

            with open(english_path, "r", encoding="utf-8") as handle:
                english_digest = handle.read()

            with self.tool.run_context(run_state.config):
                translation_start = time.perf_counter()
                chinese_digest = await self.tool.generation.translate_digest(
                    ctx,
                    english_digest,
                    normalized_area,
                    run_state.config.version,
                    run_state.config.channel,
                    debug_mode,
                )
                translation_duration = time.perf_counter() - translation_start

            zh_path = await self.io.persist_output(
                version=run_state.config.version,
                channel=run_state.config.channel,
                language="zh",
                content=chinese_digest,
                area=normalized_area,
                debug=debug_mode,
            )

            self.telemetry.observe_area_stage(
                area=normalized_area,
                stage="translation",
                language="zh",
                duration_seconds=translation_duration,
                status="success",
                extra={"attempt": 1},
            )

            await self._finalize_language_status(run_state, normalized_area, "zh", "success", str(zh_path))

            return {
                "success": True,
                "run_id": run_id,
                "area": normalized_area,
                "status": "success",
                "chinese_path": str(zh_path),
            }

        return await self._execute("digest.translate_area", _operation)

    async def write_outputs(
        self,
        *,
        run_id: str,
    ) -> Dict[str, Any]:
        """Finalize a run by flushing progress and returning output manifest."""

        async def _operation() -> Dict[str, Any]:
            run_state = self._require_run(run_id)
            all_done = self._all_areas_complete(run_state)

            if all_done:
                async with run_state.progress_lock:
                    run_state.progress_data["completed_at"] = datetime.now(timezone.utc).isoformat()
                    run_state.progress_data["total_time_seconds"] = max(
                        0.0, (run_state.last_updated - run_state.created_at).total_seconds()
                    )
                    await self.io.update_progress(run_state.progress_data, run_state.debug)

            manifest = run_state.results.get("outputs", {})
            return {
                "success": all_done,
                "run_id": run_id,
                "completed": all_done,
                "outputs": manifest,
                "areas_pending": self._areas_pending(run_state),
            }

        return await self._execute("digest.write_outputs", _operation)

    async def inspect_cache(
        self,
        *,
        area: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Inspect YAML cache statistics and optionally dump a cached area."""

        async def _operation() -> Dict[str, Any]:
            normalized = self.focus_manager.normalize_area(area) if area else None
            memory_cache = self.yaml_cache._memory_cache  # pylint: disable=protected-access
            cache_payload: Dict[str, Any] = {
                "memory_hits": self.yaml_cache.cache_hits,
                "memory_misses": self.yaml_cache.cache_misses,
                "entries": [],
            }
            for key, value in memory_cache.items():
                entry: Dict[str, Any] = {"key": key}
                if isinstance(value, dict):
                    entry["feature_count"] = len(value.get("features", []))
                cache_payload["entries"].append(entry)

            if normalized:
                matches = [
                    entry for entry in cache_payload["entries"] if normalized in str(entry["key"])
                ]
                cache_payload["filtered"] = matches
            return {"success": True, "cache": cache_payload}

        return await self._execute("digest.inspect_cache", _operation)

    async def validate_links(
        self,
        ctx: Context,
        *,
        version: str,
        channel: str,
    ) -> Dict[str, Any]:
        """Expose EnhancedWebplatformDigestTool.validate_links via registry."""

        async def _operation() -> Dict[str, Any]:
            report = await self.tool.validate_links(ctx, version, channel)
            return {"success": True, "report": report}

        return await self._execute("digest.validate_links", _operation)

    async def summarize_progress(self) -> Dict[str, Any]:
        """Return the latest progress snapshot from monitoring directory."""

        async def _operation() -> Dict[str, Any]:
            progress_file = self.base_path / ".monitoring" / "webplatform-progress.json"
            if not progress_file.exists():
                return {"success": False, "error": "Progress file not found"}
            try:
                payload = json.loads(progress_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                return {"success": False, "error": f"Unable to parse progress file: {exc}"}
            return {"success": True, "progress": payload}

        return await self._execute("digest.summarize_progress", _operation)

    async def list_outputs(
        self,
        *,
        run_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List digest outputs on disk, optionally scoped to a run."""

        async def _operation() -> Dict[str, Any]:
            if not self.digest_dir.exists():
                return {"success": True, "outputs": []}

            items: List[Dict[str, Any]] = []
            for path in sorted(self.digest_dir.rglob("*.md")):
                item = {
                    "path": str(path),
                    "size_bytes": path.stat().st_size,
                    "updated_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                }
                items.append(item)

            if run_id and run_id in self._runs:
                run_state = self._runs[run_id]
                tracked = set()
                for area_outputs in run_state.results.get("outputs", {}).values():
                    tracked.update(area_outputs.values())
                for item in items:
                    item["tracked_in_run"] = item["path"] in tracked
            return {"success": True, "outputs": items}

        return await self._execute("digest.list_outputs", _operation)

    async def describe_run_config(self, run_id: str) -> Dict[str, Any]:
        """Describe configuration for a registered run."""

        async def _operation() -> Dict[str, Any]:
            run_state = self._require_run(run_id)
            cfg = run_state.config
            return {
                "success": True,
                "run_id": run_id,
                "config": {
                    "version": cfg.version,
                    "channel": cfg.channel,
                    "language": cfg.language_mode(),
                    "target_area": cfg.target_area,
                    "focus_areas": run_state.focus_areas,
                    "split_by_area": cfg.split_by_area,
                },
                "created_at": run_state.created_at.isoformat(),
                "last_updated": run_state.last_updated.isoformat(),
                "areas": run_state.areas,
            }

        return await self._execute("digest.describe_run_config", _operation)

    async def reset_run_state(
        self,
        run_id: Optional[str] = None,
        reset_cache: bool = False,
    ) -> Dict[str, Any]:
        """Reset run state and optionally clear in-memory YAML cache."""

        async def _operation() -> Dict[str, Any]:
            cleared: List[str] = []
            if run_id:
                if run_id in self._runs:
                    cleared.append(run_id)
                    del self._runs[run_id]
            else:
                cleared = list(self._runs.keys())
                self._runs.clear()

            if reset_cache:
                self.yaml_cache._memory_cache.clear()  # pylint: disable=protected-access

            return {"success": True, "cleared_runs": cleared, "cache_cleared": reset_cache}

        return await self._execute("digest.reset_run_state", _operation)

    async def available_prompts(self) -> Dict[str, Any]:
        """List available prompt templates for diagnostics."""

        async def _operation() -> Dict[str, Any]:
            prompt_dir = self.base_path / "prompts" / "webplatform-prompts"
            if not prompt_dir.exists():
                return {"success": False, "error": "Prompt directory not found"}
            prompts = []
            for path in sorted(prompt_dir.glob("*.md")):
                prompts.append(
                    {
                        "name": path.stem,
                        "path": str(path),
                        "size_bytes": path.stat().st_size,
                        "updated_at": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                    }
                )
            return {"success": True, "prompts": prompts}

        return await self._execute("digest.available_prompts", _operation)

    async def report_metrics(self) -> Dict[str, Any]:
        """Return per-tool runtime metrics tracked by the registry."""

        async def _operation() -> Dict[str, Any]:
            summary = {}
            for tool_name, metrics in self._tool_metrics.items():
                count = metrics.get("count", 0)
                total_duration = metrics.get("total_duration", 0.0)
                avg_duration = total_duration / count if count else 0.0
                summary[tool_name] = {
                    "count": count,
                    "avg_duration_seconds": round(avg_duration, 4),
                    "last_status": metrics.get("last_status"),
                    "last_duration_seconds": round(metrics.get("last_duration", 0.0), 4),
                    "last_wait_seconds": round(metrics.get("last_wait", 0.0), 4),
                    "max_queue_depth": metrics.get("max_queue_depth", 0),
                }
            return {"success": True, "tool_metrics": summary}

        return await self._execute("telemetry.report_metrics", _operation)

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    async def run_serialized(self, tool_name: str, handler: Callable[[], Awaitable[Any]]) -> Any:
        """Expose serialized execution for external callers."""
        return await self._execute(tool_name, handler)

    async def _execute(self, tool_name: str, operation: Callable[[], Any]) -> Any:
        request_start = time.perf_counter()
        self._pending_requests += 1
        try:
            current_queue_depth = max(0, self._pending_requests - 1)
            self._max_queue_depth = max(self._max_queue_depth, current_queue_depth)
            await self._runtime_lock.acquire()
        finally:
            self._pending_requests -= 1

        wait_time = time.perf_counter() - request_start
        start_time = time.perf_counter()
        status = "success"
        queue_depth = max(0, current_queue_depth)

        try:
            result = await operation()
            return result
        except Exception:
            status = "error"
            raise
        finally:
            duration = time.perf_counter() - start_time
            self._runtime_lock.release()
            self._record_tool_metrics(tool_name, status, duration, wait_time, queue_depth)

    def _record_tool_metrics(
        self,
        tool_name: str,
        status: str,
        duration_seconds: float,
        wait_seconds: float,
        queue_depth: int,
    ) -> None:
        metrics = self._tool_metrics.setdefault(
            tool_name,
            {"count": 0, "total_duration": 0.0, "max_queue_depth": 0},
        )
        metrics["count"] += 1
        metrics["total_duration"] += duration_seconds
        metrics["last_status"] = status
        metrics["last_duration"] = duration_seconds
        metrics["last_wait"] = wait_seconds
        metrics["max_queue_depth"] = max(metrics.get("max_queue_depth", 0), queue_depth)

        self.telemetry.log_tool_operation(
            tool_name=tool_name,
            status=status,
            duration_seconds=duration_seconds,
            wait_seconds=wait_seconds,
            queue_depth=queue_depth,
        )

    def _parse_focus_areas(self, focus_areas: Optional[str]) -> List[str]:
        if not focus_areas:
            return []
        parts = [part.strip() for part in focus_areas.split(",")]
        return [part for part in parts if part]

    def _require_run(self, run_id: str) -> DigestRunState:
        if run_id not in self._runs:
            raise KeyError(f"Run '{run_id}' not found. Prepare YAML before continuing.")
        return self._runs[run_id]

    async def _mark_language_status(
        self,
        run_state: DigestRunState,
        area: str,
        language: str,
        status: str,
    ) -> None:
        async with run_state.progress_lock:
            entry = run_state.progress_data["per_area"].setdefault(area, {"en": "pending", "zh": "pending"})
            entry[language] = status
            await self.io.update_progress(run_state.progress_data, run_state.debug)

    async def _finalize_language_status(
        self,
        run_state: DigestRunState,
        area: str,
        language: str,
        status: str,
        path: Optional[str],
    ) -> None:
        async with run_state.progress_lock:
            per_area = run_state.progress_data["per_area"].setdefault(area, {"en": "pending", "zh": "pending"})
            per_area[language] = status
            if path:
                per_area[f"{language}_path"] = path
                run_state.results.setdefault("outputs", {}).setdefault(area, {})[language] = path

            run_state.progress_data["completed_areas"] = self._count_completed_areas(run_state)
            run_state.progress_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            run_state.last_updated = _utcnow()

            await self.io.update_progress(run_state.progress_data, run_state.debug)

    def _count_completed_areas(self, run_state: DigestRunState) -> int:
        completion_states = {"success", "fallback", "skipped"}
        required_languages = run_state.config.resolved_languages()
        count = 0
        for per_area in run_state.progress_data.get("per_area", {}).values():
            done = True
            for lang in required_languages:
                if per_area.get(lang) not in completion_states:
                    done = False
                    break
            if done:
                count += 1
        return count

    def _all_areas_complete(self, run_state: DigestRunState) -> bool:
        total = run_state.progress_data.get("total_areas", 0)
        completed = self._count_completed_areas(run_state)
        return completed >= total and total > 0

    def _areas_pending(self, run_state: DigestRunState) -> List[str]:
        completion_states = {"success", "fallback", "skipped"}
        pending: List[str] = []
        required_languages = run_state.config.resolved_languages()
        for area, per_area in run_state.progress_data.get("per_area", {}).items():
            if any(per_area.get(lang) not in completion_states for lang in required_languages):
                pending.append(area)
        return pending
