from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from chrome_update_digest.utils.telemetry import DigestTelemetry


class DigestIOManager:
    """Handles digest path resolution, file persistence, and progress tracking."""

    def __init__(
        self,
        base_path: Path,
        digest_dir: Path,
        telemetry: DigestTelemetry,
    ) -> None:
        self.base_path = base_path
        self.digest_dir = digest_dir
        self.telemetry = telemetry
        self._last_progress_write: float = 0.0
        self._last_progress_completed: int = -1

    def get_digest_path(self, version: str, channel: str, target_area: Optional[str], language: str) -> Path:
        channel = channel or 'stable'
        lang_suffix = {
            'en': 'en',
            'zh': 'zh',
            'bilingual': 'bilingual',
        }.get(language, 'en')

        if target_area:
            normalized_area = 'graphics-webgpu' if target_area in ['webgpu', 'graphics-webgpu'] else target_area
            area_dir = self.digest_dir / normalized_area
            area_dir.mkdir(parents=True, exist_ok=True)
            filename = f"chrome-{version}-{channel}-{lang_suffix}.md"
            return area_dir / filename

        filename = f"chrome-{version}-{channel}-{lang_suffix}.md"
        return self.digest_dir / filename

    async def save_digest(self, content: str, file_path: Path, debug: bool = False) -> None:
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            if debug:
                print(f"Successfully saved digest to: {file_path}")
        except Exception as exc:
            if debug:
                print(f"Error saving digest: {exc}")
            raise

    async def persist_output(
        self,
        *,
        version: str,
        channel: str,
        language: str,
        content: str,
        area: Optional[str],
        debug: bool = False,
    ) -> Path:
        file_path = self.get_digest_path(version, channel, area, language)
        await self.save_digest(content, file_path, debug)
        return file_path

    async def persist_area_language_output(
        self,
        *,
        version: str,
        channel: str,
        normalized_area: str,
        area_key: str,
        language: str,
        content: str,
        lock,
        progress_data: Dict[str, Any],
        results: Dict[str, Any],
        status: str,
        debug: bool,
        reason: Optional[str] = None,
    ) -> Path:
        file_path = await self.persist_output(
            version=version,
            channel=channel,
            language=language,
            content=content,
            area=normalized_area,
            debug=debug,
        )

        async with lock:
            outputs = results["outputs"].setdefault(normalized_area, {})
            outputs[language] = str(file_path)
            area_progress = progress_data["per_area"].setdefault(area_key, {"en": "pending", "zh": "pending"})
            area_progress[language] = status
            area_progress[f"{language}_path"] = str(file_path)
            progress_data["updated_at"] = datetime.now().isoformat()
            await self.update_progress(progress_data, debug)

        event_payload: Dict[str, Any] = {
            "area": normalized_area,
            "language": language,
            "status": status,
        }
        if reason:
            event_payload["reason"] = reason
        self.telemetry.log_event("area_language_persisted", event_payload)

        return file_path

    async def update_progress(self, progress_data: Dict[str, Any], debug: bool = False) -> None:
        try:
            import time

            now = time.perf_counter()
            completed = progress_data.get("completed_areas", 0)
            min_interval = float(os.getenv("WEBPLATFORM_PROGRESS_MIN_INTERVAL", "0.5"))

            if (
                not debug
                and self._last_progress_write > 0
                and completed == self._last_progress_completed
                and (now - self._last_progress_write) < min_interval
            ):
                return

            monitoring_dir = self.base_path / '.monitoring'
            monitoring_dir.mkdir(parents=True, exist_ok=True)

            progress_file = monitoring_dir / 'webplatform-progress.json'
            progress_data["updated_at"] = datetime.now().isoformat()
            progress_file.write_text(json.dumps(progress_data, indent=2, ensure_ascii=False), encoding='utf-8')

            self._last_progress_write = now
            self._last_progress_completed = completed

            if debug and progress_data.get("completed_areas", 0) > 0:
                total = progress_data.get("total_areas", 1)
                completed_count = progress_data.get("completed_areas", 0)
                percentage = (completed_count / total) * 100
                print(f"Progress: {completed_count}/{total} areas ({percentage:.0f}%)")
        except Exception as exc:
            if debug:
                print(f"Failed to update progress: {exc}")
