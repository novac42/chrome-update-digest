"""
Enhanced WebPlatform Digest Tool with deterministic link extraction.
Uses script-based extraction for 100% link accuracy.
"""

import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

from fastmcp import Context
from src.utils.yaml_pipeline import YAMLPipeline
from src.utils.focus_area_manager import FocusAreaManager


class EnhancedWebplatformDigestTool:
    """
    Enhanced MCP tool for WebPlatform digest generation.
    
    Key improvements:
    1. Deterministic link extraction (100% accuracy)
    2. YAML intermediate format
    3. Focus area filtering
    4. Tag-based organization
    """
    
    def __init__(self, base_path: Path = None):
        """Initialize the enhanced tool."""
        # Use provided base_path or default to current working directory
        if base_path is None:
            base_path = Path.cwd()
        self.base_path = base_path
        
        self.yaml_pipeline = YAMLPipeline()
        self.focus_manager = FocusAreaManager(self.base_path / 'config' / 'focus_areas.yaml')
        # Update cache directory to match new structure
        self.cache_dir = self.base_path / 'upstream_docs' / 'processed_releasenotes' / 'processed_forwebplatform'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # Digest output directory
        self.digest_dir = self.base_path / 'digest_markdown' / 'webplatform'
        self.digest_dir.mkdir(parents=True, exist_ok=True)
    
    async def run(
        self,
        ctx: Context,
        version: str = "138",
        channel: str = "stable",
        focus_areas: Optional[str] = None,
        use_cache: bool = True,
        language: Optional[str] = None,
        split_by_area: bool = False,
        target_area: Optional[str] = None,
        debug: bool = False
    ) -> str:
        """
        Generate WebPlatform digest with enhanced extraction.
        
        Args:
            ctx: FastMCP context
            version: Chrome version
            channel: Release channel
            focus_areas: Comma-separated focus areas (e.g., "ai,webgpu,security")
            use_cache: Whether to use cached YAML if available
            language: Output language ("en", "zh", or None for both)
            split_by_area: Whether to split features by area into separate YAML files
            target_area: Specific area to analyze (e.g., "css", "webapi", "security")
            debug: Enable debug output
            
        Returns:
            Generated digest in markdown format
        """
        try:
            # Parse focus areas
            focus_area_list = []
            if focus_areas:
                focus_area_list = [area.strip() for area in focus_areas.split(',')]
                if debug:
                    print(f"Filtering by focus areas: {focus_area_list}")
            
            # Step 1: Get or generate YAML data
            yaml_data = await self._get_yaml_data(ctx, version, channel, use_cache, split_by_area, target_area, debug)
            
            if not yaml_data:
                return json.dumps({
                    "success": False,
                    "error": f"Could not process release notes for Chrome {version} {channel}",
                    "version": version,
                    "channel": channel
                }, ensure_ascii=False)
            
            # Step 2: Apply focus area filtering if specified
            if focus_area_list:
                yaml_data = self.yaml_pipeline.filter_by_focus_areas(
                    yaml_data, focus_area_list
                )
                if debug:
                    filtered_count = len(yaml_data.get('features', []))
                    print(f"Filtered to {filtered_count} features")
            
            # Step 3: Generate digest from YAML data with language support
            # Default to generating both languages if not specified
            if language is None or language == 'bilingual':
                # Generate both EN and ZH versions
                try:
                    digest_en = await self._generate_digest_from_yaml(ctx, yaml_data, 'en', target_area, debug)
                    digest_path_en = self._get_digest_path(version, channel, target_area, 'en')
                    await self._save_digest(digest_en, digest_path_en, debug)
                    if debug:
                        print(f"English digest saved to: {digest_path_en}")
                except Exception as e:
                    return json.dumps({
                        "success": False,
                        "error": f"Failed to generate English digest: {str(e)}",
                        "version": version,
                        "channel": channel,
                        "language": "en",
                        "target_area": target_area
                    }, ensure_ascii=False)
                
                try:
                    digest_zh = await self._generate_digest_from_yaml(ctx, yaml_data, 'zh', target_area, debug)
                    digest_path_zh = self._get_digest_path(version, channel, target_area, 'zh')
                    await self._save_digest(digest_zh, digest_path_zh, debug)
                    if debug:
                        print(f"Chinese digest saved to: {digest_path_zh}")
                except Exception as e:
                    return json.dumps({
                        "success": False,
                        "error": f"Failed to generate Chinese digest: {str(e)}",
                        "version": version,
                        "channel": channel,
                        "language": "zh",
                        "target_area": target_area
                    }, ensure_ascii=False)
                
                # Return structured success response
                return json.dumps({
                    "success": True,
                    "version": version,
                    "channel": channel,
                    "language": "bilingual",
                    "target_area": target_area,
                    "output_paths": {
                        "en": str(digest_path_en),
                        "zh": str(digest_path_zh)
                    },
                    "content_preview": {
                        "en": digest_en[:300] + "..." if len(digest_en) > 300 else digest_en,
                        "zh": digest_zh[:300] + "..." if len(digest_zh) > 300 else digest_zh
                    },
                    "total_length": {
                        "en": len(digest_en),
                        "zh": len(digest_zh)
                    }
                }, ensure_ascii=False)
            else:
                # Single language mode
                digest = await self._generate_digest_from_yaml(ctx, yaml_data, language, target_area, debug)
                
                # Save digest to file with area-based folder structure
                digest_path = self._get_digest_path(version, channel, target_area, language)
                await self._save_digest(digest, digest_path, debug)
                if debug:
                    print(f"Digest saved to: {digest_path}")
                
                # Return structured success response
                return json.dumps({
                    "success": True,
                    "version": version,
                    "channel": channel,
                    "language": language,
                    "target_area": target_area,
                    "output_path": str(digest_path),
                    "content_preview": digest[:500] + "..." if len(digest) > 500 else digest,
                    "total_length": len(digest)
                }, ensure_ascii=False)
            
        except Exception as e:
            # Return structured error response (aligned with Enterprise)
            return json.dumps({
                "success": False,
                "error": str(e),
                "version": version,
                "channel": channel,
                "language": language,
                "target_area": target_area
            }, ensure_ascii=False)
    
    async def _get_yaml_data(
        self,
        ctx: Context,
        version: str,
        channel: str,
        use_cache: bool,
        split_by_area: bool,
        target_area: Optional[str],
        debug: bool
    ) -> Optional[Dict]:
        """
        Get YAML data from cache or generate it.
        
        Args:
            ctx: FastMCP context
            version: Chrome version
            channel: Release channel
            use_cache: Whether to use cache
            split_by_area: Whether to split by area
            target_area: Specific area to load
            debug: Debug mode
            
        Returns:
            YAML data dictionary or None
        """
        # Check for cached YAML with new folder structure
        if target_area:
            # Normalize area name: 'webgpu' -> 'graphics-webgpu' for consistency
            normalized_area = 'graphics-webgpu' if target_area in ['webgpu', 'graphics-webgpu'] else target_area
            # Area-specific files are in subdirectories
            yaml_path = self.cache_dir / normalized_area / f"chrome-{version}-{channel}.yml"
        else:
            # General tagged file in root directory
            yaml_path = self.cache_dir / f"chrome-{version}-{channel}-tagged.yml"
        
        if use_cache and yaml_path.exists():
            if debug:
                print(f"Using cached YAML: {yaml_path}")
            return self.yaml_pipeline.load_from_yaml(yaml_path)
        
        # Load release notes (with WebGPU merging if target_area is graphics-webgpu)
        release_notes = await self._load_release_notes(ctx, version, channel, debug, target_area)
        if not release_notes:
            return None
        
        # Process through pipeline
        if debug:
            print(f"Processing release notes through YAML pipeline...")
            if split_by_area:
                print(f"Splitting features by area into separate YAML files")
        
        yaml_data = self.yaml_pipeline.process_release_notes(
            markdown_content=release_notes,
            version=version,
            channel=channel,
            save_yaml=True,
            split_by_area=split_by_area
        )
        
        if debug:
            stats = yaml_data.get('statistics', {})
            print(f"Extracted {stats.get('total_features', 0)} features with {stats.get('total_links', 0)} links")
        
        return yaml_data
    
    async def _load_release_notes(
        self,
        ctx: Context,
        version: str,
        channel: str,
        debug: bool,
        target_area: Optional[str] = None
    ) -> Optional[str]:
        """
        Load release notes from resources or file system.
        For graphics-webgpu area, merge Chrome and WebGPU content.
        
        Args:
            ctx: FastMCP context
            version: Chrome version
            channel: Release channel
            debug: Debug mode
            target_area: Specific area being processed
            
        Returns:
            Release notes content or None
        """
        # Load from file system
        # Note: In future, this could be enhanced to use MCP resource system
        base_dir = self.base_path / 'upstream_docs' / 'release_notes' / 'webplatform'
        
        # Try different file patterns
        # For stable channel, also try without channel suffix
        patterns = [
            f"Chrome {version} release note - WebPlatform.md",
            f"chrome-{version}-{channel}.md",
            f"chrome_{version}_{channel}.md"
        ]
        
        # For stable channel, the file might not have "-stable" suffix
        if channel == 'stable':
            patterns.insert(1, f"chrome-{version}.md")
        
        chrome_content = None
        for pattern in patterns:
            file_path = base_dir / pattern
            if file_path.exists():
                if debug:
                    print(f"Loading from file: {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    chrome_content = f.read()
                break
        
        if not chrome_content:
            if debug:
                print(f"No release notes found for Chrome {version} {channel}")
            return None
        
        # If target area is graphics-webgpu, merge with WebGPU content
        if target_area == 'graphics-webgpu' or target_area == 'webgpu':
            webgpu_file = base_dir / f"webgpu-{version}.md"
            if webgpu_file.exists():
                if debug:
                    print(f"Merging WebGPU content from: {webgpu_file}")
                
                with open(webgpu_file, 'r', encoding='utf-8') as f:
                    webgpu_content = f.read()
                
                # Merge WebGPU content into Chrome content
                merged_content = self._merge_webgpu_content(chrome_content, webgpu_content, version)
                return merged_content
            elif debug:
                print(f"No WebGPU file found for version {version}")
        
        return chrome_content
    
    def _merge_webgpu_content(self, chrome_content: str, webgpu_content: str, version: str) -> str:
        """
        Merge WebGPU content with Chrome release notes.
        
        Args:
            chrome_content: Chrome release notes content
            webgpu_content: WebGPU specific content
            version: Chrome version
            
        Returns:
            Merged content
        """
        # Check if Chrome already has WebGPU section
        if '## WebGPU' in chrome_content:
            # Replace existing WebGPU section with detailed one
            lines = chrome_content.split('\n')
            new_lines = []
            skip_section = False
            
            for line in lines:
                if line.startswith('## WebGPU'):
                    skip_section = True
                    # Insert the WebGPU content here
                    new_lines.append('## WebGPU')
                    new_lines.append('')
                    # Add WebGPU content without the title
                    webgpu_lines = webgpu_content.split('\n')
                    in_content = False
                    for wline in webgpu_lines:
                        if in_content or (wline and not wline.startswith('#')):
                            in_content = True
                            new_lines.append(wline)
                    continue
                elif skip_section and line.startswith('##'):
                    skip_section = False
                
                if not skip_section:
                    new_lines.append(line)
            
            return '\n'.join(new_lines)
        else:
            # Append WebGPU section
            return chrome_content + '\n\n## WebGPU\n\n' + webgpu_content
    
    async def _generate_digest_from_yaml(
        self,
        ctx: Context,
        yaml_data: Dict,
        language: str,
        target_area: Optional[str],
        debug: bool
    ) -> str:
        """
        Generate digest from YAML data using LLM.
        
        Args:
            ctx: FastMCP context
            yaml_data: Tagged features in YAML format
            language: Output language ("en", "zh", "bilingual")
            target_area: Specific area being analyzed
            debug: Debug mode
            
        Returns:
            Generated digest markdown
        """
        # Load prompt template based on language and area
        prompt = await self._load_prompt(ctx, language, target_area, debug)
        
        # Format features as proper YAML
        yaml_text = self._format_features_for_llm(yaml_data)
        
        # Build system prompt based on language
        if language == 'zh':
            system_prompt = """你是 Chrome 更新分析专家，专注于 Web 平台功能。
请严格按照提供的模板结构生成摘要。
仅使用提供的 YAML 数据中的功能和链接，不要编造任何内容。
输出语言：中文"""
        else:  # Default to English
            system_prompt = """You are a Chrome Update Analyzer specializing in web platform features.
Follow the provided template structure strictly.
Use ONLY the features and links from the provided YAML data. Do not make up any content.
Output language: English"""
        
        # Build user message as single string (matching Enterprise pattern)
        version = yaml_data.get('version', 'Unknown')
        stats = yaml_data.get('statistics', {})
        
        # Combine prompt and data into single user message string
        user_message = f"""{prompt}

Chrome {version} Release Data
Total Features: {stats.get('total_features', 0)}
Total Links: {stats.get('total_links', 0)}

YAML Data:
```yaml
{yaml_text}
```"""
        
        # Use safe sampling with retry (no fallback - fail explicitly)
        if hasattr(ctx, 'sample'):
            if debug:
                print("Generating digest with LLM sampling...")
                print(f"Using language: {language}")
                print(f"System prompt: {system_prompt[:50]}...")
            
            try:
                return await self._safe_sample_with_retry(ctx, user_message, system_prompt, debug)
            except Exception as e:
                # Don't hide failures - raise them to be handled at higher level
                raise Exception(f"Failed to generate digest via sampling: {str(e)}")
        else:
            # No sampling capability - fail explicitly instead of fallback
            raise Exception("No sampling capability available in context")
    
    async def _safe_sample_with_retry(self, ctx: Context, messages: str, system_prompt: str, 
                                     debug: bool, max_retries: int = 3, timeout: int = 60) -> str:
        """Safe sampling with exponential backoff retry and timeout (aligned with Enterprise).
        
        Args:
            ctx: FastMCP context
            messages: User message as string (matching Enterprise pattern)
            system_prompt: System prompt as separate parameter
            debug: Debug mode
            max_retries: Maximum number of retry attempts
            timeout: Timeout in seconds for each attempt
            
        Returns:
            Generated digest content or raises exception
        """
        import asyncio
        
        for attempt in range(max_retries):
            try:
                if debug:
                    print(f"Sampling attempt {attempt + 1}/{max_retries}...")
                
                # Use asyncio.wait_for for timeout control (matching Enterprise)
                response = await asyncio.wait_for(
                    ctx.sample(
                        messages=messages,
                        system_prompt=system_prompt,  # Pass as separate parameter (aligned with Enterprise)
                        model_preferences=["claude-4-sonnet", "gpt5"],  # Aligned with Enterprise
                        temperature=0.7,  # Aligned with Enterprise (was 0.4)
                        max_tokens=50000  # Aligned with Enterprise (was 40000)
                    ),
                    timeout=timeout
                )
                
                # Extract result (matching Enterprise pattern)
                if isinstance(response, str):
                    if debug:
                        print("Successfully generated digest")
                    return response
                elif hasattr(response, 'content'):
                    return response.content
                elif hasattr(response, 'text'):
                    return response.text
                else:
                    return str(response)
                    
            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4 seconds
                    if debug:
                        print(f"Sampling timeout, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"Sampling timed out after {max_retries} retries")
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    if debug:
                        print(f"Sampling failed: {e}, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"Sampling failed after {max_retries} retries: {str(e)}")
        
        # This should never be reached, but added for type safety
        raise Exception("Unexpected end of retry loop")
    
    async def _load_prompt(self, ctx: Context, language: str, target_area: Optional[str], debug: bool) -> str:
        """Load the WebPlatform prompt template based on language and area."""
        # Select prompt file based on language
        # Note: bilingual mode should not reach here as it's handled separately
        prompt_files = {
            'en': self.base_path / 'prompts' / 'webplatform-prompts' / 'webplatform-prompt-en.md',
            'zh': self.base_path / 'prompts' / 'webplatform-prompts' / 'webplatform-prompt-zh.md'
        }
        
        # For bilingual, default to 'en' (though bilingual should be handled separately)
        if language == 'bilingual':
            language = 'en'
        
        prompt_path = prompt_files.get(language, prompt_files['en'])
        
        if debug:
            print(f"Loading prompt from: {prompt_path}")
        
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Replace [AREA] placeholder with actual area if specified
                if target_area:
                    content = content.replace('[AREA]', target_area)
                else:
                    # When no specific area, analyze all areas
                    if language == 'zh':
                        content = content.replace('在 **[AREA]** 领域拥有深厚的专业知识', '在所有 Web 平台技术领域拥有全面的专业知识')
                        content = content.replace('**[AREA]** 领域', '所有技术领域')
                        content = content.replace('[AREA]', '全领域')
                    else:
                        content = content.replace('with deep specialization in the **[AREA]** domain', 'with comprehensive expertise across all Web Platform technologies')
                        content = content.replace('for the **[AREA]** area', 'across all technical areas')
                        content = content.replace('in **[AREA]** for', 'across all areas for')
                        content = content.replace('**[AREA]** domain', 'all technical domains')
                        content = content.replace('**[AREA]**', 'all areas')
                        content = content.replace('[AREA]', 'all areas')
                return content
        
        # Try fallback to YAML bilingual prompt
        fallback_path = self.base_path / 'prompts' / 'webplatform-prompt-yaml-bilingual.md'
        if fallback_path.exists():
            if debug:
                print(f"Using fallback prompt: {fallback_path}")
            with open(fallback_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # Final fallback prompt
        return """
# WebPlatform Digest Generator

Generate a comprehensive digest of Chrome release notes focusing on:
1. Key features and improvements
2. Developer impact
3. Security enhancements
4. Performance optimizations

Format the output with clear sections and include all relevant links.
Language: """ + language
    
    def _format_features_for_llm(self, yaml_data: Dict) -> str:
        """Format features as proper YAML for LLM processing."""
        import yaml
        
        # Create simplified YAML structure with only necessary fields
        simplified_data = {
            'version': yaml_data.get('version'),
            'channel': yaml_data.get('channel', 'stable'),
            'features': []
        }
        
        for feature in yaml_data.get('features', []):
            simplified_feature = {
                'title': feature.get('title', 'Untitled'),
                'content': feature.get('content', ''),
                'primary_tags': [
                    tag.get('name') if isinstance(tag, dict) else str(tag)
                    for tag in feature.get('primary_tags', [])
                ],
                'links': []
            }
            
            # Maintain link structure
            for link in feature.get('links', []):
                if isinstance(link, dict):
                    simplified_feature['links'].append({
                        'url': link.get('url', ''),
                        'title': link.get('title', ''),
                        'type': link.get('type', 'other')
                    })
                else:
                    simplified_feature['links'].append(str(link))
            
            simplified_data['features'].append(simplified_feature)
        
        # Generate YAML string
        return yaml.safe_dump(simplified_data, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    def _generate_fallback_digest(self, yaml_data: Dict, language: str = 'en') -> str:
        """Generate a basic digest without LLM."""
        version = yaml_data.get('version', 'Unknown')
        date_str = datetime.now().strftime('%Y-%m-%d')
        stats = yaml_data.get('statistics', {})
        total_features = stats.get('total_features', 0)
        total_links = stats.get('total_links', 0)
        
        if language == 'zh':
            lines = [
                f"# Chrome {version} WebPlatform 摘要",
                f"\n*生成日期: {date_str}*",
                "\n## 摘要"
            ]
            lines.append(f"此版本包含 {total_features} 个功能特性和 {total_links} 个参考链接。")
        else:
            lines = [
                f"# Chrome {version} WebPlatform Digest",
                f"\n*Generated: {date_str}*",
                "\n## Summary"
            ]
            lines.append(f"This release includes {total_features} features with {total_links} reference links.")
        
        # Group features by primary tag
        features_by_tag = {}
        for feature in yaml_data.get('features', []):
            tags = feature.get('primary_tags', [])
            if tags:
                tag_name = tags[0].get('name') if isinstance(tags[0], dict) else str(tags[0])
                if tag_name not in features_by_tag:
                    features_by_tag[tag_name] = []
                features_by_tag[tag_name].append(feature)
            else:
                if 'uncategorized' not in features_by_tag:
                    features_by_tag['uncategorized'] = []
                features_by_tag['uncategorized'].append(feature)
        
        # Output features by category
        for tag, features in features_by_tag.items():
            if language == 'zh':
                # Translate common tags to Chinese
                tag_translations = {
                    'css': 'CSS 特性',
                    'webapi': 'Web API',
                    'javascript': 'JavaScript',
                    'graphics-webgpu': '图形与 WebGPU',
                    'security-privacy': '安全与隐私',
                    'performance': '性能优化',
                    'multimedia': '多媒体',
                    'devices': '设备接口',
                    'pwa-service-worker': 'PWA 与 Service Worker',
                    'webassembly': 'WebAssembly',
                    'deprecations': '弃用特性',
                    'uncategorized': '未分类'
                }
                tag_display = tag_translations.get(tag.lower(), tag.title())
            else:
                tag_display = tag.title()
            
            lines.append(f"\n## {tag_display}")
            
            for feature in features:
                lines.append(f"\n### {feature.get('title', 'Untitled')}")
                
                content = feature.get('content', '').strip()
                if content:
                    lines.append(content)
                
                links = feature.get('links', [])
                if links:
                    if language == 'zh':
                        lines.append("\n**参考资料:**")
                    else:
                        lines.append("\n**References:**")
                    for link in links:
                        if isinstance(link, dict):
                            url = link.get('url', '')
                            title = link.get('title', link.get('url', ''))
                            lines.append(f"- [{title}]({url})")
                        else:
                            lines.append(f"- {link}")
        
        # Add match scores if filtered
        if 'applied_filters' in yaml_data:
            if language == 'zh':
                lines.append("\n## 应用的过滤器")
                filters = yaml_data['applied_filters']
                lines.append(f"- 关注领域: {', '.join(filters.get('focus_areas', []))}")
                lines.append(f"- 最低分数: {filters.get('min_score', 0.3)}")
            else:
                lines.append("\n## Applied Filters")
                filters = yaml_data['applied_filters']
                lines.append(f"- Focus Areas: {', '.join(filters.get('focus_areas', []))}")
                lines.append(f"- Minimum Score: {filters.get('min_score', 0.3)}")
        
        return '\n'.join(lines)
    
    async def validate_links(
        self,
        ctx: Context,
        version: str = "138",
        channel: str = "stable"
    ) -> Dict[str, Any]:
        """
        Validate all extracted links.
        
        Args:
            ctx: FastMCP context
            version: Chrome version
            channel: Release channel
            
        Returns:
            Validation report
        """
        yaml_data = await self._get_yaml_data(ctx, version, channel, True, False)
        
        if not yaml_data:
            return {"error": "Could not load YAML data"}
        
        report = {
            "version": version,
            "channel": channel,
            "total_features": len(yaml_data.get('features', [])),
            "total_links": 0,
            "link_types": {},
            "invalid_links": []
        }
        
        for feature in yaml_data.get('features', []):
            for link in feature.get('links', []):
                if isinstance(link, dict):
                    url = link.get('url', '')
                    link_type = link.get('type', 'other')
                    
                    report['total_links'] += 1
                    report['link_types'][link_type] = report['link_types'].get(link_type, 0) + 1
                    
                    # Basic URL validation
                    if not url.startswith(('http://', 'https://')):
                        report['invalid_links'].append({
                            'feature': feature.get('title', 'Unknown'),
                            'url': url,
                            'reason': 'Invalid URL scheme'
                        })
        
        return report
    
    def _get_digest_path(self, version: str, channel: str, target_area: Optional[str], language: str) -> Path:
        """
        Generate digest file path with area-based folder structure.
        
        Structure:
        - With area: digest_markdown/webplatform/{area}/chrome-{version}-{channel}-{language}.md
        - Without area: digest_markdown/webplatform/chrome-{version}-{channel}-{language}.md
        """
        # Ensure channel is set
        if not channel:
            channel = 'stable'
        
        # Determine language suffix
        lang_suffix = {
            'en': 'en',
            'zh': 'zh',
            'bilingual': 'bilingual'  # This shouldn't be used since bilingual generates 2 files
        }.get(language, 'en')
        
        if target_area:
            # Normalize area name: 'webgpu' -> 'graphics-webgpu' for consistency
            normalized_area = 'graphics-webgpu' if target_area in ['webgpu', 'graphics-webgpu'] else target_area
            # Area-specific digests go in subdirectories
            area_dir = self.digest_dir / normalized_area
            area_dir.mkdir(parents=True, exist_ok=True)
            filename = f"chrome-{version}-{channel}-{lang_suffix}.md"
            return area_dir / filename
        else:
            # General digest in root directory
            filename = f"chrome-{version}-{channel}-{lang_suffix}.md"
            return self.digest_dir / filename
    
    async def _save_digest(self, content: str, file_path: Path, debug: bool = False) -> None:
        """
        Save digest content to file.
        
        Args:
            content: Digest markdown content
            file_path: Output file path
            debug: Debug mode
        """
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if debug:
                print(f"Successfully saved digest to: {file_path}")
                
        except Exception as e:
            if debug:
                print(f"Error saving digest: {e}")
            raise