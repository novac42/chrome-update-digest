#!/usr/bin/env python3
"""
Chrome Update Digest Processing - Skill Orchestration Script

This script orchestrates the Chrome release note processing workflow.
It's self-contained with vendored dependencies.

DESIGN: Stateless processing - no version history tracking.
Each run is independent and only processes the specified version.

WORKFLOW:
1. Download missing release notes (Chrome required, WebGPU optional)
2. Run clean pipeline to extract area-specific content
3. Generate GitHub Pages navigation structure

NOTE: AI digest generation (step between 2 and 3) should be done by the
agent invoking this skill using bundled prompts.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Add vendored modules to path
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT / "vendored"))
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from project_paths import get_project_root, get_release_notes_dir
from utils.release_monitor_core import ReleaseMonitorCore
from processors.clean_data_pipeline import main as clean_pipeline_main
from tools.generate_github_pages_navigation import GitHubPagesNavigationGenerator


def check_and_download_release_notes(version: str, channel: str) -> None:
    """Check if release notes exist, download if missing.

    Chrome releases have two sources:
    1. Chrome WebPlatform release notes (chrome-{version}.md) - REQUIRED
    2. WebGPU release notes (webgpu-{version}.md) - OPTIONAL

    WebGPU enhances the graphics-webgpu area when available but is not required.
    """
    release_notes_dir = get_release_notes_dir()

    # Check Chrome WebPlatform release notes
    if channel == "stable":
        chrome_files = [
            release_notes_dir / f"chrome-{version}.md",
            release_notes_dir / f"chrome-{version}-stable.md"
        ]
    else:
        chrome_files = [release_notes_dir / f"chrome-{version}-{channel}.md"]

    chrome_exists = any(f.exists() for f in chrome_files)

    # Check WebGPU release notes
    webgpu_file = release_notes_dir / f"webgpu-{version}.md"
    webgpu_exists = webgpu_file.exists()

    # Report what exists
    if chrome_exists and webgpu_exists:
        print(f"[OK] Chrome and WebGPU release notes found")
        return
    elif chrome_exists:
        print(f"[OK] Chrome release notes found")
        print(f"[DOWNLOAD] WebGPU release notes missing, downloading...")
    elif webgpu_exists:
        print(f"[OK] WebGPU release notes found")
        print(f"[DOWNLOAD] Chrome release notes missing, downloading...")
    else:
        print(f"[DOWNLOAD] Release notes not found, downloading both Chrome and WebGPU...")

    # Download missing files using vendored ReleaseMonitorCore
    monitor = ReleaseMonitorCore(base_path=get_project_root())

    if not chrome_exists:
        try:
            result = monitor.download_chrome_release(version, channel)
            print(f"  [OK] Chrome: {result['file_path']}")
        except Exception as e:
            print(f"  [ERROR] Chrome download failed: {e}")

    if not webgpu_exists:
        try:
            result = monitor.download_webgpu_release(version)
            print(f"  [OK] WebGPU: {result['file_path']}")
        except Exception as e:
            print(f"  [ERROR] WebGPU download failed: {e}")

    print(f"[OK] Download complete")


def check_latest_chrome_version() -> dict:
    """Check latest Chrome stable and beta versions.

    Returns:
        dict: {'stable': str, 'beta': str} with version numbers

    Note: This is a stateless query - no version history tracking.
    """
    monitor = ReleaseMonitorCore(base_path=get_project_root())
    try:
        # Detect latest Chrome version from web probing
        stable_version = monitor.detect_latest_webplatform_version()

        # Scan existing versions to estimate beta
        existing = monitor.scan_existing_versions("beta")
        beta_versions = existing.get("webplatform", set())
        beta_version = max(beta_versions) if beta_versions else None

        return {
            'stable': str(stable_version) if stable_version else 'unknown',
            'beta': str(beta_version) if beta_version else 'unknown'
        }
    except Exception as e:
        print(f"X Failed to check latest versions: {e}")
        return {'stable': 'unknown', 'beta': 'unknown'}


def get_areas_to_process(version: str, channel: str) -> list:
    """Get list of areas that have been extracted for this version.

    Args:
        version: Chrome version number (e.g., "143")
        channel: Release channel ("stable" or "beta")

    Returns:
        List of area names that have YAML files

    Note: This checks what was extracted by the clean pipeline.
    Used by agents to know which areas need digest generation.
    """
    processed_dir = get_project_root() / "upstream_docs/processed_releasenotes/processed_forwebplatform/areas"

    if not processed_dir.exists():
        return []

    areas = []
    for area_dir in processed_dir.iterdir():
        if area_dir.is_dir():
            yaml_file = area_dir / f"chrome-{version}-{channel}.yml"
            if yaml_file.exists():
                areas.append(area_dir.name)

    return sorted(areas)


def main():
    parser = argparse.ArgumentParser(
        description="Process Chrome release notes (stateless, no version history)"
    )
    parser.add_argument("--version", help="Chrome version (e.g., 143)")
    parser.add_argument("--channel", default="stable", choices=["stable", "beta"])
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--check-latest", action="store_true",
                       help="Check latest Chrome versions and exit")
    parser.add_argument("--list-areas", action="store_true",
                       help="List areas extracted for this version and exit")

    args = parser.parse_args()

    # Handle --check-latest
    if args.check_latest:
        print("Checking latest Chrome versions...")
        versions = check_latest_chrome_version()
        print(f"\nLatest Chrome versions:")
        print(f"  Stable: {versions['stable']}")
        print(f"  Beta:   {versions['beta']}")
        return

    # Handle --list-areas
    if args.list_areas:
        if not args.version:
            print("Error: --list-areas requires --version")
            sys.exit(1)
        print(f"Checking areas for Chrome {args.version} ({args.channel})...")
        areas = get_areas_to_process(args.version, args.channel)
        if areas:
            print(f"\nFound {len(areas)} areas:")
            for area in areas:
                print(f"  - {area}")
        else:
            print(f"\nNo areas found. Run without --list-areas to process first.")
        return

    # Require version for normal processing
    if not args.version:
        print("Error: --version is required for processing")
        parser.print_help()
        sys.exit(1)

    print(f"Processing Chrome {args.version} ({args.channel})")

    # Step 0: Check and download release notes if needed
    check_and_download_release_notes(args.version, args.channel)

    # Step 1: Run clean pipeline using vendored module
    print("[1/2] Running clean data pipeline...")
    # Set up sys.argv for clean_pipeline_main
    original_argv = sys.argv
    sys.argv = [
        "clean_data_pipeline.py",
        "--version", args.version,
        "--channel", args.channel,
        "--with-yaml"
    ]
    try:
        clean_pipeline_main()
    finally:
        sys.argv = original_argv

    # Step 2: Generate navigation using vendored module
    print("[2/2] Generating GitHub Pages navigation...")
    generator = GitHubPagesNavigationGenerator(base_path=str(get_project_root()))
    generator.run()

    print("\n[DONE] Processing complete!")
    print("[INFO] Next: Generate AI digests using bundled prompts")
    print(f"   - English prompt: {SKILL_ROOT}/prompts/webplatform-prompt-en.md")
    print(f"   - Chinese prompt: {SKILL_ROOT}/prompts/webplatform-translation-prompt-zh.md")
    print(f"\n[INFO] To see extracted areas: python {__file__} --version {args.version} --channel {args.channel} --list-areas")

if __name__ == "__main__":
    main()
