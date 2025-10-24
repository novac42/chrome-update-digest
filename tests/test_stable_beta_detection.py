"""
Integration test for stable vs beta channel detection.
This test verifies the key requirement that:
- Files without channel suffix (e.g., chrome-136.md) are detected as stable
- Files with beta suffix (e.g., chrome-139-beta.md) are detected as beta
- Missing stable versions are detected when beta exists
"""

import tempfile
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from chrome_update_digest.utils.release_monitor_core import ReleaseMonitorCore


def test_stable_beta_channel_detection():
    """Test that stable and beta channels are correctly detected."""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        monitor = ReleaseMonitorCore(base_path)
        
        # Create test directory structure
        webplatform_dir = base_path / "upstream_docs" / "release_notes" / "webplatform"
        webplatform_dir.mkdir(parents=True)
        
        # Create stable versions (no suffix)
        (webplatform_dir / "chrome-136.md").write_text("Chrome 136 stable content")
        (webplatform_dir / "chrome-137.md").write_text("Chrome 137 stable content")
        (webplatform_dir / "chrome-138.md").write_text("Chrome 138 stable content")
        
        # Create beta versions (with beta suffix)
        (webplatform_dir / "chrome-139-beta.md").write_text("Chrome 139 beta content")
        (webplatform_dir / "chrome-140-beta.md").write_text("Chrome 140 beta content")
        
        # Also create a version that has both stable and beta
        (webplatform_dir / "chrome-135.md").write_text("Chrome 135 stable content")
        (webplatform_dir / "chrome-135-beta.md").write_text("Chrome 135 beta content")
        
        # Test 1: Stable channel scanning
        print("Test 1: Scanning stable channel...")
        stable_versions = monitor.scan_existing_versions("stable")
        assert stable_versions["webplatform"] == {135, 136, 137, 138}, f"Expected {{135, 136, 137, 138}}, got {stable_versions['webplatform']}"
        print(f"✅ Stable versions correctly detected: {sorted(stable_versions['webplatform'])}")
        
        # Test 2: Beta channel scanning
        print("\nTest 2: Scanning beta channel...")
        beta_versions = monitor.scan_existing_versions("beta")
        assert beta_versions["webplatform"] == {135, 139, 140}, f"Expected {{135, 139, 140}}, got {beta_versions['webplatform']}"
        print(f"✅ Beta versions correctly detected: {sorted(beta_versions['webplatform'])}")
        
        # Test 3: Missing stable detection
        print("\nTest 3: Detecting missing stable versions...")
        missing_stable = monitor.detect_missing_stable_versions()
        assert set(missing_stable) == {139, 140}, f"Expected {{139, 140}}, got {set(missing_stable)}"
        print(f"✅ Missing stable versions correctly detected: {missing_stable}")
        print("   (These versions have beta but no stable release)")
        
        # Test 4: Verify chrome-136.md is recognized as STABLE (not beta)
        print("\nTest 4: Verifying chrome-136.md is recognized as stable...")
        assert 136 in stable_versions["webplatform"], "chrome-136.md should be detected as stable"
        assert 136 not in beta_versions["webplatform"], "chrome-136.md should NOT be detected as beta"
        print("✅ chrome-136.md correctly identified as stable channel")
        
        # Test 5: Verify chrome-139-beta.md is NOT recognized as stable
        print("\nTest 5: Verifying chrome-139-beta.md is NOT recognized as stable...")
        assert 139 not in stable_versions["webplatform"], "chrome-139-beta.md should NOT be detected as stable"
        assert 139 in beta_versions["webplatform"], "chrome-139-beta.md should be detected as beta"
        print("✅ chrome-139-beta.md correctly identified as beta channel only")
        
        print("\n" + "="*60)
        print("All tests passed! Channel detection working correctly.")
        print("="*60)
        
        return True


if __name__ == "__main__":
    success = test_stable_beta_channel_detection()
    if success:
        print("\n✅ SUCCESS: Stable vs Beta channel detection is working correctly!")
        print("\nKey findings:")
        print("1. Files without suffix (e.g., chrome-136.md) → STABLE channel")
        print("2. Files with -beta suffix (e.g., chrome-139-beta.md) → BETA channel")
        print("3. Missing stable detection works: if only chrome-139-beta.md exists,")
        print("   the system correctly identifies that stable v139 is missing")
    else:
        print("\n❌ FAILED: Channel detection has issues")
        sys.exit(1)