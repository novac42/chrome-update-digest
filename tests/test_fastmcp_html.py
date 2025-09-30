#!/usr/bin/env python3
"""
测试FastMCP服务器中的webplatform_digest_html工具
"""

import pytest

import asyncio
import json
from pathlib import Path
import sys

# 添加当前目录到路径
sys.path.append('.')

@pytest.mark.asyncio
async def test_merged_digest_html():
    """测试merged_digest_html工具（不依赖FastMCP，直接测试逻辑）"""
    
    print("🧪 测试 merged_digest_html 工具逻辑...")
    
    try:
        # 导入必要的模块
        from src.convert_md2html import ChromeDigestConverter
        from datetime import datetime
        
        BASE_PATH = Path('.')
        version = 138
        channel = "stable"
        output_dir = "digest_html"
        
        # 定义输出文件路径
        output_path = BASE_PATH / output_dir / f"chrome-{version}-merged-digest-{channel}.html"
        
        # 读取已生成的digest文件
        enterprise_path = BASE_PATH / "digest_markdown" / "enterprise" / f"digest-chrome-{version}-enterprise.md"
        webplatform_path = BASE_PATH / "digest_markdown" / "webplatform" / f"digest-chrome-{version}-webplatform-{channel}.md"
        
        print(f"[DIR] 检查enterprise文件: {enterprise_path}")
        print(f"   存在: {enterprise_path.exists()}")
        
        print(f"[DIR] 检查webplatform文件: {webplatform_path}")
        print(f"   存在: {webplatform_path.exists()}")
        
        if not enterprise_path.exists() or not webplatform_path.exists():
            print("❌ 缺少必要的digest文件")
            return False
        
        # 读取digest内容
        print("📖 读取digest内容...")
        with open(enterprise_path, 'r', encoding='utf-8') as f:
            enterprise_content = f.read()
        
        with open(webplatform_path, 'r', encoding='utf-8') as f:
            webplatform_content = f.read()
        
        print(f"   Enterprise内容长度: {len(enterprise_content)} 字符")
        print(f"   WebPlatform内容长度: {len(webplatform_content)} 字符")
        
        # 使用ChromeDigestConverter处理内容
        print("🔄 使用ChromeDigestConverter处理内容...")
        converter = ChromeDigestConverter()
        
        # 解析企业版章节
        enterprise_chapters = converter.parse_chapters(enterprise_content)
        print(f"   Enterprise章节数: {len(enterprise_chapters)}")
        for chapter_title in enterprise_chapters.keys():
            print(f"     - {chapter_title}")
        
        enterprise_html_chapters = {}
        for chapter_title, chapter_content in enterprise_chapters.items():
            enterprise_html_chapters[chapter_title] = converter.process_content(chapter_content)
        
        # 解析web平台章节
        webplatform_chapters = converter.parse_chapters(webplatform_content)
        print(f"   WebPlatform章节数: {len(webplatform_chapters)}")
        for chapter_title in webplatform_chapters.keys():
            print(f"     - {chapter_title}")
        
        webplatform_html_chapters = {}
        for chapter_title, chapter_content in webplatform_chapters.items():
            webplatform_html_chapters[chapter_title] = converter.process_content(chapter_content)
        
        # 渲染章节为HTML
        def render_sections(chapters):
            html_parts = []
            for chapter_title, chapter_content in chapters.items():
                html_parts.append(f'<div class="section">')
                html_parts.append(f'<h2>{chapter_title}</h2>')
                html_parts.append(chapter_content)
                html_parts.append('</div>')
            return '\n'.join(html_parts)
        
        enterprise_html = render_sections(enterprise_html_chapters)
        webplatform_html = render_sections(webplatform_html_chapters)
        
        print(f"   Enterprise HTML长度: {len(enterprise_html)} 字符")
        print(f"   WebPlatform HTML长度: {len(webplatform_html)} 字符")
        
        # 准备版本数据
        enterprise_version_data = [{
            'version': str(version),
            'channel': channel,
            'digest_type': 'enterprise',
            'html_content': enterprise_html
        }]
        
        webplatform_version_data = [{
            'version': str(version),
            'channel': channel,
            'digest_type': 'webplatform',
            'html_content': webplatform_html
        }]
        
        # 尝试使用模板渲染
        print("🎨 尝试使用模板渲染...")
        try:
            template = converter.template_env.get_template('digest_combined.html')
            html_content = template.render(
                webplatform_versions=webplatform_version_data,
                enterprise_versions=enterprise_version_data,
                webplatform_total=1,
                enterprise_total=1,
                generated_at=datetime.now()
            )
            print("   ✅ 模板渲染成功")
        except Exception as template_error:
            print(f"   ⚠️ 模板渲染失败: {template_error}")
            print("   🔄 使用fallback HTML...")
            # 使用简单的fallback HTML
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrome {version} {channel.title()} - Merged Digest</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .tabs {{ display: flex; margin-bottom: 20px; }}
        .tab {{ padding: 10px 20px; cursor: pointer; background: #f0f0f0; margin-right: 10px; }}
        .tab.active {{ background: #007acc; color: white; }}
        .content {{ display: none; }}
        .content.active {{ display: block; }}
        .section {{ margin-bottom: 30px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #007acc; border-bottom: 2px solid #007acc; padding-bottom: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Chrome {version} {channel.title()} - Merged Digest</h1>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('enterprise')">🏢 Enterprise</div>
            <div class="tab" onclick="switchTab('webplatform')">🌐 Web Platform</div>
        </div>
        
        <div id="enterprise" class="content active">
            {enterprise_html}
        </div>
        
        <div id="webplatform" class="content">
            {webplatform_html}
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {{
            // Hide all content
            document.querySelectorAll('.content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
            
            // Show selected content
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>"""
        
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存HTML文件
        print(f"💾 保存HTML文件到: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✅ HTML文件大小: {len(html_content)} 字符")
        print(f"   ✅ 文件已保存: {output_path}")
        
        # 验证文件是否正确创建
        if output_path.exists():
            file_size = output_path.stat().st_size
            print(f"   ✅ 文件验证成功，大小: {file_size} bytes")
            return True
        else:
            print("   ❌ 文件创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 FastMCP HTML工具测试")
    print("=" * 50)
    
    success = await test_merged_digest_html()
    
    print("=" * 50)
    if success:
        print("✅ 所有测试通过!")
    else:
        print("❌ 测试失败!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
