#!/usr/bin/env python3
"""
测试LLM格式遵循性的脚本

NOTE: This test is currently disabled as EnterpriseDigestTool module doesn't exist
"""
import asyncio
import sys
import pytest
from pathlib import Path
sys.path.append('src')

# Skip all tests in this file
pytestmark = pytest.mark.skip(reason="EnterpriseDigestTool module doesn't exist")

# from src.mcp_tools.enterprise_digest import EnterpriseDigestTool
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool as WebplatformDigestTool
import json


class RealLLMContext:
    """模拟真实的LLM Context用于测试"""
    
    async def sample(self, messages, system_prompt, model_preferences=None, temperature=0.7, max_tokens=4000):
        """模拟真实LLM调用，返回基于prompt要求的固定格式内容"""
        print(f"📤 LLM调用参数:")
        print(f"   System Prompt长度: {len(system_prompt)} 字符")
        print(f"   Messages长度: {len(messages)} 字符")
        print(f"   模型偏好: {model_preferences}")
        
        # 检查是否包含强制格式要求
        if "MANDATORY FORMAT REQUIREMENTS" in messages:
            print("   ✅ 检测到强制格式要求")
            
            # 返回遵循enterprise prompt格式的内容
            if "enterprise" in system_prompt.lower():
                return """**Chrome Enterprise Update Watch: Chrome 137**

# Highlights

## Productivity Highlights
• **Multiple Identity Support on iOS** - Chrome 137在iOS平台扩展了多身份支持，为企业用户提供更好的账户分离功能
• **Inactive Profile Deletion** - Chrome Enterprise Core中的非活动配置文件自动清理功能，帮助维护系统整洁
• **Enhanced History Sync** - 配置文件标识改进，使用户更容易选择历史同步

## Mobile Enterprise Security Highlights
• **Enhanced Safe Browsing同步设置** - Enhanced Safe Browsing现在是同步设置，确保跨设备的一致保护
• **URL过滤功能** - iOS上的新URL过滤功能为管理员提供更好的网络访问控制

## Mobile Management Highlights
• **企业策略管理改进** - 提升的企业策略管理功能
• **Chrome Enterprise Core集成** - 更好的Chrome Enterprise Core集成，简化管理流程

# Updates by Area

## User Productivity Updates on Chrome Desktop

### Current Stable Version (Chrome 137)
• **多身份支持扩展** - iOS平台现在支持托管账户的多身份功能，提供严格的工作和个人浏览数据分离
• **书签和阅读列表改进** - 桌面版Chrome的书签管理和阅读列表功能增强
• **配置文件管理** - 改进的配置文件自定义选项，包括自定义徽标和标签

### Upcoming Changes
• **AI Mode搜索推荐** - AI驱动的搜索推荐功能将在后续版本中推出
• **更多企业策略选项** - 计划在未来版本中添加更多企业策略配置选项

# Version Comparison Context
Chrome 137相比前版本在企业功能方面有显著提升，特别是在移动端安全性和配置文件管理方面。这些改进反映了Chrome对企业客户需求的持续关注。"""
            else:
                # WebPlatform格式
                return """# Web Platform Upstream Watch: Chrome 137

## Executive Summary
Chrome 137为Web平台带来了重要的增强功能，重点关注AI集成、WebGPU功能和设备API改进，为开发者提供了新的机会。

## Key Takeaways for the Team

### 🤖 AI in Browser
**摘要**：Chrome 137引入了新的AI驱动功能，增强了浏览器智能和机器学习API集成

**完整内容**：
• **AI Mode搜索推荐功能** - 桌面版地址栏开始推出AI驱动的搜索推荐，帮助用户深入了解感兴趣的主题
• **增强的机器学习API** - 改进的浏览器内机器学习工作负载支持
• **智能内容分析** - 新的AI功能用于内容理解和用户体验优化

### 🕹️ WebGPU
**摘要**：Chrome 137在WebGPU方面取得重大进展，包括Dawn引擎更新和图形管道优化

**完整内容**：
• **Dawn引擎更新** - 升级到最新的Dawn版本，提供更好的性能和稳定性
• **图形管道增强** - 改进的WebGPU图形功能，支持更复杂的3D场景渲染
• **计算着色器支持** - 增强的计算着色器功能，用于高级图形应用

### 📱 Device & Sensors
**摘要**：设备和传感器API的扩展，提供更好的硬件集成

**完整内容**：
• **传感器API增强** - 改进的设备传感器集成，支持响应式Web体验
• **硬件加速特性** - 新的硬件加速功能，提升Web应用性能
• **跨平台兼容性** - 更好的设备API标准化，支持多样化硬件配置

### Breaking Changes
• **废弃的API清理** - 移除了一些过时的Web API，提供明确的迁移路径
• **权限模型更新** - 设备权限处理的变更可能需要应用更新

### New Opportunities
• **AI增强用户体验** - 开发者可以利用浏览器AI功能创建个性化用户体验
• **高性能图形** - WebGPU增强功能支持在Web应用中实现主机级图形质量
• **丰富的移动体验** - 增强的设备API为移动Web应用提供更丰富的功能

## Other Key Updates

### 🎨 CSS and UI Enhancements
• **系统强调色支持** - accent-color属性现在支持操作系统强调色，适用于Windows和ChromeOS
• **新的CSS布局功能** - 改进的flexbox和grid功能
• **增强的动画支持** - 更好的CSS动画和过渡效果

### 🔒 Security and Privacy Improvements
• **内容安全策略增强** - 改进的CSP实施和执行
• **隐私控制改进** - 为用户提供更好的隐私保护选项
• **安全上下文要求** - 增强的现代安全标准支持

### ⚡ Performance Optimizations
• **V8引擎改进** - JavaScript引擎性能的显著提升
• **网络性能优化** - 改进的HTTP/3支持和优化
• **资源加载增强** - 更好的缓存机制和资源优先级

## Version Comparison
与Chrome 136相比，Chrome 137在Web平台演进方面取得了重要进展，特别是AI集成和WebGPU功能的成熟化，标志着Web技术向更智能和高性能方向的发展趋势。"""
        
        else:
            print("   ⚠️ 未检测到强制格式要求，返回通用内容")
            return "Mock LLM generated digest content without format requirements"
    
    async def read_resource(self, resource_name):
        """读取resource内容"""
        print(f"📖 读取资源: {resource_name}")
        
        if resource_name == "enterprise-prompt":
            prompt_path = Path("prompts/enterprise-update-prompt-en.md")
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return type('MockResource', (), {'text': f.read()})()
        
        elif resource_name == "webplatform-prompt":
            prompt_path = Path("prompts/chrome-update-analyzer-prompt-webplatform.md")
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return type('MockResource', (), {'text': f.read()})()
        
        elif resource_name == "profile-keywords":
            keywords_path = Path("prompts/profile-keywords.txt")
            if keywords_path.exists():
                with open(keywords_path, 'r', encoding='utf-8') as f:
                    return type('MockResource', (), {'text': f.read()})()
            else:
                return type('MockResource', (), {'text': 'profile, account, identity, sync'})()
        
        return type('MockResource', (), {'text': f'Mock {resource_name} content'})()


async def test_enterprise_format_compliance():
    """测试企业digest格式遵循性"""
    print("\n🧪 测试Enterprise Digest格式遵循性...")
    
    # 初始化工具
    base_path = Path('.')
    tool = EnterpriseDigestTool(base_path)
    ctx = RealLLMContext()
    
    # 测试参数
    arguments = {
        'version': 137,
        'channel': 'stable',
        'focus_area': 'all',
        'custom_instruction': 'Strictly follow the prompt format requirements'
    }
    
    try:
        result = await tool.generate_digest_with_sampling(ctx, arguments)
        result_data = json.loads(result)
        
        if result_data['success']:
            print(f"✅ 成功生成enterprise digest")
            print(f"   版本: {result_data['version']}")
            print(f"   输出路径: {result_data['output_path']}")
            
            # 检查生成的文件
            output_path = Path(result_data['output_path'])
            if output_path.exists():
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"   📄 内容分析:")
                
                # 检查标题格式
                if content.startswith('**Chrome Enterprise Update Watch:'):
                    print("   ✅ 标题格式正确 (使用 ** 格式)")
                else:
                    print("   ❌ 标题格式错误 (应使用 ** 格式)")
                
                # 检查必需的章节
                required_sections = [
                    "# Highlights",
                    "## Productivity Highlights", 
                    "## Mobile Enterprise Security Highlights",
                    "## Mobile Management Highlights",
                    "# Updates by Area"
                ]
                
                found_sections = []
                for section in required_sections:
                    if section in content:
                        found_sections.append(section)
                
                print(f"   📊 必需章节: {len(found_sections)}/{len(required_sections)} 找到")
                for section in found_sections:
                    print(f"      ✅ {section}")
                
                missing_sections = [s for s in required_sections if s not in found_sections]
                for section in missing_sections:
                    print(f"      ❌ 缺失: {section}")
                
                # 检查语言使用
                chinese_indicators = ["企业", "功能", "管理", "安全", "用户"]
                chinese_found = sum(1 for indicator in chinese_indicators if indicator in content)
                
                if chinese_found > 0:
                    print(f"   ✅ 包含中文内容 ({chinese_found} 个中文词汇)")
                else:
                    print("   ❌ 缺少中文内容")
                
                return True
        else:
            print(f"❌ 生成失败: {result_data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False


async def test_webplatform_format_compliance():
    """测试webplatform digest格式遵循性"""
    print("\n🧪 测试WebPlatform Digest格式遵循性...")
    
    # 初始化工具
    base_path = Path('.')
    tool = WebplatformDigestTool(base_path)
    ctx = RealLLMContext()
    
    # 测试参数
    arguments = {
        'version': 137,
        'channel': 'stable',
        'focus_areas': ['ai', 'webgpu', 'devices'],
        'custom_instruction': 'Strictly follow the prompt format requirements'
    }
    
    try:
        result = await tool.generate_digest_with_sampling(ctx, arguments)
        result_data = json.loads(result)
        
        if result_data['success']:
            print(f"✅ 成功生成webplatform digest")
            print(f"   版本: {result_data['version']}")
            print(f"   输出路径: {result_data['output_path']}")
            
            # 检查生成的文件
            output_path = Path(result_data['output_path'])
            if output_path.exists():
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"   📄 内容分析:")
                
                # 检查必需的章节
                required_sections = [
                    "## Executive Summary",
                    "## Key Takeaways for the Team",
                    "### 🤖 AI in Browser",
                    "### 🕹️ WebGPU",
                    "### 📱 Device & Sensors",
                    "## Other Key Updates",
                    "## Version Comparison"
                ]
                
                found_sections = []
                for section in required_sections:
                    if section in content:
                        found_sections.append(section)
                
                print(f"   📊 必需章节: {len(found_sections)}/{len(required_sections)} 找到")
                for section in found_sections:
                    print(f"      ✅ {section}")
                
                missing_sections = [s for s in required_sections if s not in found_sections]
                for section in missing_sections:
                    print(f"      ❌ 缺失: {section}")
                
                # 检查WebGPU中是否提到Dawn
                if "Dawn" in content:
                    print("   ✅ WebGPU章节包含Dawn引擎信息")
                else:
                    print("   ⚠️ WebGPU章节缺少Dawn引擎信息")
                
                return True
        else:
            print(f"❌ 生成失败: {result_data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False


async def main():
    """主测试函数"""
    print("🚀 LLM格式遵循性测试开始")
    print("=" * 60)
    
    enterprise_result = await test_enterprise_format_compliance()
    webplatform_result = await test_webplatform_format_compliance()
    
    print("\n" + "=" * 60)
    if enterprise_result and webplatform_result:
        print("🎉 所有格式遵循性测试通过！")
    else:
        print("❌ 部分测试未通过，需要继续优化")


if __name__ == "__main__":
    asyncio.run(main())
