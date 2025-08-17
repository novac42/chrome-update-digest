#!/usr/bin/env python3
"""
Simple test to debug FastMCP server issues
"""

import sys
from pathlib import Path

# Add the server directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_import():
    """Test importing the server"""
    try:
        from fast_mcp_server import mcp, BASE_PATH
        print("✅ FastMCP server imported successfully")
        print(f"✅ Base path: {BASE_PATH}")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resources():
    """Test resource files exist"""
    try:
        from fast_mcp_server import BASE_PATH
        
        resource_files = [
            "prompts/enterprise-update-prompt-en.md",
            "prompts/chrome-update-analyzer-prompt-webplatform.md", 
            "prompts/profile-keywords.txt"
        ]
        
        print("\n🔧 Testing resource files...")
        for file_name in resource_files:
            file_path = BASE_PATH / file_name
            if file_path.exists():
                print(f"  ✅ {file_name}")
            else:
                print(f"  ❌ {file_name} - Not found")
        return True
    except Exception as e:
        print(f"❌ Resource test failed: {e}")
        return False

def test_data_files():
    """Test data files exist"""
    try:
        from fast_mcp_server import BASE_PATH
        
        print("\n[DIR] Testing data files...")
        
        versions = [137, 138]
        for version in versions:
            # Enterprise data
            enterprise_path = BASE_PATH / "upstream_docs/processed_releasenotes/processed_forenterprise" / f"{version}-organized_chromechanges-enterprise.md"
            if enterprise_path.exists():
                print(f"  ✅ Enterprise v{version}")
            else:
                print(f"  ❌ Enterprise v{version} - Not found")
                
            # WebPlatform data
            webplatform_path = BASE_PATH / "upstream_docs/processed_releasenotes/processed_forwebplatform" / f"{version}-webplatform-with-webgpu.md"
            if webplatform_path.exists():
                print(f"  ✅ WebPlatform v{version}")
            else:
                print(f"  ❌ WebPlatform v{version} - Not found")
        
        return True
    except Exception as e:
        print(f"❌ Data files test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple FastMCP Test")
    print("=" * 40)
    
    success = True
    success = test_import() and success
    success = test_resources() and success  
    success = test_data_files() and success
    
    print("\n" + "=" * 40)
    if success:
        print("✅ All basic tests passed!")
    else:
        print("❌ Some tests failed!")
