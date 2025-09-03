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
        split_by_area: bool = True,
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
            split_by_area: Whether to generate separate digests for each area (default: True)
            target_area: Specific area to analyze (e.g., "css", "webapi", "security")
            debug: Enable debug output
            
        Returns:
            Generated digest in markdown format or JSON with per-area results
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
                    "error": f"Release notes for Chrome {version} {channel} channel not found. This specific channel needs to be processed separately. Do NOT use other channels as alternatives.",
                    "version": version,
                    "channel": channel,
                    "note": f"To process {channel} channel, run: python src/processors/clean_data_pipeline.py --version {version} --channel {channel} --with-yaml"
                }, ensure_ascii=False)
            
            # Step 2: Apply focus area filtering if specified
            if focus_area_list:
                yaml_data = self.yaml_pipeline.filter_by_focus_areas(
                    yaml_data, focus_area_list
                )
                if debug:
                    filtered_count = len(yaml_data.get('features', []))
                    print(f"Filtered to {filtered_count} features")
            
            # Step 3: Handle per-area generation if split_by_area is True
            if split_by_area:
                return await self._generate_per_area_digests(ctx, yaml_data, version, channel, language, debug)
            
            # Step 4: Generate digest from YAML data with language support
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
        if target_area and target_area != "all":
            # Normalize area name: 'webgpu' -> 'graphics-webgpu' for consistency
            normalized_area = 'graphics-webgpu' if target_area in ['webgpu', 'graphics-webgpu'] else target_area
            # Area-specific files are now in areas/{area}/ directories
            yaml_path = self.cache_dir.parent / 'areas' / normalized_area / f"chrome-{version}-{channel}.yml"
        else:
            # For "all" or no target_area, aggregate from all area-specific files
            return await self._aggregate_area_files(ctx, version, channel, use_cache, debug)
        
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
    
    async def _aggregate_area_files(
        self,
        ctx: Context,
        version: str,
        channel: str,
        use_cache: bool,
        debug: bool
    ) -> Dict:
        """
        Aggregate all area-specific files into a single comprehensive result.
        
        Args:
            ctx: MCP context
            version: Chrome version
            channel: Release channel  
            use_cache: Whether to use cached files
            debug: Debug mode
            
        Returns:
            Aggregated YAML data dictionary
        """
        aggregated_features = []
        all_areas = []
        total_stats = {'total_features': 0, 'total_links': 0, 'primary_tags': {}, 'cross_cutting': {}}
        
        # Get all area subdirectories from areas/ directory
        areas_dir = self.cache_dir.parent / 'areas'
        if not areas_dir.exists():
            if debug:
                print(f"Areas directory not found: {areas_dir}")
            return None
            
        for area_dir in areas_dir.iterdir():
            if not area_dir.is_dir():
                continue
                
            area_name = area_dir.name
            yaml_path = area_dir / f"chrome-{version}-{channel}.yml"
            
            if yaml_path.exists():
                try:
                    area_data = self.yaml_pipeline.load_from_yaml(yaml_path)
                    if area_data and 'features' in area_data:
                        aggregated_features.extend(area_data['features'])
                        all_areas.append(area_name)
                        
                        # Aggregate statistics
                        area_stats = area_data.get('statistics', {})
                        total_stats['total_features'] += area_stats.get('total_features', 0)
                        total_stats['total_links'] += area_stats.get('total_links', 0)
                        
                        # Merge tag counts
                        for tag, count in area_stats.get('primary_tags', {}).items():
                            total_stats['primary_tags'][tag] = total_stats['primary_tags'].get(tag, 0) + count
                            
                        for concern, count in area_stats.get('cross_cutting', {}).items():
                            total_stats['cross_cutting'][concern] = total_stats['cross_cutting'].get(concern, 0) + count
                            
                        if debug:
                            print(f"Aggregated {len(area_data['features'])} features from {area_name}")
                            
                except Exception as e:
                    if debug:
                        print(f"Failed to load {yaml_path}: {e}")
                    continue
        
        if not aggregated_features:
            if debug:
                print(f"No area files found for Chrome {version} {channel}")
            return None
            
        # Build aggregated result
        return {
            'version': version,
            'channel': channel,
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_method': 'aggregated',
            'statistics': total_stats,
            'features': aggregated_features,
            'areas': all_areas
        }
    
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
        base_dir = self.base_path / 'upstream_docs' / 'release_notes' / 'WebPlatform'
        
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

重要规则：
1. 绝对不要建议检查其他 channel（如 beta/dev/canary）当 stable 不可用时
2. 每个 channel（stable、beta、dev）包含不同的内容和发布日期 - 它们不可互换
3. 如果请求的 channel 数据不存在，只报告该 channel 需要处理，不要提供其他 channel 作为替代
4. 请严格按照提供的模板结构生成摘要
5. 仅使用提供的 YAML 数据中的功能和链接，不要编造任何内容

输出语言：中文"""
        else:  # Default to English
            system_prompt = """You are a Chrome Update Analyzer specializing in web platform features.

CRITICAL RULES:
1. NEVER suggest checking a different channel (beta/dev/canary) when stable is unavailable
2. Each channel (stable, beta, dev) contains DIFFERENT content and release dates - they are NOT interchangeable
3. If requested channel data doesn't exist, only report that channel needs processing - do NOT offer other channels as alternatives
4. Follow the provided template structure strictly
5. Use ONLY the features and links from the provided YAML data. Do not make up any content

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
    
    async def _generate_per_area_digests(
        self,
        ctx: Context,
        yaml_data: Dict,
        version: str,
        channel: str,
        language: Optional[str],
        debug: bool
    ) -> str:
        """
        Generate digests for each area separately.
        
        Args:
            ctx: FastMCP context
            yaml_data: Full YAML data with all features
            version: Chrome version
            channel: Release channel
            language: Output language ("en", "zh", or None for bilingual)
            debug: Debug mode
            
        Returns:
            JSON response with status and output paths
        """
        # Determine languages to generate
        languages = ['en', 'zh'] if language in [None, 'bilingual'] else [language]
        
        # Get all areas from YAML data
        areas = self._get_areas_from_yaml(yaml_data)
        if debug:
            print(f"Found {len(areas)} areas to process: {areas}")
        
        results = {
            "success": True,
            "mode": "per_area",
            "version": version,
            "channel": channel,
            "language": language or "bilingual",
            "languages": languages,
            "areas": areas,
            "outputs": {},
            "errors": {},
            "translation_status": {}
        }
        
        # Process each area
        for area in areas:
            if debug:
                print(f"\nProcessing area: {area}")
            
            # Normalize area name
            normalized_area = self.focus_manager.normalize_area(area)
            
            # Load area-specific YAML
            area_yaml = await self._load_area_yaml(ctx, version, channel, normalized_area, yaml_data, debug)
            if not area_yaml or len(area_yaml.get('features', [])) == 0:
                if debug:
                    print(f"No features for area {area}, generating fallback")
                # Generate minimal fallback
                fallback_content = self._generate_minimal_fallback(version, channel, area, 'en')
                fallback_path = self._get_digest_path(version, channel, normalized_area, 'en')
                await self._save_digest(fallback_content, fallback_path, debug)
                results["outputs"][normalized_area] = {"en": str(fallback_path)}
                if 'zh' in languages:
                    fallback_zh = self._generate_minimal_fallback(version, channel, area, 'zh')
                    fallback_zh_path = self._get_digest_path(version, channel, normalized_area, 'zh')
                    await self._save_digest(fallback_zh, fallback_zh_path, debug)
                    results["outputs"][normalized_area]["zh"] = str(fallback_zh_path)
                continue
            
            # Generate English digest first (canonical)
            try:
                if debug:
                    print(f"Generating English digest for {area}")
                
                english_digest = await self._generate_area_digest(
                    ctx, area_yaml, 'en', normalized_area, debug
                )
                
                # Validate English digest
                validation_result = self._validate_digest(english_digest, area_yaml)
                if not validation_result['valid']:
                    if debug:
                        print(f"Validation failed for {area}: {validation_result['issues']}")
                    # Retry once with corrective prompt
                    english_digest = await self._generate_area_digest(
                        ctx, area_yaml, 'en', normalized_area, debug,
                        retry_context=validation_result['issues']
                    )
                    validation_result = self._validate_digest(english_digest, area_yaml)
                    if not validation_result['valid']:
                        # Generate fallback
                        english_digest = self._generate_area_fallback(
                            area_yaml, 'en', normalized_area, "LLM generation failed validation"
                        )
                
                # Save English digest
                en_path = self._get_digest_path(version, channel, normalized_area, 'en')
                await self._save_digest(english_digest, en_path, debug)
                
                if normalized_area not in results["outputs"]:
                    results["outputs"][normalized_area] = {}
                results["outputs"][normalized_area]["en"] = str(en_path)
                
                # Generate Chinese translation if needed
                if 'zh' in languages:
                    if debug:
                        print(f"Translating to Chinese for {area}")
                    
                    try:
                        chinese_digest = await self._translate_digest(
                            ctx, english_digest, normalized_area, version, channel, debug
                        )
                        
                        # Validate translation
                        translation_valid = self._validate_translation(english_digest, chinese_digest)
                        if not translation_valid['valid']:
                            if debug:
                                print(f"Translation validation failed: {translation_valid['issues']}")
                            # Retry translation once
                            chinese_digest = await self._translate_digest(
                                ctx, english_digest, normalized_area, version, channel, debug,
                                retry_context=translation_valid['issues']
                            )
                            translation_valid = self._validate_translation(english_digest, chinese_digest)
                            if not translation_valid['valid']:
                                # Translation fallback
                                chinese_digest = self._generate_translation_fallback(
                                    version, channel, normalized_area, en_path
                                )
                                results["translation_status"][normalized_area] = "fallback"
                            else:
                                results["translation_status"][normalized_area] = "retry_success"
                        else:
                            results["translation_status"][normalized_area] = "ok"
                        
                        # Save Chinese digest
                        zh_path = self._get_digest_path(version, channel, normalized_area, 'zh')
                        await self._save_digest(chinese_digest, zh_path, debug)
                        results["outputs"][normalized_area]["zh"] = str(zh_path)
                        
                    except Exception as e:
                        if debug:
                            print(f"Translation failed for {area}: {e}")
                        results["errors"][f"{normalized_area}:zh"] = str(e)
                        results["translation_status"][normalized_area] = "error"
                        # Generate translation fallback
                        fallback = self._generate_translation_fallback(
                            version, channel, normalized_area, en_path
                        )
                        zh_path = self._get_digest_path(version, channel, normalized_area, 'zh')
                        await self._save_digest(fallback, zh_path, debug)
                        results["outputs"][normalized_area]["zh"] = str(zh_path)
                
            except Exception as e:
                if debug:
                    print(f"Failed to generate digest for {area}: {e}")
                results["errors"][f"{normalized_area}:en"] = str(e)
                results["success"] = False
        
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    def _get_areas_from_yaml(self, yaml_data: Dict) -> List[str]:
        """Extract all areas from YAML data and normalize them."""
        areas = set()
        for feature in yaml_data.get('features', []):
            tags = feature.get('primary_tags', [])
            for tag in tags:
                if isinstance(tag, dict):
                    tag_name = tag.get('name', 'others')
                else:
                    tag_name = str(tag)
                
                # Normalize the area name to match folder structure
                normalized = self.focus_manager.normalize_area(tag_name)
                areas.add(normalized)
        
        # Always include 'others' if there are untagged features
        if not areas:
            areas.add('others')
        
        return sorted(list(areas))
    
    async def _load_area_yaml(
        self,
        ctx: Context,
        version: str,
        channel: str,
        area: str,
        full_yaml: Dict,
        debug: bool
    ) -> Optional[Dict]:
        """Load or extract area-specific YAML data."""
        # Check for cached area YAML
        area_yaml_path = self.cache_dir / area / f"chrome-{version}-{channel}.yml"
        if area_yaml_path.exists():
            if debug:
                print(f"Loading cached area YAML: {area_yaml_path}")
            return self.yaml_pipeline.load_from_yaml(area_yaml_path)
        
        # Extract features for this area from full YAML
        area_features = []
        for feature in full_yaml.get('features', []):
            tags = feature.get('primary_tags', [])
            tag_names = []
            for tag in tags:
                if isinstance(tag, dict):
                    tag_names.append(tag.get('name', ''))
                else:
                    tag_names.append(str(tag))
            
            # Check if area matches any tag, considering normalization
            # For graphics-webgpu, we need to match 'webgpu' tags
            if area in tag_names:
                area_features.append(feature)
            elif area == 'graphics-webgpu' and 'webgpu' in tag_names:
                area_features.append(feature)
            elif area == 'security-privacy' and ('security' in tag_names or 'privacy' in tag_names):
                area_features.append(feature)
            elif area == 'pwa-service-worker' and ('pwa' in tag_names or 'service-worker' in tag_names or 'serviceworker' in tag_names):
                area_features.append(feature)
            elif area == 'navigation-loading' and ('loading' in tag_names or 'navigation' in tag_names):
                area_features.append(feature)
            elif area == 'origin-trials' and 'trials' in tag_names:
                area_features.append(feature)
        
        if not area_features and area == 'others':
            # Get untagged features for 'others'
            for feature in full_yaml.get('features', []):
                if not feature.get('primary_tags', []):
                    area_features.append(feature)
        
        # Create area-specific YAML structure
        area_yaml = {
            'version': full_yaml.get('version'),
            'channel': full_yaml.get('channel'),
            'area': area,
            'features': area_features,
            'statistics': {
                'total_features': len(area_features),
                'total_links': sum(len(f.get('links', [])) for f in area_features)
            }
        }
        
        return area_yaml
    
    async def _generate_area_digest(
        self,
        ctx: Context,
        area_yaml: Dict,
        language: str,
        area: str,
        debug: bool,
        retry_context: Optional[str] = None
    ) -> str:
        """Generate digest for a specific area."""
        # Load prompt template
        prompt = await self._load_area_prompt(ctx, language, area, debug)
        
        # Truncate feature content to avoid token limits
        truncated_yaml = self._truncate_features(area_yaml, max_content_length=300)
        
        # Format features as YAML
        yaml_text = self._format_features_for_llm(truncated_yaml)
        
        # Build system prompt
        area_display = self.focus_manager.get_area_display_name(area)
        if language == 'zh':
            system_prompt = f"""你是 Chrome 更新分析专家，专注于 {area_display} 领域。
请严格按照提供的模板结构生成摘要。
仅使用提供的 YAML 数据中的功能和链接，不要编造任何内容。
输出语言：中文"""
        else:
            system_prompt = f"""You are a Chrome Update Analyzer specializing in {area_display}.
Follow the provided template structure strictly.
Use ONLY the features and links from the provided YAML data. Do not make up any content.
Output language: English"""
        
        # Add retry context if provided
        if retry_context:
            system_prompt += f"\n\nPREVIOUS ATTEMPT FAILED. Issues found:\n{retry_context}\nPlease correct these issues."
        
        # Build user message
        version = area_yaml.get('version', 'Unknown')
        stats = area_yaml.get('statistics', {})
        
        user_message = f"""{prompt}

Chrome {version} Release Data for {area_display}
Total Features: {stats.get('total_features', 0)}
Total Links: {stats.get('total_links', 0)}

YAML Data:
```yaml
{yaml_text}
```"""
        
        # Generate with LLM
        return await self._safe_sample_with_retry(ctx, user_message, system_prompt, debug)
    
    async def _load_area_prompt(self, ctx: Context, language: str, area: str, debug: bool) -> str:
        """Load prompt template for specific area."""
        prompt_path = self.base_path / 'prompts' / 'webplatform-prompts' / f'webplatform-prompt-{language}.md'
        
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Replace [AREA] with display name
                area_display = self.focus_manager.get_area_display_name(area)
                content = content.replace('[AREA]', area_display)
                
                return content
        
        # Fallback prompt
        area_display = self.focus_manager.get_area_display_name(area)
        if language == 'zh':
            return f"生成 Chrome {area_display} 领域的更新摘要。"
        else:
            return f"Generate a Chrome update digest for the {area_display} area."
    
    def _truncate_features(self, yaml_data: Dict, max_content_length: int = 300) -> Dict:
        """Truncate feature content to avoid token limits."""
        truncated = yaml_data.copy()
        truncated['features'] = []
        
        for feature in yaml_data.get('features', []):
            truncated_feature = feature.copy()
            content = truncated_feature.get('content', '')
            if len(content) > max_content_length:
                truncated_feature['content'] = content[:max_content_length] + '...'
            truncated['features'].append(truncated_feature)
        
        return truncated
    
    def _validate_digest(self, digest: str, yaml_data: Dict) -> Dict[str, Any]:
        """Validate that digest contains expected features and links."""
        import re
        
        # Extract feature titles from YAML
        expected_titles = set()
        expected_links = set()
        
        for feature in yaml_data.get('features', []):
            expected_titles.add(feature.get('title', ''))
            for link in feature.get('links', []):
                if isinstance(link, dict):
                    expected_links.add(link.get('url', ''))
                else:
                    expected_links.add(str(link))
        
        # Extract titles and links from digest
        # Look for H3 headers (feature titles)
        found_titles = set(re.findall(r'^###\s+(.+)$', digest, re.MULTILINE))
        # Look for markdown links
        found_links = set(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', digest))
        found_link_urls = {url for _, url in found_links}
        
        # Calculate missing elements
        missing_titles = expected_titles - found_titles
        extra_links = found_link_urls - expected_links
        
        # Determine if valid
        missing_ratio = len(missing_titles) / len(expected_titles) if expected_titles else 0
        valid = missing_ratio <= 0.3 and len(extra_links) <= 2
        
        issues = []
        if missing_ratio > 0.3:
            issues.append(f"Missing {len(missing_titles)} of {len(expected_titles)} features")
        if len(extra_links) > 2:
            issues.append(f"Found {len(extra_links)} unknown links")
        
        return {
            'valid': valid,
            'missing_titles': list(missing_titles),
            'extra_links': list(extra_links),
            'missing_ratio': missing_ratio,
            'issues': '; '.join(issues) if issues else None
        }
    
    async def _translate_digest(
        self,
        ctx: Context,
        english_digest: str,
        area: str,
        version: str,
        channel: str,
        debug: bool,
        retry_context: Optional[str] = None
    ) -> str:
        """Translate English digest to Chinese."""
        # Load translation prompt
        prompt_path = self.base_path / 'prompts' / 'webplatform-prompts' / 'webplatform-translation-prompt-zh.md'
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Translation prompt not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        # Replace placeholders
        area_display = self.focus_manager.get_area_display_name(area)
        prompt = prompt_template.replace('[AREA_DISPLAY]', area_display)
        prompt = prompt.replace('[AREA_KEY]', area)
        prompt = prompt.replace('[VERSION]', version)
        prompt = prompt.replace('[CHANNEL]', channel)
        prompt = prompt.replace('[ENGLISH_DIGEST_MARKDOWN]', english_digest)
        
        # System prompt for translation
        system_prompt = "You are a professional bilingual technical translator specializing in Chrome Web Platform documentation."
        
        if retry_context:
            prompt += f"\n\nPREVIOUS TRANSLATION FAILED VALIDATION:\n{retry_context}\nPlease correct these issues."
        
        # Generate translation
        if debug:
            print(f"Translating digest for {area} to Chinese...")
        
        return await self._safe_sample_with_retry(ctx, prompt, system_prompt, debug)
    
    def _validate_translation(self, english_digest: str, chinese_digest: str) -> Dict[str, Any]:
        """Validate that translation preserves structure and links."""
        import re
        
        # Check for error marker
        if 'ERROR_TRANSLATION_STRUCTURE_MISMATCH' in chinese_digest:
            return {
                'valid': False,
                'issues': 'Translation reported structure mismatch error'
            }
        
        # Extract headings from both versions
        en_headings = re.findall(r'^(#{2,4})\s+(.+)$', english_digest, re.MULTILINE)
        zh_headings = re.findall(r'^(#{2,4})\s+(.+)$', chinese_digest, re.MULTILINE)
        
        # Extract links from both versions
        en_links = set(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', english_digest))
        zh_links = set(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', chinese_digest))
        
        en_link_urls = {url for _, url in en_links}
        zh_link_urls = {url for _, url in zh_links}
        
        issues = []
        
        # Check heading count and hierarchy
        if len(en_headings) != len(zh_headings):
            issues.append(f"Heading count mismatch: EN={len(en_headings)}, ZH={len(zh_headings)}")
        
        # Check heading levels match
        for i, ((en_level, _), (zh_level, _)) in enumerate(zip(en_headings[:min(len(en_headings), len(zh_headings))], zh_headings)):
            if en_level != zh_level:
                issues.append(f"Heading level mismatch at position {i+1}")
        
        # Check links are preserved
        missing_links = en_link_urls - zh_link_urls
        extra_links = zh_link_urls - en_link_urls
        
        if missing_links:
            issues.append(f"Missing {len(missing_links)} links from English version")
        if extra_links:
            issues.append(f"Added {len(extra_links)} new links not in English version")
        
        valid = len(issues) == 0
        
        return {
            'valid': valid,
            'issues': '; '.join(issues) if issues else None,
            'heading_match': len(en_headings) == len(zh_headings),
            'link_match': en_link_urls == zh_link_urls
        }
    
    def _generate_area_fallback(self, area_yaml: Dict, language: str, area: str, reason: str) -> str:
        """Generate fallback digest for an area."""
        version = area_yaml.get('version', 'Unknown')
        area_display = self.focus_manager.get_area_display_name(area)
        
        if language == 'zh':
            lines = [
                f"# Chrome {version} {area_display} 摘要 (Fallback)",
                f"> LLM 生成失败：{reason}。以下是原始功能列表。",
                "",
                "## 功能列表"
            ]
        else:
            lines = [
                f"# Chrome {version} {area_display} Digest (Fallback)",
                f"> LLM generation failed: {reason}. Below is the raw feature list.",
                "",
                "## Features"
            ]
        
        for feature in area_yaml.get('features', []):
            lines.append(f"\n### {feature.get('title', 'Untitled')}")
            
            links = feature.get('links', [])
            if links:
                if language == 'zh':
                    lines.append("链接：")
                else:
                    lines.append("Links:")
                for link in links:
                    if isinstance(link, dict):
                        lines.append(f"- [{link.get('title', 'Link')}]({link.get('url', '')})")
                    else:
                        lines.append(f"- {link}")
        
        return '\n'.join(lines)
    
    def _generate_translation_fallback(self, version: str, channel: str, area: str, en_path: Path) -> str:
        """Generate fallback for failed translation."""
        area_display = self.focus_manager.get_area_display_name(area)
        return f"""# Chrome {version} {area_display} 摘要（中文翻译失败）

> 自动翻译失败。请参考英文版：{en_path}

## Translation Failed

The automatic translation to Chinese failed. Please refer to the English version for the complete digest.

English version path: `{en_path}`
"""
    
    def _generate_minimal_fallback(self, version: str, channel: str, area: str, language: str) -> str:
        """Generate minimal fallback for empty area."""
        area_display = self.focus_manager.get_area_display_name(area)
        
        if language == 'zh':
            return f"""# Chrome {version} {area_display} 摘要

> 此版本在 {area_display} 领域没有新功能。
"""
        else:
            return f"""# Chrome {version} {area_display} Digest

> No new features in the {area_display} area for this release.
"""