"""Utilities for locating WebPlatform release note files."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Union

VersionInput = Union[str, int]

_PROJECT_ROOT = Path(__file__).resolve().parents[3]  # Updated for new package structure
_WEBPLATFORM_ROOT = _PROJECT_ROOT / "upstream_docs" / "release_notes" / "WebPlatform"


def _normalize_version(version: VersionInput) -> str:
    """Return the version as a string without surrounding whitespace."""
    return str(version).strip()


def _iter_existing(paths: Iterable[Path]) -> Optional[Path]:
    for candidate in paths:
        if candidate.exists():
            return candidate
    return None


def _build_chrome_candidates(version: str, channel: str, base_dir: Path) -> list[Path]:
    channel = channel.lower()
    subdir = base_dir / "webplatform"

    names: list[str]
    if channel == "stable":
        names = [
            f"chrome-{version}.md",
            f"chrome-{version}-stable.md",
        ]
    else:
        names = [f"chrome-{version}-{channel}.md"]

    candidates: list[Path] = []

    # Prefer files stored directly under WebPlatform/ (new canonical layout)
    for name in names:
        candidates.append(base_dir / name)

    # Fall back to legacy layout where files were saved in a webplatform/ subdirectory
    for name in names:
        candidates.append(subdir / name)

    return candidates


def _build_webgpu_candidates(version: str, base_dir: Path) -> list[Path]:
    name = f"webgpu-{version}.md"
    return [
        (base_dir / name),
        (base_dir / "webplatform" / name),
    ]


def find_chrome_release_note(
    version: VersionInput,
    channel: str = "stable",
    base_dir: Optional[Union[str, Path]] = None,
) -> Optional[Path]:
    """Locate the Chrome release note file for the given version and channel."""
    resolved_base = Path(base_dir) if base_dir is not None else _WEBPLATFORM_ROOT
    normalized_version = _normalize_version(version)
    candidates = _build_chrome_candidates(normalized_version, channel, resolved_base)
    return _iter_existing(candidates)


def find_webgpu_release_note(
    version: VersionInput,
    base_dir: Optional[Union[str, Path]] = None,
) -> Optional[Path]:
    """Locate the WebGPU release note file for the given version."""
    resolved_base = Path(base_dir) if base_dir is not None else _WEBPLATFORM_ROOT
    normalized_version = _normalize_version(version)
    candidates = _build_webgpu_candidates(normalized_version, resolved_base)
    return _iter_existing(candidates)


__all__ = [
    "find_chrome_release_note",
    "find_webgpu_release_note",
]
