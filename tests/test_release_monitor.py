#!/usr/bin/env python3
"""
Test script for the release monitor functionality
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from utils.release_monitor_core import ReleaseMonitorCore


def test_release_monitor():
    """Test the release monitor functionality"""
    base_path = Path(__file__).parent
    monitor = ReleaseMonitorCore(base_path)
    
    print("Testing Release Monitor Core")
    print("=" * 50)
    
    # Test 1: Scan existing versions
    print("\n1. Scanning existing versions...")
    existing = monitor.scan_existing_versions()
    print(f"   WebPlatform versions: {sorted(existing['webplatform'])}")
    print(f"   Enterprise versions: {sorted(existing['enterprise'])}")
    
    # Test 2: Detect latest versions
    print("\n2. Detecting latest versions from web...")
    
    latest_chrome = monitor.detect_latest_webplatform_version()
    print(f"   Latest Chrome version: {latest_chrome}")
    
    latest_webgpu = monitor.detect_latest_webgpu_version()
    print(f"   Latest WebGPU version: {latest_webgpu}")
    
    latest_enterprise = monitor.detect_latest_enterprise_version()
    if latest_enterprise:
        version_id, url = latest_enterprise
        print(f"   Latest Enterprise version: {version_id}")
        print(f"   Enterprise URL: {url}")
    else:
        print("   Could not detect Enterprise version")
    
    # Test 3: Check what's missing
    print("\n3. Checking for missing releases...")
    missing = []
    
    if latest_chrome and latest_chrome not in existing['webplatform']:
        missing.append(f"Chrome {latest_chrome}")
    
    if latest_webgpu and latest_webgpu not in existing['webplatform']:
        missing.append(f"WebGPU {latest_webgpu}")
    
    if latest_enterprise:
        version_id, _ = latest_enterprise
        if version_id not in existing['enterprise']:
            missing.append(f"Enterprise {version_id}")
    
    if missing:
        print(f"   Missing releases: {', '.join(missing)}")
    else:
        print("   All releases are up to date!")
    
    print("\n" + "=" * 50)
    print("Test completed!")


if __name__ == "__main__":
    test_release_monitor()