#!/usr/bin/env python3
"""
Test individual FastMCP tools
"""

import pytest

import asyncio
import json
import sys
from pathlib import Path

# Add the server directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

@pytest.mark.asyncio
async def test_single_tool():
    """Test a single tool call"""
    try:
        from fast_mcp_server import mcp
        
        print("🏢 Testing enterprise digest tool...")
        
        # Test enterprise digest
        result = await mcp.call_tool("enterprise_digest", {
            "version": 138,
            "channel": "stable",
            "focus_area": "security"
        })
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        result_data = json.loads(result)
        
        if result_data.get("success"):
            print("✅ Tool call successful!")
            print(f"Output path: {result_data.get('output_path')}")
            
            # Check if file was created
            output_path = Path(result_data.get('output_path'))
            if output_path.exists():
                print("✅ Output file created!")
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"Content preview:\n{content[:500]}...")
            else:
                print("❌ Output file not found")
        else:
            print(f"❌ Tool call failed: {result_data.get('error')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_single_tool())
