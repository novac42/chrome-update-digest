import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastmcp import Context


class AreaRunner:
    """Minimal per-area executor extracted from the tool.

    This is a skeleton to reduce closure capture in _generate_per_area_digests.
    It delegates actual generation/translation back to the tool instance to keep behavior identical.
    """

    def __init__(self, tool_ref: Any):
        self.tool = tool_ref

    async def process_one_area(
        self,
        ctx: Context,
        area: str,
        version: str,
        channel: str,
        languages: List[str],
        debug: bool,
    ) -> Dict[str, Any]:
        normalized_area = self.tool.focus_manager.normalize_area(area)
        import time

        # Load or slice area YAML using existing tool pathways
        area_yaml = await self.tool._load_area_yaml(ctx, version, channel, normalized_area, None, debug)
        if not area_yaml or len(area_yaml.get('features', [])) == 0:
            # Fallback minimal output (mirror telemetry semantics)
            fallback_reason = "empty_area"
            en_fallback = self.tool._generate_minimal_fallback(version, channel, area, 'en')
            fallback_start = time.perf_counter()
            en_path = self.tool._get_digest_path(version, channel, normalized_area, 'en')
            await self.tool._save_digest(en_fallback, en_path, debug)
            fallback_elapsed = time.perf_counter() - fallback_start
            self.tool.telemetry.observe_area_stage(
                area=normalized_area,
                stage="fallback_generation",
                language="en",
                duration_seconds=fallback_elapsed,
                status="success",
                extra={"reason": fallback_reason},
            )
            result = {"area": normalized_area, "paths": {"en": str(en_path)}, "status": "fallback"}
            if 'zh' in languages:
                zh_fallback = self.tool._generate_translation_fallback(version, channel, normalized_area, en_path)
                zh_path = self.tool._get_digest_path(version, channel, normalized_area, 'zh')
                zh_fallback_start = time.perf_counter()
                await self.tool._save_digest(zh_fallback, zh_path, debug)
                zh_fallback_elapsed = time.perf_counter() - zh_fallback_start
                self.tool.telemetry.observe_area_stage(
                    area=normalized_area,
                    stage="fallback_generation",
                    language="zh",
                    duration_seconds=zh_fallback_elapsed,
                    status="success",
                    extra={"reason": fallback_reason},
                )
                result["paths"]["zh"] = str(zh_path)
            return result

        # Generate English with timing and return paths; validation stays in tool
        english_stage_start = time.perf_counter()
        english_digest = await self.tool._generate_area_digest(ctx, area_yaml, 'en', normalized_area, debug)
        english_duration = time.perf_counter() - english_stage_start
        self.tool.telemetry.observe_area_stage(
            area=normalized_area,
            stage="english_generation",
            language="en",
            duration_seconds=english_duration,
            status="success",
            extra={"attempt": 1},
        )
        en_path = self.tool._get_digest_path(version, channel, normalized_area, 'en')
        await self.tool._save_digest(english_digest, en_path, debug)

        result_paths: Dict[str, str] = {"en": str(en_path)}

        if 'zh' in languages:
            translation_stage_start = time.perf_counter()
            chinese_digest = await self.tool._translate_digest(ctx, english_digest, normalized_area, version, channel, debug)
            translation_duration = time.perf_counter() - translation_stage_start
            self.tool.telemetry.observe_area_stage(
                area=normalized_area,
                stage="translation",
                language="zh",
                duration_seconds=translation_duration,
                status="success",
                extra={"attempt": 1},
            )
            zh_path = self.tool._get_digest_path(version, channel, normalized_area, 'zh')
            await self.tool._save_digest(chinese_digest, zh_path, debug)
            result_paths['zh'] = str(zh_path)

        return {"area": normalized_area, "paths": result_paths, "status": "success"}
