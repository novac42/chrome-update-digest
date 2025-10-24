#!/usr/bin/env python3
"""
Test actual splitting (non-dry-run) for the feature splitter tool
"""

import pytest

import asyncio
import json
import os
import shutil
from pathlib import Path
import sys
from pathlib import Path

# Add project root to path to allow importing from src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chrome_update_digest.mcp.tools.feature_splitter import FeatureSplitterTool


@pytest.mark.asyncio
async def test_actual_split():
    """Test actual file splitting with a single file"""
    print("=== Testing Actual File Splitting ===\n")
    
    base_path = Path(__file__).parent.parent
    splitter = FeatureSplitterTool(base_path)
    
    # Create a test output directory
    test_output_dir = base_path / "tests" / "feature_split_output"
    
    # Clean up any existing test output
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)
    
    # Ensure test directory exists
    test_output_dir.parent.mkdir(exist_ok=True)
    
    test_arguments = {
        "input_path": "feature_details/processed_given_feature/profile/chrome-137-profile-features.md",
        "output_base_dir": str(test_output_dir),
        "dry_run": False
    }
    
    print(f"Testing with arguments: {test_arguments}\n")
    
    result = await splitter.split_features(test_arguments)
    result_dict = json.loads(result)
    
    print("Result:")
    print(json.dumps(result_dict, indent=2))
    
    # Check if files were actually created
    if result_dict.get("success"):
        output_dir = test_output_dir / "profile-137"
        if output_dir.exists():
            created_files = list(output_dir.glob("*.md"))
            print(f"\n✅ Successfully created {len(created_files)} files in {output_dir}:")
            for file in created_files[:5]:  # Show first 5 files
                print(f"  - {file.name}")
            if len(created_files) > 5:
                print(f"  ... and {len(created_files) - 5} more files")
                
            # Show content of one file as sample
            sample_file = created_files[0]
            print(f"\nSample content from {sample_file.name}:")
            print("=" * 50)
            with open(sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Show first 300 characters
                print(content[:300] + "..." if len(content) > 300 else content)
            print("=" * 50)
        else:
            print(f"❌ Expected output directory {output_dir} was not created")
    
    return result_dict


async def main():
    """Run test"""
    try:
        await test_actual_split()
        print("\n✅ Actual splitting test completed!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
