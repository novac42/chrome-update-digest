"""Orchestrator MCP tool for end-to-end GitHub Pages generation.

Runs the enhanced WebPlatform digest tool, refreshes the GitHub Pages
navigation, and validates the output in a single call.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import Context

from .enhanced_webplatform_digest import EnhancedWebplatformDigestTool


class GithubPagesOrchestratorTool:
    """Coordinate digest creation, navigation generation, and validation."""

    def __init__(self, base_path: Optional[Path] = None) -> None:
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.digest_tool = EnhancedWebplatformDigestTool(self.base_path)
        self.navigation_script = self.base_path / "src" / "tools" / "generate_github_pages_navigation.py"
        self.validation_script = self.base_path / "src" / "tools" / "validate_github_pages.py"
        self.digest_output_dir = self.base_path / "digest_markdown" / "webplatform"

    async def run(
        self,
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
        debug: bool = False
    ) -> str:
        """Execute the generation pipeline and return a JSON status report."""
        response: Dict[str, Any] = {
            "success": True,
            "version": version,
            "channel": channel,
            "steps": {}
        }

        languages = self._normalize_languages(language)
        digest_available = self._digest_outputs_present(version, channel, languages)
        existing_outputs = self._collect_existing_digest_paths(version, channel, languages)

        # Step 1: Generate per-area digests via the enhanced tool when needed
        if skip_digest:
            response["steps"]["digest"] = {
                "skipped": True,
                "reason": "skip_digest flag set",
                "available": digest_available,
                "outputs": existing_outputs
            }
            if not digest_available and not force_regenerate:
                response["steps"]["digest"]["warning"] = (
                    "No existing digests found for the requested version; navigation may be incomplete."
                )
        else:
            if force_regenerate or not digest_available:
                digest_result = await self._run_digest(
                    ctx,
                    version,
                    channel,
                    focus_areas,
                    language,
                    force_regenerate,
                    target_area,
                    debug
                )
                response["steps"]["digest"] = digest_result
                if not digest_result.get("success", False):
                    response["success"] = False
                    return json.dumps(response, ensure_ascii=False)

                # Refresh cache of generated paths after successful run
                existing_outputs = self._collect_existing_digest_paths(version, channel, languages)
                if existing_outputs:
                    response["steps"]["digest"]["outputs"] = existing_outputs
                digest_available = True
            else:
                response["steps"]["digest"] = {
                    "skipped": True,
                    "reason": "existing digests reused",
                    "available": True,
                    "outputs": existing_outputs
                }

        # Step 2: Refresh the GitHub Pages navigation content
        navigation_language = self._resolve_navigation_language(language)
        navigation_result = await self._run_navigation_generator(skip_clean, navigation_language, debug)
        response["steps"]["navigation"] = navigation_result
        if navigation_result["return_code"] != 0:
            response["success"] = False
            return json.dumps(response, ensure_ascii=False)

        # Step 3: Validate the generated site (optional)
        if not skip_validation:
            validation_result = await self._run_validation(debug)
            response["steps"]["validation"] = validation_result
            if validation_result["return_code"] != 0:
                response["success"] = False
        else:
            response["steps"]["validation"] = {
                "skipped": True
            }

        return json.dumps(response, ensure_ascii=False)

    async def _run_digest(
        self,
        ctx: Context,
        version: str,
        channel: str,
        focus_areas: Optional[str],
        language: str,
        force_regenerate: bool,
        target_area: Optional[str],
        debug: bool
    ) -> Dict[str, Any]:
        """Invoke the enhanced digest tool and normalise the response."""
        try:
            raw = await self.digest_tool.run(
                ctx,
                version=version,
                channel=channel,
                focus_areas=focus_areas,
                use_cache=not force_regenerate,
                language=language,
                split_by_area=True,
                target_area=target_area,
                debug=debug
            )
        except Exception as exc:  # pragma: no cover - defensive guard
            return {
                "success": False,
                "error": f"Digest generation failed: {exc}"
            }

        parsed = self._safe_json_load(raw)
        if not isinstance(parsed, dict):
            return {
                "success": False,
                "error": "Unexpected digest response format",
                "raw": raw
            }

        return parsed

    async def _run_navigation_generator(self, skip_clean: bool, language: str, debug: bool) -> Dict[str, Any]:
        """Run the navigation generator script."""
        if not self.navigation_script.exists():
            return {
                "return_code": 1,
                "stdout": "",
                "stderr": f"Navigation script not found: {self.navigation_script}"
            }

        args = [
            "python3",
            str(self.navigation_script),
            "--base-path",
            str(self.base_path),
            "--language",
            language
        ]
        if not skip_clean:
            args.append("--clean")

        return await self._run_subprocess(args, debug)

    async def _run_validation(self, debug: bool) -> Dict[str, Any]:
        """Run the structural validator and capture results."""
        if not self.validation_script.exists():
            return {
                "return_code": 1,
                "stdout": "",
                "stderr": f"Validation script not found: {self.validation_script}"
            }

        args = ["python3", str(self.validation_script), "--digest-dir", "digest_markdown"]
        result = await self._run_subprocess(args, debug)
        if result.get("stdout"):
            result["summary"] = self._extract_validation_summary(result["stdout"])
        return result

    async def _run_subprocess(self, args: List[str], debug: bool) -> Dict[str, Any]:
        """Helper to execute a subprocess and capture its output."""
        process = await asyncio.create_subprocess_exec(
            *args,
            cwd=str(self.base_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout_bytes, stderr_bytes = await process.communicate()
        stdout = stdout_bytes.decode("utf-8", errors="replace")
        stderr = stderr_bytes.decode("utf-8", errors="replace")

        if debug and stderr:
            print(f"Command {' '.join(args)} stderr:\n{stderr}")

        return {
            "args": args,
            "return_code": process.returncode,
            "stdout": stdout,
            "stderr": stderr
        }

    @staticmethod
    def _normalize_languages(language: Optional[str]) -> List[str]:
        """Map language parameter to the concrete digest variants to expect."""
        if not language:
            return ["en"]
        normalized = language.lower()
        if normalized == "bilingual":
            return ["en", "zh"]
        if normalized in {"en", "zh"}:
            return [normalized]
        return ["en"]

    def _digest_outputs_present(self, version: str, channel: str, languages: List[str]) -> bool:
        """Check whether digest files already exist for the requested version."""
        if not self.digest_output_dir.exists():
            return False

        for lang in languages:
            pattern = f"chrome-{version}-{channel}-{lang}.md"
            found = False
            for area_dir in self.digest_output_dir.iterdir():
                if not area_dir.is_dir():
                    continue
                if (area_dir / pattern).exists():
                    found = True
                    break
            if not found:
                return False

        return True

    def _collect_existing_digest_paths(
        self,
        version: str,
        channel: str,
        languages: List[str]
    ) -> Dict[str, Dict[str, str]]:
        """Return a mapping of area -> language -> path for available digests."""
        outputs: Dict[str, Dict[str, str]] = {}
        if not self.digest_output_dir.exists():
            return outputs

        for area_dir in self.digest_output_dir.iterdir():
            if not area_dir.is_dir():
                continue

            area_name = area_dir.name
            for lang in languages:
                candidate = area_dir / f"chrome-{version}-{channel}-{lang}.md"
                if candidate.exists():
                    outputs.setdefault(area_name, {})[lang] = str(candidate)

        return outputs

    @staticmethod
    def _resolve_navigation_language(language: Optional[str]) -> str:
        """Choose a single language variant for navigation scaffolding."""
        if not language:
            return "en"
        normalized = language.lower()
        if normalized == "bilingual":
            return "bilingual"
        if normalized in {"en", "zh"}:
            return normalized
        return "en"

    @staticmethod
    def _safe_json_load(payload: str) -> Any:
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _extract_validation_summary(stdout: str) -> Dict[str, Any]:
        """Summarise validation output (errors, warnings, coverage info)."""
        summary: Dict[str, Any] = {
            "errors": [],
            "warnings": []
        }

        for line in stdout.splitlines():
            stripped = line.strip()
            if stripped.startswith("❌") or ": Broken link" in stripped:
                summary.setdefault("errors", []).append(stripped)
            elif stripped.startswith("⚠"):
                summary.setdefault("warnings", []).append(stripped)
            elif stripped.startswith("- Versions found:"):
                summary["versions"] = stripped
            elif stripped.startswith("- Areas found:"):
                summary["areas"] = stripped

        if not summary["errors"]:
            summary.pop("errors", None)
        if not summary["warnings"]:
            summary.pop("warnings", None)

        return summary
