#!/usr/bin/env python3
"""
Chrome Update Digest Processing - Skill Orchestration Script

This script orchestrates the Chrome release note processing workflow.
It's designed to be self-contained and work with the installed CLI tools.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Import from local scripts directory
from project_paths import get_project_root, get_release_notes_dir


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

    # Download missing files
    download_commands = []

    if not chrome_exists:
        download_commands.append(("Chrome", f"""
import sys
from pathlib import Path
sys.path.insert(0, '{get_project_root() / "src"}')
from chrome_update_digest.utils.release_monitor_core import ReleaseMonitorCore
monitor = ReleaseMonitorCore(base_path=Path('{get_project_root()}'))
result = monitor.download_chrome_release({version}, '{channel}')
print(f"  ✓ Chrome: {{result['file_path']}}")
"""))

    if not webgpu_exists:
        download_commands.append(("WebGPU", f"""
import sys
from pathlib import Path
sys.path.insert(0, '{get_project_root() / "src"}')
from chrome_update_digest.utils.release_monitor_core import ReleaseMonitorCore
monitor = ReleaseMonitorCore(base_path=Path('{get_project_root()}'))
result = monitor.download_webgpu_release({version})
print(f"  ✓ WebGPU: {{result['file_path']}}")
"""))

    # Execute downloads
    failed_downloads = []
    for name, cmd_code in download_commands:
        cmd = ["uv", "run", "python", "-c", cmd_code]
        try:
            subprocess.run(cmd, cwd=get_project_root(), check=True)
        except subprocess.CalledProcessError as e:
            failed_downloads.append(name)
            print(f"  ✗ {name} download failed")

    if failed_downloads:
        print(f"\n⚠️  Some downloads failed: {', '.join(failed_downloads)}")
        print(f"Please download manually from: https://developer.chrome.com/release-notes/")
        print(f"Note: Processing may continue with available files")
    else:
        print(f"✓ Download complete")


def main():
    parser = argparse.ArgumentParser(description="Process Chrome release notes")
    parser.add_argument("--version", required=True, help="Chrome version (e.g., 143)")
    parser.add_argument("--channel", default="stable", choices=["stable", "beta"])
    parser.add_argument("--verbose", action="store_true")
    
    args = parser.parse_args()

    print(f"🚀 Processing Chrome {args.version} ({args.channel})")

    # Check and download release notes if needed
    check_and_download_release_notes(args.version, args.channel)

    # Step 1: Run clean pipeline
    print("[1/3] Running clean data pipeline...")
    pipeline_script = get_project_root() / "src/chrome_update_digest/processors/clean_data_pipeline.py"
    cmd = ["uv", "run", "python", str(pipeline_script),
           "--version", args.version, "--channel", args.channel, "--with-yaml"]
    subprocess.run(cmd, cwd=get_project_root(), check=True)

    # Step 2: Generate navigation
    print("[2/3] Generating GitHub Pages navigation...")
    nav_script = get_project_root() / "src/chrome_update_digest/tools/generate_github_pages_navigation.py"
    cmd = ["uv", "run", "python", str(nav_script)]
    subprocess.run(cmd, cwd=get_project_root(), check=True)
    
    print("\n✅ Processing complete!")
    print("💡 Next: Generate AI digests via MCP server if needed")

if __name__ == "__main__":
    main()
