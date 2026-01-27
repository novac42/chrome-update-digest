"""
Path resolution utilities for the Chrome Update Digest skill.

This module provides functions to locate the project root (for input/output)
and the skill root (for bundled config/prompts).
"""

import os
from pathlib import Path


def get_project_root() -> Path:
    """
    Detect project root for input/output paths.

    The project root is where upstream_docs/ and digest_markdown/ directories live.

    Resolution order:
    1. CHROME_UPDATE_DIGEST_BASE_PATH environment variable (explicit)
    2. Current working directory if it has marker files
    3. Parent directories if they have marker files
    4. Fallback to current working directory

    Returns:
        Path: Project root directory
    """
    # Option 1: Environment variable (explicit)
    env_path = os.getenv("CHROME_UPDATE_DIGEST_BASE_PATH")
    if env_path:
        path = Path(env_path)
        if path.exists():
            return path
        else:
            raise FileNotFoundError(
                f"CHROME_UPDATE_DIGEST_BASE_PATH is set to '{env_path}' but path does not exist"
            )

    # Option 2: Detect from CWD (if inside repo)
    cwd = Path.cwd()
    if _is_project_root(cwd):
        return cwd

    # Option 3: Go up from CWD to find repo root
    for parent in cwd.parents:
        if _is_project_root(parent):
            return parent

    # Fallback: Use CWD
    return cwd


def _is_project_root(path: Path) -> bool:
    """
    Check if a path is the project root by looking for marker files/directories.

    Args:
        path: Path to check

    Returns:
        bool: True if this looks like the project root
    """
    # Look for marker directories that should exist in project root
    markers = [
        "upstream_docs",
        "digest_markdown",
    ]

    return all((path / marker).exists() for marker in markers)


def get_skill_root() -> Path:
    """
    Get skill folder root for bundled config/prompts.

    The skill root is where config/, prompts/, and vendored/ folders live.
    This is typically .claude/skills/chrome-update-digest/

    Returns:
        Path: Skill root directory
    """
    # Skill code is in .claude/skills/chrome-update-digest/vendored/utils/
    # Go up two levels: utils/ -> vendored/ -> chrome-update-digest/
    return Path(__file__).parent.parent.parent


def get_config_path(filename: str) -> Path:
    """
    Get path to a bundled config file.

    Args:
        filename: Config filename (e.g., 'focus_areas.yaml')

    Returns:
        Path: Full path to config file
    """
    return get_skill_root() / "config" / filename


def get_prompt_path(filename: str) -> Path:
    """
    Get path to a bundled prompt template.

    Args:
        filename: Prompt filename (e.g., 'webplatform-prompt-en.md')

    Returns:
        Path: Full path to prompt file
    """
    return get_skill_root() / "prompts" / filename


# Convenience paths for common directories
def get_release_notes_dir() -> Path:
    """Get the directory containing raw release notes."""
    return get_project_root() / "upstream_docs" / "release_notes" / "WebPlatform"


def get_processed_areas_dir() -> Path:
    """Get the directory containing processed area files."""
    return (
        get_project_root()
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
    )


def get_digest_output_dir() -> Path:
    """Get the directory where digest markdown files should be written."""
    return get_project_root() / "digest_markdown" / "webplatform"


def get_navigation_output_dir() -> Path:
    """Get the directory where GitHub Pages navigation is written."""
    return get_project_root() / "digest_markdown"
