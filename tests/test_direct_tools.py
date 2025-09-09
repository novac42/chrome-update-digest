#!/usr/bin/env python3
"""
Test FastMCP WebPlatform tools by calling them directly
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the server directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_direct_call():
    """Test calling the tools directly"""
    try:
        from fast_mcp_server import webplatform_digest
        
        print("🌐 Testing webplatform digest function directly...")
        
        # Call webplatform function
        result = await webplatform_digest(
            version=138,
            channel="stable",
            focus_areas=["ai", "webgpu"],
            custom_instruction="Focus on AI and WebGPU"
        )
        
        print(f"WebPlatform digest result:\n{result}")
        
        result_data = json.loads(result)
        if result_data.get("success"):
            print("✅ WebPlatform digest successful!")
            
            # Check if file was created
            output_path = Path(result_data.get('output_path'))
            if output_path.exists():
                print("✅ WebPlatform digest file created!")
                print(f"   Path: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_call())
