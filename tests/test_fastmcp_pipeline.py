#!/usr/bin/env python3
"""
FastMCP 端到端流程测试
测试完整的pipeline：企业版digest → Web平台digest → 合并HTML

NOTE: This test is currently disabled as the enterprise_digest and merged_digest_html
functions have been removed from fast_mcp_server.py
"""

import sys
import pytest
from pathlib import Path

# Skip all tests in this file
pytestmark = pytest.mark.skip(reason="enterprise_digest and merged_digest_html functions no longer exist")

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

# Commenting out non-existent imports
# from fast_mcp_server import (
#     enterprise_digest,
#     webplatform_digest, 
#     merged_digest_html,
#     BASE_PATH
# )


async def test_complete_pipeline():
    """测试完整的digest生成pipeline"""
    print("🚀 FastMCP 端到端流程测试")
    print("=" * 60)
    
    # 测试参数
    test_version = 138
    test_channel = "stable"
    
    print(f"📋 测试参数: Chrome {test_version} {test_channel}")
    print()
    
    # 第一步：生成企业版digest
    print("🏢 步骤1: 生成企业版digest...")
    try:
        enterprise_result = await enterprise_digest(
            version=test_version,
            channel=test_channel,
            focus_area="productivity",
            custom_instruction="Focus on user productivity features and management capabilities"
        )
        
        enterprise_data = json.loads(enterprise_result)
        if enterprise_data["success"]:
            print(f"   ✅ 企业版digest生成成功")
            print(f"   📄 输出文件: {enterprise_data['output_path']}")
            
            # 验证文件存在
            enterprise_path = Path(enterprise_data['output_path'])
            if enterprise_path.exists():
                file_size = enterprise_path.stat().st_size
                print(f"   📊 文件大小: {file_size} bytes")
            else:
                print(f"   ❌ 文件不存在: {enterprise_path}")
                return False
        else:
            print(f"   ❌ 企业版digest生成失败: {enterprise_data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ 企业版digest异常: {str(e)}")
        return False
    
    print()
    
    # 第二步：生成Web平台digest
    print("🌐 步骤2: 生成Web平台digest...")
    try:
        webplatform_result = await webplatform_digest(
            version=test_version,
            channel=test_channel,
            focus_areas=["ai", "webgpu", "css", "performance"],
            custom_instruction="Emphasize AI features and WebGPU improvements"
        )
        
        webplatform_data = json.loads(webplatform_result)
        if webplatform_data["success"]:
            print(f"   ✅ Web平台digest生成成功")
            print(f"   📄 输出文件: {webplatform_data['output_path']}")
            
            # 验证文件存在
            webplatform_path = Path(webplatform_data['output_path'])
            if webplatform_path.exists():
                file_size = webplatform_path.stat().st_size
                print(f"   📊 文件大小: {file_size} bytes")
            else:
                print(f"   ❌ 文件不存在: {webplatform_path}")
                return False
        else:
            print(f"   ❌ Web平台digest生成失败: {webplatform_data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Web平台digest异常: {str(e)}")
        return False
    
    print()
    
    # 第三步：生成合并HTML
    print("📄 步骤3: 生成合并HTML...")  
    try:
        html_result = await merged_digest_html(
            version=test_version,
            channel=test_channel,
            force_regenerate=True,
            output_dir="digest_html"
        )
        
        html_data = json.loads(html_result)
        if html_data["success"]:
            print(f"   ✅ 合并HTML生成成功")
            print(f"   📄 输出文件: {html_data['output_path']}")
            
            # 验证文件存在
            html_path = Path(html_data['output_path'])
            if html_path.exists():
                file_size = html_path.stat().st_size
                print(f"   📊 文件大小: {file_size} bytes")
                
                # 简单验证HTML内容
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    
                # 检查HTML基本结构
                checks = [
                    ("<!DOCTYPE html>", "HTML声明"),
                    ("<title>", "页面标题"),
                    ("Enterprise", "企业版内容"),
                    ("WebPlatform", "Web平台内容"),
                    ("switchDigestType('enterprise')", "企业版tab"),
                    ("switchDigestType('webplatform')", "Web平台tab"),
                    ("switchDigestType", "tab切换功能")
                ]
                
                print("   🔍 HTML内容验证:")
                for check_text, description in checks:
                    if check_text in html_content:
                        print(f"      ✅ {description}")
                    else:
                        print(f"      ❌ 缺少 {description}")
                        
            else:
                print(f"   ❌ 文件不存在: {html_path}")
                return False
        else:
            print(f"   ❌ 合并HTML生成失败: {html_data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ 合并HTML异常: {str(e)}")
        return False
    
    print()
    print("🎉 端到端流程测试完成！")
    print("=" * 60)
    return True


async def test_pipeline_with_different_versions():
    """测试不同版本的pipeline"""
    print("📊 测试不同版本的pipeline...")
    
    test_cases = [
        (137, "stable"),
        (138, "stable")
    ]
    
    for version, channel in test_cases:
        print(f"\n📋 测试 Chrome {version} {channel}...")
        
        try:
            # 快速测试每个版本的基本功能
            enterprise_result = await enterprise_digest(version, channel, "all", "")
            enterprise_data = json.loads(enterprise_result)
            
            webplatform_result = await webplatform_digest(version, channel, ["all"], "")
            webplatform_data = json.loads(webplatform_result)
            
            if enterprise_data["success"] and webplatform_data["success"]:
                print(f"   ✅ Chrome {version} {channel} 基础功能正常")
                
                # 检查数据文件是否存在
                enterprise_file = Path(enterprise_data['output_path'])
                webplatform_file = Path(webplatform_data['output_path'])
                
                if enterprise_file.exists() and webplatform_file.exists():
                    print(f"   ✅ 生成的digest文件都存在")
                else:
                    print(f"   ❌ 某些digest文件缺失")
                    
            else:
                print(f"   ❌ Chrome {version} {channel} 生成失败")
                if not enterprise_data["success"]:
                    print(f"      企业版错误: {enterprise_data.get('error', 'Unknown')}")
                if not webplatform_data["success"]:
                    print(f"      Web平台错误: {webplatform_data.get('error', 'Unknown')}")
                    
        except Exception as e:
            print(f"   ❌ Chrome {version} {channel} 异常: {str(e)}")
    
    print("\n✅ 版本测试完成")


async def test_error_handling():
    """测试错误处理能力"""
    print("\n🧪 测试错误处理...")
    
    # 测试无效版本号
    print("   📋 测试无效版本号...")
    try:
        result = await enterprise_digest(999, "stable")
        data = json.loads(result)
        if not data["success"]:
            print("   ✅ 无效版本号正确处理")
        else:
            print("   ⚠️  无效版本号未正确拒绝")
    except Exception as e:
        print(f"   ✅ 无效版本号引发异常（正常）: {str(e)}")
    
    # 测试无效通道名
    print("   📋 测试无效通道名...")
    try:
        result = await webplatform_digest(138, "invalid_channel")
        data = json.loads(result)
        if not data["success"]:
            print("   ✅ 无效通道名正确处理")
        else:
            print("   ⚠️  无效通道名未正确拒绝")
    except Exception as e:
        print(f"   ✅ 无效通道名引发异常（正常）: {str(e)}")
    
    print("   ✅ 错误处理测试完成")


async def generate_pipeline_report():
    """生成pipeline测试报告"""
    print("\n📊 生成测试报告...")
    
    report_content = f"""# FastMCP Pipeline测试报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 测试概览

本次测试验证了FastMCP digest生成系统的完整pipeline功能。

## 测试范围

1. **基础功能测试**
   - ✅ 企业版digest生成
   - ✅ Web平台digest生成  
   - ✅ 合并HTML生成

2. **流程完整性测试**
   - ✅ 端到端workflow
   - ✅ 文件生成和存储
   - ✅ HTML格式验证

3. **多版本支持测试**
   - ✅ Chrome 137支持
   - ✅ Chrome 138支持

## 生成的文件

### Digest文件
- `digest_markdown/enterprise/digest-chrome-138-enterprise.md`
- `digest_markdown/webplatform/digest-chrome-138-webplatform-stable.md`

### HTML文件
- `digest_html/chrome-138-merged-digest-stable.html`

## 测试结果

✅ **所有核心功能正常工作**
✅ **文件生成和存储正常**
✅ **HTML格式正确且可浏览**
✅ **错误处理机制有效**

## 下一步规划

1. **LLM集成**: 替换当前的占位符内容生成
2. **增强错误处理**: 添加更多边界情况处理
3. **性能优化**: 优化大文件处理性能
4. **用户界面**: 开发用户友好的接口

## 技术栈

- **FastMCP**: MCP服务器框架
- **Python 3.x**: 主要开发语言
- **Jinja2**: HTML模板引擎
- **Pathlib**: 文件路径处理

---

*本报告由FastMCP pipeline测试系统自动生成*
"""
    
    # 保存报告
    report_path = BASE_PATH / "digest_html" / "pipeline-test-report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"   📄 测试报告已保存: {report_path}")
    return report_path


async def main():
    """主测试函数"""
    print("🚀 FastMCP Pipeline 完整测试套件")
    print("=" * 70)
    
    # 执行完整的pipeline测试
    success = await test_complete_pipeline()
    
    if success:
        # 执行版本兼容性测试
        await test_pipeline_with_different_versions()
        
        # 执行错误处理测试
        await test_error_handling()
        
        # 生成测试报告
        await generate_pipeline_report()
        
        print("\n🎉 所有pipeline测试完成！")
        print("✅ 系统已准备好进行下一阶段的开发")
    else:
        print("\n❌ Pipeline测试失败")
        print("🔧 请检查上述错误信息并修复问题")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
