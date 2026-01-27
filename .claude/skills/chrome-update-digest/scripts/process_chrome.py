#!/usr/bin/env python3
"""
Chrome Update Digest Processing Script for Claude Code Skill

This script orchestrates the Chrome release notes processing workflow,
calling the processing pipeline directly for better performance.
"""

import sys
import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
import os

# Determine project root
# Script is at: .claude/skills/chrome-update-digest/scripts/process_chrome.py
# We need to check for env var CHROME_UPDATE_DIGEST_BASE_PATH or detect project root
if 'CHROME_UPDATE_DIGEST_BASE_PATH' in os.environ:
    project_root = Path(os.environ['CHROME_UPDATE_DIGEST_BASE_PATH'])
else:
    # Go up from .claude/skills/chrome-update-digest/scripts/ to project root
    # Check if we're in the .claude directory structure
    current = Path(__file__).resolve()
    if '.claude' in current.parts:
        # Find the .claude directory and go up one level
        parts = list(current.parts)
        claude_idx = parts.index('.claude')
        project_root = Path(*parts[:claude_idx])
    else:
        # Fallback: assume we're 4 levels deep
        project_root = Path(__file__).parent.parent.parent.parent

sys.path.insert(0, str(project_root))

from chrome_update_digest.processors.clean_data_pipeline import CleanDataPipeline
from chrome_update_digest.utils.release_note_locator import find_chrome_release_note
import yaml


def load_area_yaml(version: str, channel: str, area: str, base_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load processed YAML file for a specific area.

    Args:
        version: Chrome version
        channel: Release channel
        area: Area key (e.g., 'css', 'webapi')
        base_path: Project root path

    Returns:
        Parsed YAML data or None if file not found
    """
    yaml_path = (
        base_path
        / "upstream_docs"
        / "processed_releasenotes"
        / "processed_forwebplatform"
        / "areas"
        / area
        / f"chrome-{version}-{channel}.yml"
    )

    if not yaml_path.exists():
        return None

    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_digest_prompt(language: str, base_path: Path) -> str:
    """
    Load the digest generation prompt template.

    Args:
        language: Language code ('en' or 'zh')
        base_path: Project root path

    Returns:
        Prompt template text
    """
    prompt_path = base_path / "prompts" / "webplatform-prompts" / f"webplatform-prompt-{language}.md"

    if not prompt_path.exists():
        # Return fallback prompt
        if language == 'zh':
            return "生成 Chrome 更新摘要，包括主要功能和重要链接。"
        return "Generate a Chrome update digest including main features and important links."

    return prompt_path.read_text(encoding='utf-8')


def format_yaml_for_llm(yaml_data: Dict[str, Any]) -> str:
    """
    Format YAML data for LLM consumption.

    Args:
        yaml_data: Parsed YAML data

    Returns:
        Formatted YAML string
    """
    lines = []
    lines.append(f"version: {yaml_data.get('version', 'Unknown')}")
    lines.append(f"channel: {yaml_data.get('channel', 'Unknown')}")
    lines.append(f"area: {yaml_data.get('area', 'all')}")
    lines.append("features:")

    for feature in yaml_data.get('features', []):
        lines.append(f"  - title: {feature.get('title', 'Untitled')}")
        lines.append(f"    summary: {feature.get('summary', '')}")
        content = feature.get('content', '').replace('\n', '\n      ')
        lines.append("    content: |")
        lines.append(f"      {content}")
        lines.append(f"    importance: {feature.get('importance', 'medium')}")

        links = feature.get('links', [])
        if links:
            lines.append("    links:")
            for link in links:
                lines.append(f"      - url: {link.get('url', '')}")
                lines.append(f"        title: {link.get('title', '')}")

    return '\n'.join(lines)


def validate_inputs(version: str, channel: str, base_path: Path) -> None:
    """
    Validate that required input files exist before processing.

    Args:
        version: Chrome version number
        channel: Release channel (stable or beta)
        base_path: Base path to project

    Raises:
        FileNotFoundError: If required files are missing
        ValueError: If parameters are invalid
    """
    # Validate version format
    try:
        int(version)
    except ValueError:
        raise ValueError(
            f"Invalid version format: '{version}'\n"
            f"Version must be a number (e.g., 139, 140)"
        )

    # Validate channel
    if channel not in ['stable', 'beta']:
        raise ValueError(
            f"Invalid channel: '{channel}'\n"
            f"Channel must be 'stable' or 'beta'"
        )

    # Check if release note file exists
    release_notes_dir = base_path / "upstream_docs" / "release_notes" / "WebPlatform"
    release_note_path = find_chrome_release_note(version, channel, release_notes_dir)

    if release_note_path is None:
        raise FileNotFoundError(
            f"Chrome {version} ({channel}) release notes not found.\n"
            f"Expected location: {release_notes_dir}/\n"
            f"Expected filename: chrome-{version}.md or chrome-{version}-{channel}.md\n\n"
            f"Solutions:\n"
            f"1. Download release notes from: https://developer.chrome.com/release-notes/{version}\n"
            f"2. Check if version {version} is released yet\n"
            f"3. Try a different channel (stable or beta)\n"
            f"4. Use the check-upstream script: uv run chrome-update-digest-cli check-upstream"
        )

    print(f"✓ Found release notes: {release_note_path.name}")


def get_all_areas(base_path: Path) -> List[str]:
    """
    Load all area names from focus_areas.yaml configuration.

    Args:
        base_path: Base path to project

    Returns:
        List of area keys
    """
    config_path = base_path / "config" / "focus_areas.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    areas = list(config.get('focus_areas', {}).keys())
    return areas


def get_output_path(version: str, channel: str, base_path: Path) -> Path:
    """
    Get the output path for processed release notes.

    Args:
        version: Chrome version number
        channel: Release channel
        base_path: Base path to project

    Returns:
        Path to output directory
    """
    return base_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "areas"


def process_chrome_release(
    version: str,
    channel: str = "stable",
    language: str = "bilingual",
    areas: Optional[List[str]] = None,
    verbose: bool = False,
    base_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Main processing function for Chrome release notes.

    This function orchestrates the complete workflow:
    1. Validate inputs
    2. Run clean data pipeline (extract area-specific YAML)
    3. Generate English digests using LLM
    4. Translate to Chinese (if requested)
    5. Write outputs

    Args:
        version: Chrome version number (e.g., "139")
        channel: Release channel ("stable" or "beta")
        language: Output language ("bilingual", "en", or "zh")
        areas: Specific areas to process (None = all areas)
        verbose: Enable detailed progress output
        base_path: Base path to project (auto-detected if None)

    Returns:
        Dictionary with processing results:
        {
            "version": str,
            "channel": str,
            "language": str,
            "areas": List[str],
            "output_path": Path,
            "status": str
        }
    """
    # Auto-detect base path if not provided
    if base_path is None:
        base_path = project_root

    if verbose:
        print(f"\n{'='*60}")
        print(f"Chrome Update Digest - Version {version} ({channel})")
        print(f"{'='*60}\n")

    # Step 1: Validate inputs
    if verbose:
        print("[1/4] Validating inputs...")

    validate_inputs(version, channel, base_path)

    # Determine which areas to process
    if areas is None:
        areas_to_process = get_all_areas(base_path)
        if verbose:
            print(f"✓ Processing all {len(areas_to_process)} areas")
    else:
        areas_to_process = areas
        if verbose:
            print(f"✓ Processing {len(areas_to_process)} areas: {', '.join(areas_to_process)}")

    # Step 2: Run clean data pipeline
    if verbose:
        print(f"\n[2/4] Running clean data pipeline for Chrome {version}...")

    pipeline = CleanDataPipeline()

    # Define output directories
    markdown_output_dir = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / "areas"
    yaml_output_dir = markdown_output_dir  # Same directory for YAML files

    try:
        results = pipeline.process_version_with_yaml(
            version=version,
            markdown_output_dir=markdown_output_dir,
            yaml_output_dir=yaml_output_dir,
            channel=channel
        )

        if verbose:
            total_areas = len(results.get('yaml', {}))
            print(f"✓ Processed {total_areas} areas, extracted YAML data")

    except Exception as e:
        print(f"✗ Error during pipeline processing: {e}")
        raise

    # Step 3: Generate digests
    if verbose:
        print(f"\n[3/4] Digest generation...")
        print(f"  YAML files prepared for {len(results.get('yaml', {}))} areas")
        print(f"  Ready for LLM-based digest generation")
        print(f"  → Use MCP tool 'digest_generate_area' for each area")
        print(f"  → Or Claude can generate digests directly from YAML files")

    # Step 4: Translation
    if verbose:
        print(f"\n[4/4] Translation...")
        if language in ("bilingual", "zh"):
            print("  Translation available via MCP tool 'digest_translate_area'")
            print("  Or Claude can translate English digests to Chinese")
        else:
            print("  ✓ English only mode (no translation needed)")

    output_path = get_output_path(version, channel, base_path)

    if verbose:
        print(f"\n{'='*60}")
        print(f"✓ Processing complete!")
        print(f"{'='*60}")
        print(f"Output location: {output_path}")
        print(f"YAML files: {len(results.get('yaml', {}))} areas")
        print(f"Markdown files: {len(results.get('markdown', {}))} areas")

    return {
        "version": version,
        "channel": channel,
        "language": language,
        "areas": areas_to_process,
        "output_path": str(output_path),
        "status": "success",
        "results": results
    }


def main():
    """Command-line entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Process Chrome release notes into area-specific digests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process Chrome 139 (stable, bilingual, all areas)
  %(prog)s --version 139 --verbose

  # Process Chrome 139 beta in English only
  %(prog)s --version 139 --channel beta --language en --verbose

  # Process specific areas only
  %(prog)s --version 139 --areas css webapi --verbose
        """
    )

    parser.add_argument(
        "--version",
        required=True,
        help="Chrome version to process (e.g., 139)"
    )

    parser.add_argument(
        "--channel",
        default="stable",
        choices=["stable", "beta"],
        help="Release channel (default: stable)"
    )

    parser.add_argument(
        "--language",
        default="bilingual",
        choices=["bilingual", "en", "zh"],
        help="Output language (default: bilingual)"
    )

    parser.add_argument(
        "--areas",
        nargs="+",
        help="Specific areas to process (default: all areas)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed progress output"
    )

    parser.add_argument(
        "--base-path",
        type=Path,
        help="Base path to project (default: auto-detect)"
    )

    args = parser.parse_args()

    try:
        result = process_chrome_release(
            version=args.version,
            channel=args.channel,
            language=args.language,
            areas=args.areas,
            verbose=args.verbose,
            base_path=args.base_path,
        )

        print(f"\n✓ Success! Generated outputs for {len(result['results'].get('yaml', {}))} areas")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
