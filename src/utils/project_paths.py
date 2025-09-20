"""
Shared path utilities for Chrome Update Digest.
Provides consistent project root resolution and path helpers.
"""

from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """
    Get the absolute path to the project root directory.

    Returns the chrome-update-digest repository root by traversing up
    from this file's location.
    """
    # From src/utils/project_paths.py, go up 2 levels
    return Path(__file__).resolve().parent.parent.parent


PROJECT_ROOT = get_project_root()


def get_upstream_docs_path(base_path: Optional[Path] = None) -> Path:
    """
    Get the path to the upstream_docs directory.

    Args:
        base_path: Optional base directory. Defaults to PROJECT_ROOT.

    Returns:
        Path to upstream_docs directory.
    """
    if base_path is None:
        base_path = PROJECT_ROOT
    return base_path / "upstream_docs"


def get_config_path(base_path: Optional[Path] = None) -> Path:
    """
    Get the path to the config directory.

    Args:
        base_path: Optional base directory. Defaults to PROJECT_ROOT.

    Returns:
        Path to config directory.
    """
    if base_path is None:
        base_path = PROJECT_ROOT
    return base_path / "config"


def get_processed_release_notes_path(base_path: Optional[Path] = None) -> Path:
    """
    Get the path to processed release notes directory.

    Args:
        base_path: Optional base directory. Defaults to PROJECT_ROOT.

    Returns:
        Path to processed release notes within upstream_docs.
    """
    return get_upstream_docs_path(base_path) / "processed_releasenotes"


def get_webplatform_processed_path(base_path: Optional[Path] = None) -> Path:
    """
    Get the path to WebPlatform processed release notes.

    Args:
        base_path: Optional base directory. Defaults to PROJECT_ROOT.

    Returns:
        Path to WebPlatform processed release notes.
    """
    return get_processed_release_notes_path(base_path) / "processed_forwebplatform"


def get_areas_output_path(base_path: Optional[Path] = None) -> Path:
    """
    Get the path to area-specific output directory.

    Args:
        base_path: Optional base directory. Defaults to PROJECT_ROOT.

    Returns:
        Path to area-specific output directory.
    """
    return get_webplatform_processed_path(base_path) / "areas"