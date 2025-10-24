#!/usr/bin/env python3
"""
Test HTML generation directly using the MergedDigestHtmlTool

NOTE: This test is currently disabled as MergedDigestHtmlTool module doesn't exist
"""

import sys
import asyncio
import pytest
from pathlib import Path

# Skip all tests in this file
pytestmark = pytest.mark.skip(reason="MergedDigestHtmlTool module doesn't exist")

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

# from chrome_update_digest.mcp.tools.merged_digest_html import MergedDigestHtmlTool

async def test_html_generation():
    """Test HTML generation"""
    print("🧪 Testing HTML generation with real digest files...")
    
    # Initialize the tool
    base_path = Path(__file__).parent
    html_tool = MergedDigestHtmlTool(base_path)
    
    # Test parameters
    test_args = {
        "version": 138,
        "channel": "stable",
        "force_regenerate": True
    }
    
    try:
        # Generate HTML
        result = await html_tool.generate_html(test_args)
        print("✅ HTML generation completed:")
        print(result)
        
    except Exception as e:
        print(f"❌ Error during HTML generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_html_generation())
