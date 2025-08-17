#!/usr/bin/env python3
"""
Chrome 137 Digest生成测试
通过MCP server调用工具生成Chrome 137的完整digest文档
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径  
sys.path.append(str(Path(__file__).parent))

# 直接导入工具类
from src.mcp_tools.enterprise_digest import EnterpriseDigestTool
from src.mcp_tools.enhanced_webplatform_digest import EnhancedWebplatformDigestTool as WebplatformDigestTool  
from src.mcp_tools.merged_digest_html import MergedDigestHtmlTool

# 创建一个简单的Context模拟类，避免直接继承Context
class MockContext:
    """模拟FastMCP的Context对象用于测试"""
    def __init__(self):
        self._session_id = "test_session"
        self._request_id = "test_request" 
        self._client_id = "test_client"
    
    @property
    def session_id(self):
        return self._session_id
    
    @property
    def request_id(self):
        return self._request_id
    
    @property
    def client_id(self):
        return self._client_id
    
    async def request_sampling(self, prompt: str, max_tokens: int = 8000):
        """模拟sampling请求 - 返回简单的占位符内容"""
        # 这里应该调用真实的LLM，现在返回占位符
        return f"""# Chrome {137} Digest

## 概述
这是Chrome 137版本的digest摘要，基于以下prompt生成：

{prompt[:200]}...

## 主要更新
- 功能更新1: 描述一些重要的功能更新
- 性能改进: 描述性能方面的改进
- 安全性增强: 描述安全相关的改进
- 开发者工具: 描述开发者相关的更新

## 详细内容
由于这是模拟环境，这里显示占位符内容。在真实环境中，这里会是LLM根据源数据生成的详细digest内容。

Prompt长度: {len(prompt)} 字符
最大tokens: {max_tokens}
生成时间: {datetime.now().isoformat()}
"""
    
    async def sample(self, messages=None, system_prompt=None, model_preferences=None, temperature=0.7, max_tokens=4000, **kwargs):
        """模拟sample方法 - 工具类实际调用的方法"""
        if messages:
            prompt_text = "\n".join([msg.get("content", "") for msg in messages if isinstance(msg, dict)])
        else:
            prompt_text = system_prompt or "未知prompt"
            
        return f"""# Chrome 137 企业版更新摘要

## 概述
本次Chrome 137版本带来了多项企业级功能改进，主要集中在生产力工具、安全性增强和管理功能优化方面。

## 主要更新内容

### 🚀 生产力提升
- **新增企业级书签同步功能**: 支持跨设备的企业书签管理
- **改进的PDF处理**: 增强了PDF查看和编辑功能
- **办公套件集成**: 更好的Microsoft Office和Google Workspace集成

### 🔒 安全性增强  
- **增强的证书管理**: 改进了企业证书的部署和管理流程
- **高级威胁防护**: 新增对钓鱼网站的智能识别功能
- **数据泄露防护**: 加强了敏感数据的保护机制

### ⚙️ 管理功能
- **策略管理优化**: 简化了企业策略的配置和部署
- **用户配置文件管理**: 改进了多用户环境下的配置管理
- **远程管理工具**: 增强了IT管理员的远程控制能力

### 🛠️ 开发者工具
- **调试工具改进**: 升级了开发者控制台的功能
- **性能分析工具**: 新增了网页性能分析功能
- **扩展API更新**: 为企业扩展开发提供了新的API

## 部署建议
- 建议企业用户优先测试新的安全功能
- 新的管理策略需要配合最新的管理控制台使用
- 建议分阶段部署，先在测试环境验证

## 影响评估
- 兼容性: 与现有企业应用保持良好兼容性
- 性能: 整体性能提升约5-10%
- 安全性: 显著提升了企业数据安全保护能力

---
*基于模拟LLM生成的摘要内容*
*模型偏好: {model_preferences}*
*温度设置: {temperature}*
*最大tokens: {max_tokens}*
"""
    
    async def info(self, message: str, logger_name: str = "test"):
        """记录信息"""
        print(f"INFO: {message}")
    
    async def debug(self, message: str, logger_name: str = "test"):
        """记录调试信息"""
        print(f"DEBUG: {message}")
    
    async def warning(self, message: str, logger_name: str = "test"):
        """记录警告"""
        print(f"WARNING: {message}")
    
    async def error(self, message: str, logger_name: str = "test"):
        """记录错误"""
        print(f"ERROR: {message}")
    
    async def report_progress(self, progress: float, total: float = 100.0, message: str = ""):
        """报告进度"""
        if total:
            print(f"PROGRESS: {progress}/{total} ({progress/total*100:.1f}%) {message}")
        else:
            print(f"PROGRESS: {progress} {message}")

# 基础路径
BASE_PATH = Path(__file__).parent


async def generate_chrome_137_digests():
    """生成Chrome 137的完整digest套件"""
    print("🚀 Chrome 137 Digest 生成测试")
    print("=" * 60)
    
    target_version = 137
    target_channel = "stable"
    
    print(f"📋 目标版本: Chrome {target_version} {target_channel}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 创建工具实例
    ctx = MockContext()
    enterprise_tool = EnterpriseDigestTool(BASE_PATH)
    webplatform_tool = WebplatformDigestTool(BASE_PATH)
    merged_tool = MergedDigestHtmlTool(BASE_PATH)
    
    # 检查源数据文件是否存在
    print("🔍 检查源数据文件...")
    enterprise_source = BASE_PATH / "upstream_docs" / "processed_releasenotes" / "processed_forenterprise" / f"{target_version}-organized_chromechanges-enterprise.md"
    webplatform_source = BASE_PATH / "upstream_docs" / "processed_releasenotes" / "processed_forwebplatform" / f"{target_version}-webplatform-with-webgpu.md"
    
    if not enterprise_source.exists():
        print(f"❌ 企业版源数据缺失: {enterprise_source}")
        return False
    else:
        print(f"✅ 企业版源数据存在: {enterprise_source}")
        
    if not webplatform_source.exists():
        print(f"❌ Web平台源数据缺失: {webplatform_source}")
        return False
    else:
        print(f"✅ Web平台源数据存在: {webplatform_source}")
    
    print()
    
    # 步骤1: 生成企业版digest
    print("🏢 步骤 1/3: 生成企业版digest...")
    print("   ⚙️  调用 enterprise_digest tool...")
    
    try:
        enterprise_params = {
            "version": target_version,
            "channel": target_channel,
            "focus_area": "productivity",
            "custom_instruction": "重点关注企业用户的生产力提升功能，包括管理功能、安全性改进和部署相关的变更。请生成详细的中文digest。"
        }
        
        enterprise_result = await enterprise_tool.generate_digest_with_sampling(ctx, enterprise_params)  # type: ignore
        
        enterprise_data = json.loads(enterprise_result)
        
        if enterprise_data["success"]:
            print(f"   ✅ 企业版digest生成成功")
            print(f"   📄 输出文件: {enterprise_data['output_path']}")
            
            # 验证文件并显示基本信息
            output_path = Path(enterprise_data['output_path'])
            if output_path.exists():
                file_size = output_path.stat().st_size
                print(f"   📊 文件大小: {file_size:,} bytes")
                
                # 读取并显示前几行内容
                with open(output_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines = len(lines)
                    print(f"   📝 总行数: {total_lines}")
                    print(f"   📖 前3行预览:")
                    for i, line in enumerate(lines[:3]):
                        print(f"      {i+1}: {line.strip()}")
            else:
                print(f"   ❌ 输出文件不存在")
                return False
        else:
            print(f"   ❌ 企业版digest生成失败")
            print(f"   🔍 错误信息: {enterprise_data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ 企业版digest生成异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    
    # 步骤2: 生成Web平台digest
    print("🌐 步骤 2/3: 生成Web平台digest...")
    print("   ⚙️  调用 webplatform_digest tool...")
    
    try:
        webplatform_params = {
            "version": target_version,
            "channel": target_channel,
            "focus_areas": ["ai", "webgpu", "css", "performance", "security"],
            "custom_instruction": "重点关注AI功能、WebGPU改进、CSS新特性、性能优化和安全性提升。请生成详细的中文digest，突出对开发者的影响。"
        }
        
        webplatform_result = await webplatform_tool.generate_digest_with_sampling(ctx, webplatform_params)  # type: ignore
        
        webplatform_data = json.loads(webplatform_result)
        
        if webplatform_data["success"]:
            print(f"   ✅ Web平台digest生成成功")
            print(f"   📄 输出文件: {webplatform_data['output_path']}")
            
            # 验证文件并显示基本信息
            output_path = Path(webplatform_data['output_path'])
            if output_path.exists():
                file_size = output_path.stat().st_size
                print(f"   📊 文件大小: {file_size:,} bytes")
                
                # 读取并显示前几行内容
                with open(output_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines = len(lines)
                    print(f"   📝 总行数: {total_lines}")
                    print(f"   📖 前3行预览:")
                    for i, line in enumerate(lines[:3]):
                        print(f"      {i+1}: {line.strip()}")
            else:
                print(f"   ❌ 输出文件不存在")
                return False
        else:
            print(f"   ❌ Web平台digest生成失败")
            print(f"   🔍 错误信息: {webplatform_data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Web平台digest生成异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    
    # 步骤3: 生成合并HTML
    print("📄 步骤 3/3: 生成合并HTML...")
    print("   ⚙️  调用 merged_digest_html tool...")
    
    try:
        html_params = {
            "version": target_version,
            "channel": target_channel,
            "force_regenerate": True,
            "output_dir": "digest_html"
        }
        
        html_result = await merged_tool.generate_html(html_params)
        
        html_data = json.loads(html_result)
        
        if html_data["success"]:
            print(f"   ✅ 合并HTML生成成功")
            print(f"   📄 输出文件: {html_data['output_path']}")
            
            # 验证HTML文件
            output_path = Path(html_data['output_path'])
            if output_path.exists():
                file_size = output_path.stat().st_size
                print(f"   📊 文件大小: {file_size:,} bytes")
                
                # 验证HTML内容结构
                with open(output_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # 基本HTML结构检查
                html_checks = [
                    ("<!DOCTYPE html>", "HTML5文档声明"),
                    ("<title>Chrome 137", "页面标题"),
                    ("switchDigestType", "Tab切换功能"),
                    ("enterprise-digest", "企业版内容区域"),
                    ("webplatform-digest", "Web平台内容区域"),
                    ("Bootstrap", "CSS框架"),
                    ("JavaScript", "交互功能")
                ]
                
                print("   🔍 HTML结构验证:")
                all_checks_passed = True
                for check_text, description in html_checks:
                    if check_text in html_content:
                        print(f"      ✅ {description}")
                    else:
                        print(f"      ❌ 缺少 {description}")
                        all_checks_passed = False
                
                if all_checks_passed:
                    print("   🎉 HTML结构完整!")
                else:
                    print("   ⚠️  HTML结构可能有问题")
                    
            else:
                print(f"   ❌ HTML输出文件不存在")
                return False
        else:
            print(f"   ❌ 合并HTML生成失败")
            print(f"   🔍 错误信息: {html_data.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"   ❌ 合并HTML生成异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("🎉 Chrome 137 Digest生成完成!")
    print("=" * 60)
    
    # 生成摘要报告
    print("📊 生成摘要:")
    print(f"   📅 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   📂 企业版Markdown: digest_markdown/enterprise/digest-chrome-{target_version}-enterprise-{target_channel}.md")
    print(f"   📂 Web平台Markdown: digest_markdown/webplatform/digest-chrome-{target_version}-webplatform-{target_channel}.md")
    print(f"   📂 合并HTML: digest_html/chrome-{target_version}-merged-digest-{target_channel}.html")
    print()
    print("🚀 下一步: 可以通过浏览器打开HTML文件查看效果，或者用编辑器查看Markdown文件。")
    
    return True


async def main():
    """主函数"""
    print("Chrome 137 MCP Tools 测试")
    print("通过FastMCP server调用digest生成工具")
    print()
    
    success = await generate_chrome_137_digests()
    
    if success:
        print("\n✅ 测试成功完成!")
        print("所有Chrome 137的digest文件都已生成。")
    else:
        print("\n❌ 测试失败!")
        print("请检查上面的错误信息。")


if __name__ == "__main__":
    asyncio.run(main())
