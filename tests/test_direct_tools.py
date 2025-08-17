#!/usr/bin/env python3
"""
Test FastMCP tools by calling them directly
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
        from fast_mcp_server import enterprise_digest, webplatform_digest, merged_digest_html
        
        print("🏢 Testing enterprise digest function directly...")
        
        # Call the function directly
        result = await enterprise_digest(
            version=138,
            channel="stable",
            focus_area="security",
            custom_instruction="Focus on security improvements"
        )
        
        print(f"Enterprise digest result:\n{result}")
        
        result_data = json.loads(result)
        if result_data.get("success"):
            print("✅ Enterprise digest successful!")
            
            # Check if file was created
            output_path = Path(result_data.get('output_path'))
            if output_path.exists():
                print("✅ Enterprise digest file created!")
                print(f"   Path: {output_path}")
        
        print("\n🌐 Testing webplatform digest function directly...")
        
        # Call webplatform function
        result2 = await webplatform_digest(
            version=138,
            channel="stable",
            focus_areas=["ai", "webgpu"],
            custom_instruction="Focus on AI and WebGPU"
        )
        
        print(f"WebPlatform digest result:\n{result2}")
        
        result2_data = json.loads(result2)
        if result2_data.get("success"):
            print("✅ WebPlatform digest successful!")
            
            # Check if file was created
            output_path2 = Path(result2_data.get('output_path'))
            if output_path2.exists():
                print("✅ WebPlatform digest file created!")
                print(f"   Path: {output_path2}")
        
        print("\n📄 Testing merged HTML generation...")
        
        # Call merged HTML function
        result3 = await merged_digest_html(
            version=138,
            channel="stable",
            force_regenerate=True
        )
        
        print(f"Merged HTML result:\n{result3}")
        
        result3_data = json.loads(result3)
        if result3_data.get("success"):
            print("✅ Merged HTML successful!")
            
            # Check if file was created
            output_path3 = Path(result3_data.get('output_path'))
            if output_path3.exists():
                print("✅ HTML file created!")
                print(f"   Path: {output_path3}")
                
                # Show a preview of the HTML
                with open(output_path3, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    print(f"   HTML size: {len(html_content)} characters")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_call())
