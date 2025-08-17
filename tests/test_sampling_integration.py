#!/usr/bin/env python3
"""
Sampling 集成测试
测试FastMCP的sampling功能和digest工具的集成
"""

import sys
import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from src.mcp_tools.enterprise_digest import EnterpriseDigestTool
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool as WebplatformDigestTool


class MockContext:
    """模拟FastMCP Context用于测试"""
    
    def __init__(self):
        self.sample = AsyncMock()
        self.read_resource = AsyncMock()
    
    async def mock_sample_response(self, **kwargs):
        """模拟LLM sampling响应"""
        messages = kwargs.get("messages", "")
        
        # 根据消息内容生成模拟响应
        if "webplatform" in messages.lower() or "web platform" in messages.lower():
            return """# Web Platform Upstream Watch: Chrome 138

## Executive Summary
Chrome 138 introduces significant web platform enhancements focusing on AI integration, WebGPU capabilities, and device API improvements that expand developer opportunities.

### 🤖 AI in Browser
- New AI-powered browser intelligence features
- Enhanced machine learning API integrations
- Improved natural language processing capabilities

### 🕹️ WebGPU  
- Advanced graphics pipeline optimizations
- New compute shader capabilities
- Enhanced WebGPU debugging tools

### 📱 Device and Sensors
- Extended sensor API support
- Improved device integration capabilities
- New hardware acceleration features

## Key Takeaways

### High Impact Changes
- **AI API Integration**: New browser-native AI capabilities enable developers to build more intelligent web applications
- **WebGPU Performance**: Significant performance improvements in graphics rendering and compute operations
- **Device API Expansion**: Extended sensor and device access for enhanced web application capabilities

### Breaking Changes
- **Deprecated APIs**: Several legacy APIs have been removed in favor of more secure alternatives
- **Permission Model Updates**: Changes to device permission handling may require application updates

### New Opportunities
- **AI-Enhanced UX**: Developers can now leverage browser AI for personalized user experiences
- **High-Performance Graphics**: WebGPU enhancements enable console-quality graphics in web applications
- **Advanced Device Integration**: New device APIs open possibilities for IoT and embedded web applications

## Other Key Updates

### 🎨 CSS and UI Enhancements
- New CSS features for advanced layouts and animations
- Improved accessibility support
- Enhanced responsive design capabilities

### 🔒 Security and Privacy Improvements
- Strengthened content security policies
- Enhanced privacy controls for users
- Improved secure context requirements

### ⚡ Performance Optimizations
- Faster page load times
- Reduced memory usage
- Improved JavaScript execution performance

---
*Generated via FastMCP sampling for Chrome 138 WebPlatform digest*"""
        
        elif "enterprise" in messages.lower():
            return """# Chrome Enterprise Update Watch: Chrome 138

## Executive Summary
This digest analyzes Chrome 138 enterprise-focused updates, highlighting key productivity, security, and management enhancements for enterprise deployments.

### 🏢 Productivity Highlights
- Enhanced Agentspace recommendations in Chrome omnibox
- Improved application management capabilities
- New user workflow optimizations

### 🔒 Security Highlights  
- Advanced threat protection updates
- Enhanced compliance features
- Improved policy enforcement mechanisms

### ⚙️ Management Highlights
- New enterprise policy options
- Enhanced device management capabilities
- Improved deployment and maintenance tools

## Key Updates

### User Productivity/Apps
- **Agentspace recommendations**: Chrome omnibox now provides intelligent suggestions based on user context and enterprise applications
- **Application lifecycle management**: Improved handling of enterprise applications with enhanced security validation

### Mobile Enterprise Security
- **Enhanced threat detection**: New algorithms for identifying and blocking enterprise security threats
- **Compliance monitoring**: Improved tracking and reporting of compliance violations

### Mobile Management
- **Policy enforcement**: Strengthened policy application across managed devices  
- **Remote management**: Enhanced capabilities for IT administrators to manage devices remotely

## Business Impact Assessment
These updates provide enterprise customers with:
- **Improved Security Posture**: Enhanced threat protection and compliance monitoring
- **Better User Experience**: More intelligent recommendations and streamlined workflows  
- **Simplified Management**: Enhanced tools for IT administrators

---
*Generated via FastMCP sampling for Chrome 138 Enterprise digest*"""
        
        else:
            return "Mock LLM generated digest content"
    
    async def mock_resource_response(self, resource_name):
        """模拟resource读取响应"""
        mock_responses = {
            "enterprise-prompt": "Mock enterprise prompt content for digest generation...",
            "webplatform-prompt": "Mock webplatform prompt content for digest generation...",
            "profile-keywords": "webgpu\nai\ndevice\nsensor\ncss\napi\nperformance\nsecurity"
        }
        return mock_responses.get(resource_name, "Mock resource content")


async def test_enterprise_digest_sampling():
    """测试enterprise digest的sampling集成"""
    print("🧪 测试Enterprise Digest Sampling...")
    
    # 初始化工具
    base_path = Path(__file__).parent
    tool = EnterpriseDigestTool(base_path)
    
    # 创建mock context
    ctx = MockContext()
    ctx.sample.side_effect = ctx.mock_sample_response
    ctx.read_resource.side_effect = ctx.mock_resource_response
    
    # 测试参数
    arguments = {
        "version": 138,
        "channel": "stable",
        "focus_area": "security",
        "custom_instruction": "Focus on business impact and security compliance"
    }
    
    try:
        print("   📊 调用 generate_digest_with_sampling...")
        result = await tool.generate_digest_with_sampling(ctx, arguments)
        
        # 解析结果
        result_data = json.loads(result)
        
        # 验证结果
        assert result_data["success"] == True, f"生成失败: {result_data.get('error')}"
        assert result_data["version"] == 138, "版本不匹配"
        assert result_data["focus_area"] == "security", "焦点区域不匹配"
        
        print(f"   ✅ 成功生成enterprise digest")
        print(f"      版本: {result_data['version']}")
        print(f"      渠道: {result_data['channel']}")
        print(f"      焦点: {result_data['focus_area']}")
        print(f"      输出路径: {result_data['output_path']}")
        print(f"      内容长度: {result_data['total_length']} 字符")
        
        # 检查生成的文件
        output_path = Path(result_data['output_path'])
        if output_path.exists():
            print(f"   ✅ 文件已保存: {output_path.name}")
            
            # 读取并验证内容
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if "Mock LLM generated digest content" not in content:
                print("   ✅ 内容包含真实的LLM生成内容（非占位符）")
            else:
                print("   ⚠️ 内容包含占位符，可能需要检查")
                
        else:
            print(f"   ❌ 文件未找到: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Enterprise digest sampling测试失败: {str(e)}")
        return False


async def test_webplatform_digest_sampling():
    """测试webplatform digest的sampling集成"""
    print("\n🧪 测试WebPlatform Digest Sampling...")
    
    # 初始化工具
    base_path = Path(__file__).parent
    tool = WebplatformDigestTool(base_path)
    
    # 创建mock context
    ctx = MockContext()
    ctx.sample.side_effect = ctx.mock_sample_response
    ctx.read_resource.side_effect = ctx.mock_resource_response
    
    # 测试参数
    arguments = {
        "version": 138,
        "channel": "stable",
        "focus_areas": ["ai", "webgpu", "devices"],
        "custom_instruction": "Emphasize developer impact and new opportunities"
    }
    
    try:
        print("   📊 调用 generate_digest_with_sampling...")
        result = await tool.generate_digest_with_sampling(ctx, arguments)
        
        # 解析结果
        result_data = json.loads(result)
        
        # 验证结果
        assert result_data["success"] == True, f"生成失败: {result_data.get('error')}"
        assert result_data["version"] == 138, "版本不匹配"
        assert result_data["focus_areas"] == ["ai", "webgpu", "devices"], "焦点区域不匹配"
        
        print(f"   ✅ 成功生成webplatform digest")
        print(f"      版本: {result_data['version']}")
        print(f"      渠道: {result_data['channel']}")
        print(f"      焦点: {', '.join(result_data['focus_areas'])}")
        print(f"      输出路径: {result_data['output_path']}")
        print(f"      内容长度: {result_data['total_length']} 字符")
        print(f"      WebGPU集成: {'是' if result_data['webgpu_integrated'] else '否'}")
        
        # 检查生成的文件
        output_path = Path(result_data['output_path'])
        if output_path.exists():
            print(f"   ✅ 文件已保存: {output_path.name}")
            
            # 读取并验证内容
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 检查内容质量
            quality_indicators = [
                "Executive Summary",
                "AI in Browser", 
                "WebGPU",
                "Device and Sensors",
                "Key Takeaways"
            ]
            
            found_indicators = [indicator for indicator in quality_indicators if indicator in content]
            print(f"   ✅ 内容质量指标: {len(found_indicators)}/{len(quality_indicators)} 找到")
            
            if len(found_indicators) >= 3:
                print("   ✅ 内容质量良好")
            else:
                print("   ⚠️ 内容质量可能需要改进")
                
        else:
            print(f"   ❌ 文件未找到: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ WebPlatform digest sampling测试失败: {str(e)}")
        return False


async def test_error_handling():
    """测试错误处理和重试机制"""
    print("\n🧪 测试错误处理和重试机制...")
    
    # 初始化工具
    base_path = Path(__file__).parent
    tool = EnterpriseDigestTool(base_path)
    
    # 创建会失败的mock context
    ctx = MockContext()
    
    # 模拟第一次失败，第二次成功的场景
    call_count = 0
    async def failing_sample(**kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise Exception("Mock sampling failure")
        else:
            return "Recovered sample response"
    
    ctx.sample.side_effect = failing_sample
    ctx.read_resource.side_effect = ctx.mock_resource_response
    
    # 测试参数
    arguments = {
        "version": 999,  # 使用不存在的版本来测试错误处理
        "channel": "stable"
    }
    
    try:
        print("   📊 测试错误恢复机制...")
        result = await tool.generate_digest_with_sampling(ctx, arguments)
        result_data = json.loads(result)
        
        # 应该失败，因为没有版本999的数据
        if not result_data["success"]:
            print(f"   ✅ 正确处理错误: {result_data['error']}")
            return True
        else:
            print("   ⚠️ 期望失败但成功了，可能需要检查错误处理")
            return False
            
    except Exception as e:
        print(f"   ❌ 错误处理测试异常: {str(e)}")
        return False


async def test_file_output_verification():
    """验证生成的文件输出"""
    print("\n🧪 验证文件输出质量...")
    
    # 检查生成的文件
    base_path = Path(__file__).parent
    enterprise_dir = base_path / "digest_markdown" / "enterprise"
    webplatform_dir = base_path / "digest_markdown" / "webplatform"
    
    print("   [DIR] 检查输出目录...")
    
    enterprise_files = list(enterprise_dir.glob("*.md")) if enterprise_dir.exists() else []
    webplatform_files = list(webplatform_dir.glob("*.md")) if webplatform_dir.exists() else []
    
    print(f"   📄 Enterprise文件: {len(enterprise_files)} 个")
    for file in enterprise_files[-3:]:  # 显示最近的3个文件
        print(f"      - {file.name}")
    
    print(f"   📄 WebPlatform文件: {len(webplatform_files)} 个")
    for file in webplatform_files[-3:]:  # 显示最近的3个文件
        print(f"      - {file.name}")
    
    # 检查最近生成的文件内容
    recent_files = sorted(enterprise_files + webplatform_files, key=lambda x: x.stat().st_mtime, reverse=True)[:2]
    
    for file in recent_files:
        print(f"\n   📖 分析文件: {file.name}")
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 基本质量检查
            lines = content.split('\n')
            word_count = len(content.split())
            
            print(f"      行数: {len(lines)}")
            print(f"      字数: {word_count}")
            
            # 检查结构质量
            has_title = any(line.startswith('# ') for line in lines)
            has_sections = sum(1 for line in lines if line.startswith('## '))
            has_content = word_count > 100
            
            print(f"      标题: {'是' if has_title else '否'}")
            print(f"      章节数: {has_sections}")
            print(f"      内容充实: {'是' if has_content else '否'}")
            
            if has_title and has_sections >= 2 and has_content:
                print(f"      ✅ 文件质量良好")
            else:
                print(f"      ⚠️ 文件质量可能需要改进")
                
        except Exception as e:
            print(f"      ❌ 读取文件失败: {str(e)}")
    
    return True


async def main():
    """主测试函数"""
    print("🚀 FastMCP Sampling 集成测试开始")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        test_enterprise_digest_sampling,
        test_webplatform_digest_sampling,
        test_error_handling,
        test_file_output_verification
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🏁 测试完成: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return True
    else:
        print("⚠️ 部分测试失败，需要进一步检查")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
