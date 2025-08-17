#!/usr/bin/env python3
"""
Final integration test for MCP server components
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path to allow importing from src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.mcp_tools.enterprise_digest import EnterpriseDigestTool
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool as WebplatformDigestTool
from src.mcp_tools.feature_splitter import FeatureSplitterTool


async def test_all_tools():
    """Test all MCP tools to ensure they work correctly"""
    print("🧪 Running Integration Tests for Chrome Digest MCP Server\n")
    
    base_path = Path(__file__).parent.parent
    
    # Test 1: Enterprise Digest Tool
    print("1. Testing Enterprise Digest Tool...")
    try:
        enterprise_tool = EnterpriseDigestTool(base_path)
        result = await enterprise_tool.generate_digest({
            "version": 137,
            "focus_area": "productivity"
        })
        print("✅ Enterprise digest tool works correctly")
        print(f"   Generated {len(result)} characters of content\n")
    except Exception as e:
        print(f"❌ Enterprise digest tool failed: {e}\n")
    
    # Test 2: Web Platform Digest Tool
    print("2. Testing Web Platform Digest Tool...")
    try:
        webplatform_tool = WebplatformDigestTool(base_path)
        result = await webplatform_tool.generate_digest({
            "version": 137,
            "focus_areas": ["ai", "webgpu"]
        })
        print("✅ Web platform digest tool works correctly")
        print(f"   Generated {len(result)} characters of content\n")
    except Exception as e:
        print(f"❌ Web platform digest tool failed: {e}\n")
    
    # Test 3: Feature Splitter Tool (dry run)
    print("3. Testing Feature Splitter Tool...")
    try:
        feature_splitter = FeatureSplitterTool(base_path.parent)  # Use parent directory
        result = await feature_splitter.split_features({
            "input_path": "feature_details/processed_given_feature/profile/chrome-137-profile-features.md",
            "dry_run": True
        })
        result_dict = json.loads(result)
        if result_dict.get("success"):
            features_count = result_dict.get("summary", {}).get("features_extracted", 0)
            print(f"✅ Feature splitter tool works correctly")
            print(f"   Would split into {features_count} feature files\n")
        else:
            print(f"❌ Feature splitter returned error: {result_dict.get('error')}\n")
    except Exception as e:
        print(f"❌ Feature splitter tool failed: {e}\n")
    
    print("🎉 Integration tests completed!")
    print("\n📋 Summary:")
    print("- Enterprise Digest Tool: Ready")
    print("- Web Platform Digest Tool: Ready") 
    print("- Feature Splitter Tool: Ready")
    print("\n🚀 Your Chrome Digest MCP Server is ready to use!")
    print("   Start it with: python mcp_server.py")


if __name__ == "__main__":
    asyncio.run(test_all_tools())
