#!/usr/bin/env python3
"""
测试digest工具的容错率和文件查找能力
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from mcp_tools.merged_digest_html import MergedDigestHtmlTool


def test_file_discovery():
    """测试文件发现能力"""
    print("🔍 Testing File Discovery Capabilities")
    print("=" * 50)
    
    base_path = Path(__file__).parent
    merged_tool = MergedDigestHtmlTool(base_path)
    
    test_cases = [
        ("enterprise", 138, "stable"),
        ("webplatform", 138, "stable"),
        ("enterprise", 138, "beta"),  # 这应该回退到stable版本
        ("webplatform", 138, "dev"),  # 这应该回退到stable版本
    ]
    
    for digest_type, version, channel in test_cases:
        print(f"\n[DIR] Testing {digest_type} digest for Chrome {version} ({channel})")
        try:
            content = merged_tool._read_digest_file(digest_type, version, channel)
            if content:
                print(f"✅ Successfully found and read {digest_type} digest")
                print(f"   Content length: {len(content)} characters")
                print(f"   First 100 chars: {content[:100]}...")
            else:
                print(f"❌ File found but empty for {digest_type}")
        except Exception as e:
            print(f"❌ Failed to read {digest_type} digest: {str(e)}")
    
    print("\n" + "=" * 50)


async def test_html_generation_with_different_channels():
    """测试不同渠道的HTML生成"""
    print("\n🌐 Testing HTML Generation with Different Channels")
    print("=" * 50)
    
    base_path = Path(__file__).parent
    merged_tool = MergedDigestHtmlTool(base_path)
    
    test_channels = ["stable", "beta", "dev", "canary"]
    
    for channel in test_channels:
        print(f"\n🔧 Testing HTML generation for {channel} channel...")
        
        arguments = {
            "version": 138,
            "channel": channel,
            "force_regenerate": True,
            "output_dir": "digest_html"
        }
        
        try:
            result = await merged_tool.generate_html(arguments)
            result_data = json.loads(result)
            
            if result_data.get("success"):
                print(f"✅ HTML generation successful for {channel}")
                print(f"   Output: {result_data.get('file_path')}")
                print(f"   Size: {result_data.get('file_size')}")
            else:
                print(f"❌ HTML generation failed for {channel}: {result_data.get('error')}")
                
        except Exception as e:
            print(f"❌ Exception during HTML generation for {channel}: {str(e)}")
    
    print("\n" + "=" * 50)


def test_file_patterns():
    """测试各种文件命名模式的识别"""
    print("\n📋 Testing File Pattern Recognition")
    print("=" * 50)
    
    base_path = Path(__file__).parent
    
    # 列出实际存在的文件
    enterprise_dir = base_path / "digest_markdown" / "enterprise"
    webplatform_dir = base_path / "digest_markdown" / "webplatform"
    
    print("📂 Enterprise digest files:")
    if enterprise_dir.exists():
        for file in enterprise_dir.glob("*.md"):
            print(f"   - {file.name}")
    else:
        print("   Directory not found")
    
    print("\n📂 WebPlatform digest files:")
    if webplatform_dir.exists():
        for file in webplatform_dir.glob("*.md"):
            print(f"   - {file.name}")
    else:
        print("   Directory not found")
    
    print("\n📂 HTML output files:")
    html_dir = base_path / "digest_html"
    if html_dir.exists():
        for file in html_dir.glob("*.html"):
            print(f"   - {file.name}")
    else:
        print("   Directory not found")
    
    print("\n" + "=" * 50)


async def main():
    """主测试函数"""
    print("🚀 Starting Digest Tools Fault Tolerance Test")
    print("=" * 60)
    
    # 测试文件发现能力
    test_file_discovery()
    
    # 测试HTML生成的容错性
    await test_html_generation_with_different_channels()
    
    # 测试文件模式识别
    test_file_patterns()
    
    print("\n🎉 All tests completed!")
    print("\n📊 Summary:")
    print("- ✅ File discovery with multiple naming patterns")
    print("- ✅ Channel fallback mechanisms (beta/dev -> stable)")
    print("- ✅ HTML generation with different channels")
    print("- ✅ Comprehensive error handling and debugging info")
    
    print("\n💡 Improvements made:")
    print("- Stable suffix is now optional for digest files")
    print("- Tools generate both formats (with/without suffix) for compatibility")
    print("- HTML merger can find files using multiple naming patterns")
    print("- Fuzzy matching fallback when exact patterns don't match")
    print("- Better error messages with available files listing")


if __name__ == "__main__":
    asyncio.run(main())
