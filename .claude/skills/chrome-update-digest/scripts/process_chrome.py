#!/usr/bin/env python3
"""
Chrome Update Digest Processing - Skill Orchestration Script

This script orchestrates the Chrome release note processing workflow.
It's self-contained with vendored dependencies.

WORKFLOW:
1. Download missing release notes (Chrome + WebGPU)
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
    1. Chrome WebPlatform release notes (chrome-{version}.md)
    2. WebGPU release notes (webgpu-{version}.md)

    Both need to be downloaded for complete coverage.
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
        print(f"✓ Chrome and WebGPU release notes found")
        return
    elif chrome_exists:
        print(f"✓ Chrome release notes found")
        print(f"⬇️  WebGPU release notes missing, downloading...")
    elif webgpu_exists:
        print(f"✓ WebGPU release notes found")
        print(f"⬇️  Chrome release notes missing, downloading...")
    else:
        print(f"⬇️  Release notes not found, downloading both Chrome and WebGPU...")

    # Download missing files using vendored ReleaseMonitorCore
    monitor = ReleaseMonitorCore(base_path=get_project_root())

    if not chrome_exists:
        try:
            result = monitor.download_chrome_release(version, channel)
            print(f"  ✓ Chrome: {result['file_path']}")
        except Exception as e:
            print(f"  ✗ Chrome download failed: {e}")

    if not webgpu_exists:
        try:
            result = monitor.download_webgpu_release(version)
            print(f"  ✓ WebGPU: {result['file_path']}")
        except Exception as e:
            print(f"  ✗ WebGPU download failed: {e}")

    print(f"✓ Download complete")


def main():
    parser = argparse.ArgumentParser(description="Process Chrome release notes")
    parser.add_argument("--version", required=True, help="Chrome version (e.g., 143)")
    parser.add_argument("--channel", default="stable", choices=["stable", "beta"])
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    print(f"🚀 Processing Chrome {args.version} ({args.channel})")

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

    print("\n✅ Processing complete!")
    print("💡 Next: Generate AI digests using bundled prompts")
    print(f"   - English prompt: {SKILL_ROOT}/prompts/webplatform-prompt-en.md")
    print(f"   - Chinese prompt: {SKILL_ROOT}/prompts/webplatform-translation-prompt-zh.md")

if __name__ == "__main__":
    main()
