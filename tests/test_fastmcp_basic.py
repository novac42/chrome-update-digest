#!/usr/bin/env python3
"""
FastMCP WebPlatform 基础功能测试
测试FastMCP服务器启动、resource读取等核心功能
"""

import sys
import asyncio
import json
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from fast_mcp_server import (
    load_prompt_from_resource, 
    load_processed_data,
    BASE_PATH
)


async def test_load_prompt_resources():
    """测试从resource加载prompt内容"""
    print("🧪 测试Resource读取功能...")
    
    test_cases = [
        ("webplatform-prompt", "chrome-update-analyzer-prompt-webplatform.md"),
        ("profile-keywords", "profile-keywords.txt")
    ]
    
    for resource_name, expected_file in test_cases:
        try:
            print(f"   📋 测试 {resource_name}...")
            content = await load_prompt_from_resource(resource_name)
            
            # 检查内容是否为空
            if not content or content.strip() == "":
                print(f"   ❌ {resource_name}: 内容为空")
                continue
            
            # 检查是否是错误消息
            if "not found" in content.lower():
                print(f"   ❌ {resource_name}: {content}")
                continue
                
            # 成功读取
            content_preview = content[:100] + "..." if len(content) > 100 else content
            print(f"   ✅ {resource_name}: 成功读取 {len(content)} 字符")
            print(f"      预览: {content_preview}")
            
        except Exception as e:
            print(f"   ❌ {resource_name}: 异常 - {str(e)}")
    
    print()


async def test_load_processed_data():
    """测试加载处理过的数据文件"""
    print("🧪 测试处理数据加载功能...")
    
    test_cases = [
        ("webplatform", 137, "stable"),
        ("webplatform", 138, "stable")
    ]
    
    for data_type, version, channel in test_cases:
        try:
            print(f"   📊 测试 {data_type} v{version} {channel}...")
            data = load_processed_data(data_type, version, channel)
            
            if not data or data.strip() == "":
                print(f"   ❌ {data_type} v{version}: 数据为空")
                continue
                
            # 成功读取
            data_preview = data[:100] + "..." if len(data) > 100 else data
            print(f"   ✅ {data_type} v{version}: 成功读取 {len(data)} 字符")
            print(f"      预览: {data_preview}")
            
        except Exception as e:
            print(f"   ❌ {data_type} v{version}: 异常 - {str(e)}")
    
    print()


def test_file_structure():
    """测试必要的文件和目录结构"""
    print("🧪 测试文件结构...")
    
    # 检查必要的目录
    required_dirs = [
        "prompts",
        "digest_markdown",
        "digest_markdown/webplatform",
        "digest_html",
        "upstream_docs",
        "upstream_docs/processed_releasenotes",
        "upstream_docs/processed_releasenotes/processed_forwebplatform",
        "src/mcp_tools",
        "templates"
    ]
    
    for dir_name in required_dirs:
        dir_path = BASE_PATH / dir_name
        if dir_path.exists():
            print(f"   ✅ 目录存在: {dir_name}")
        else:
            print(f"   ❌ 目录缺失: {dir_name}")
    
    # 检查必要的文件
    required_files = [
        "prompts/chrome-update-analyzer-prompt-webplatform.md", 
        "prompts/profile-keywords.txt",
        "src/convert_md2html.py",
        "templates/digest_webplatform.html"
    ]
    
    for file_name in required_files:
        file_path = BASE_PATH / file_name
        if file_path.exists():
            print(f"   ✅ 文件存在: {file_name}")
        else:
            print(f"   ❌ 文件缺失: {file_name}")
    
    print()


async def test_import_dependencies():
    """测试必要模块的导入"""
    print("🧪 测试模块导入...")
    
    try:
        print("   📦 测试 fastmcp 导入...")
        from fastmcp import FastMCP
        from fastmcp.resources import FileResource
        print("   ✅ FastMCP 导入成功")
    except ImportError as e:
        print(f"   ❌ FastMCP 导入失败: {e}")
    
    try:
        print("   📦 测试 convert_md2html 导入...")
        from src.convert_md2html import ChromeDigestConverter
        print("   ✅ ChromeDigestConverter 导入成功")
    except ImportError as e:
        print(f"   ❌ ChromeDigestConverter 导入失败: {e}")
    
    try:
        print("   📦 测试 feature_splitter 导入...")
        from src.mcp_tools.feature_splitter import FeatureSplitterTool
        print("   ✅ FeatureSplitterTool 导入成功")
    except ImportError as e:
        print(f"   ❌ FeatureSplitterTool 导入失败: {e}")
    
    print()


async def main():
    """主测试函数"""
    print("🚀 FastMCP 基础功能测试开始")
    print("=" * 50)
    
    # 测试文件结构
    test_file_structure()
    
    # 测试模块导入
    await test_import_dependencies()
    
    # 测试resource读取
    await test_load_prompt_resources()
    
    # 测试数据加载
    await test_load_processed_data()
    
    print("🏁 基础功能测试完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())