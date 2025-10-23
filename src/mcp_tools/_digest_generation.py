from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional

from fastmcp import Context

from src.utils.focus_area_manager import FocusAreaManager


SafeSampler = Callable[..., Awaitable[str]]


class DigestGenerationEngine:
    """Encapsulates prompt loading, LLM generation, translation, and validation logic."""

    def __init__(
        self,
        base_path: Path,
        focus_manager: FocusAreaManager,
        safe_sampler: SafeSampler,
    ) -> None:
        self.base_path = base_path
        self.focus_manager = focus_manager
        self._safe_sampler = safe_sampler

    async def generate_digest_from_yaml(
        self,
        ctx: Context,
        yaml_data: Dict[str, Any],
        language: str,
        target_area: Optional[str],
        debug: bool,
    ) -> str:
        prompt = await self._load_prompt(language, target_area, debug)
        yaml_text = self._format_features_for_llm(yaml_data)

        if language == 'zh':
            system_prompt = """你是 Chrome 更新分析专家，专注于 Web 平台功能。

重要规则：
1. 绝对不要建议检查其他 channel（如 beta/dev/canary）当 stable 不可用时
2. 每个 channel（stable、beta、dev）包含不同的内容和发布日期 - 它们不可互换
3. 如果请求的 channel 数据不存在，只报告该 channel 需要处理，不要提供其他 channel 作为替代
4. 请严格按照提供的模板结构生成摘要
5. 仅使用提供的 YAML 数据中的功能和链接，不要编造任何内容

输出语言：中文"""
        else:
            system_prompt = """You are a Chrome Update Analyzer specializing in web platform features.

CRITICAL RULES:
1. NEVER suggest checking a different channel (beta/dev/canary) when stable is unavailable
2. Each channel (stable, beta, dev) contains DIFFERENT content and release dates - they are NOT interchangeable
3. If requested channel data doesn't exist, only report that channel needs processing - do NOT offer other channels as alternatives
4. Follow the provided template structure strictly
5. Use ONLY the features and links from the provided YAML data. Do not make up any content

Output language: English"""

        version = yaml_data.get('version', 'Unknown')
        stats = yaml_data.get('statistics', {})

        user_message = f"""{prompt}

Chrome {version} Release Data
Total Features: {stats.get('total_features', 0)}
Total Links: {stats.get('total_links', 0)}

YAML Data:
```yaml
{yaml_text}
```"""

        if not hasattr(ctx, 'sample'):
            raise Exception("No sampling capability available in context")

        if debug:
            print("Generating digest with LLM sampling...")
            print(f"Using language: {language}")
            print(f"System prompt: {system_prompt[:50]}...")

        return await self._safe_sampler(
            ctx,
            user_message,
            system_prompt,
            debug,
            telemetry_context={
                "operation": "bulk_digest_generation",
                "language": language,
                "target_area": target_area or "all",
                "version": version,
                "channel": yaml_data.get('channel'),
            },
        )

    async def generate_area_digest(
        self,
        ctx: Context,
        area_yaml: Dict[str, Any],
        language: str,
        area: str,
        debug: bool,
        retry_context: Optional[str] = None,
    ) -> str:
        prompt = await self._load_area_prompt(language, area, debug)
        truncated_yaml = self._truncate_features(area_yaml, max_content_length=300)
        yaml_text = self._format_features_for_llm(truncated_yaml)

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

        if retry_context:
            system_prompt += f"\n\nPREVIOUS ATTEMPT FAILED. Issues found:\n{retry_context}\nPlease correct these issues."

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

        return await self._safe_sampler(
            ctx,
            user_message,
            system_prompt,
            debug,
            telemetry_context={
                "operation": "english_generation" if language == 'en' else f"{language}_generation",
                "language": language,
                "area": area,
                "version": area_yaml.get('version'),
                "channel": area_yaml.get('channel'),
            },
        )

    async def translate_digest(
        self,
        ctx: Context,
        english_digest: str,
        area: str,
        version: str,
        channel: str,
        debug: bool,
        retry_context: Optional[str] = None,
    ) -> str:
        prompt_path = self.base_path / 'prompts' / 'webplatform-prompts' / 'webplatform-translation-prompt-zh.md'
        if not prompt_path.exists():
            raise FileNotFoundError(f"Translation prompt not found: {prompt_path}")

        prompt_template = prompt_path.read_text(encoding='utf-8')
        area_display = self.focus_manager.get_area_display_name(area)
        prompt = (
            prompt_template.replace('[AREA_DISPLAY]', area_display)
            .replace('[AREA_KEY]', area)
            .replace('[VERSION]', version)
            .replace('[CHANNEL]', channel)
            .replace('[ENGLISH_DIGEST_MARKDOWN]', english_digest)
        )

        system_prompt = "You are a professional bilingual technical translator specializing in Chrome Web Platform documentation."

        if retry_context:
            prompt += f"\n\nPREVIOUS TRANSLATION FAILED VALIDATION:\n{retry_context}\nPlease correct these issues."

        if debug:
            print(f"Translating digest for {area} to Chinese...")

        return await self._safe_sampler(
            ctx,
            prompt,
            system_prompt,
            debug,
            telemetry_context={
                "operation": "translation",
                "language": "zh",
                "area": area,
                "version": version,
                "channel": channel,
            },
        )

    def validate_translation(self, english_digest: str, chinese_digest: str) -> Dict[str, Any]:
        if 'ERROR_TRANSLATION_STRUCTURE_MISMATCH' in chinese_digest:
            return {
                'valid': False,
                'issues': 'Translation reported structure mismatch error'
            }

        en_headings = re.findall(r'^(#{2,4})\s+(.+)$', english_digest, re.MULTILINE)
        zh_headings = re.findall(r'^(#{2,4})\s+(.+)$', chinese_digest, re.MULTILINE)

        en_links = set(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', english_digest))
        zh_links = set(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', chinese_digest))

        en_link_urls = {url for _, url in en_links}
        zh_link_urls = {url for _, url in zh_links}

        issues: List[str] = []

        if len(en_headings) != len(zh_headings):
            issues.append(f"Heading count mismatch: EN={len(en_headings)}, ZH={len(zh_headings)}")

        for i, ((en_level, _), (zh_level, _)) in enumerate(zip(en_headings[:min(len(en_headings), len(zh_headings))], zh_headings)):
            if en_level != zh_level:
                issues.append(f"Heading level mismatch at position {i+1}")

        missing_links = en_link_urls - zh_link_urls
        extra_links = zh_link_urls - en_link_urls

        if missing_links:
            issues.append(f"Missing {len(missing_links)} links from English version")
        if extra_links:
            issues.append(f"Added {len(extra_links)} new links not in English version")

        chinese_char_pattern = re.compile('[\u3400-\u4dbf\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
        content_char_pattern = re.compile('[A-Za-z\u3400-\u4dbf\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
        chinese_char_count = len(chinese_char_pattern.findall(chinese_digest))
        content_char_count = len(content_char_pattern.findall(chinese_digest))
        chinese_ratio = (chinese_char_count / content_char_count) if content_char_count else 0.0
        if content_char_count >= 100 and chinese_ratio < 0.3:
            issues.append(f"Chinese character ratio too low ({chinese_ratio:.2f}, threshold 0.30)")

        valid = len(issues) == 0

        return {
            'valid': valid,
            'issues': '; '.join(issues) if issues else None,
            'heading_match': len(en_headings) == len(zh_headings),
            'link_match': en_link_urls == zh_link_urls,
            'chinese_ratio': chinese_ratio,
            'content_char_count': content_char_count,
        }

    def validate_digest(self, digest: str, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        expected_titles = set()
        expected_links = set()

        for feature in yaml_data.get('features', []):
            expected_titles.add(feature.get('title', ''))
            for link in feature.get('links', []):
                if isinstance(link, dict):
                    expected_links.add(link.get('url', ''))
                else:
                    expected_links.add(str(link))

        h3_titles = re.findall(r'^###\s+(.+)$', digest, re.MULTILINE)
        h4_titles = re.findall(r'^####\s+(.+)$', digest, re.MULTILINE)

        def _normalize_title(title: str) -> str:
            normalized = title.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
            normalized = normalized.replace('–', '-').replace('—', '-')
            normalized = re.sub(r'\s+', ' ', normalized.strip().lower())
            return normalized

        raw_found_titles = h3_titles if h3_titles else h4_titles
        found_titles = {_normalize_title(title) for title in raw_found_titles}
        normalized_expected = {_normalize_title(title) for title in expected_titles}

        found_links = set(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', digest))
        found_link_urls = {url for _, url in found_links}

        missing_normalized = normalized_expected - found_titles
        missing_titles = [title for title in expected_titles if _normalize_title(title) in missing_normalized]
        extra_links = found_link_urls - expected_links

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
            'issues': '; '.join(issues) if issues else None,
        }

    def generate_area_fallback(self, area_yaml: Dict[str, Any], language: str, area: str, reason: str) -> str:
        version = area_yaml.get('version', 'Unknown')
        area_display = self.focus_manager.get_area_display_name(area)

        if language == 'zh':
            lines = [
                f"# Chrome {version} {area_display} 摘要 (Fallback)",
                f"> LLM 生成失败：{reason}。以下是原始功能列表。",
                "",
                "## 功能列表",
            ]
        else:
            lines = [
                f"# Chrome {version} {area_display} Digest (Fallback)",
                f"> LLM generation failed: {reason}. Below is the raw feature list.",
                "",
                "## Features",
            ]

        for feature in area_yaml.get('features', []):
            lines.append(f"\n### {feature.get('title', 'Untitled')}")
            links = feature.get('links', [])
            if links:
                lines.append("链接：" if language == 'zh' else "Links:")
                for link in links:
                    if isinstance(link, dict):
                        lines.append(f"- [{link.get('title', 'Link')}]({link.get('url', '')})")
                    else:
                        lines.append(f"- {link}")

        return '\n'.join(lines)

    def generate_translation_fallback(self, version: str, channel: str, area: str, en_path: Path) -> str:
        area_display = self.focus_manager.get_area_display_name(area)
        return f"""# Chrome {version} {area_display} 摘要（中文翻译失败）

> 自动翻译失败。请参考英文版：{en_path}

## Translation Failed

The automatic translation to Chinese failed. Please refer to the English version for the complete digest.

English version path: `{en_path}`
"""

    def generate_minimal_fallback(self, version: str, channel: str, area: str, language: str) -> str:
        area_display = self.focus_manager.get_area_display_name(area)

        if language == 'zh':
            return f"""# Chrome {version} {area_display} 摘要

> 此版本在 {area_display} 领域没有新功能。
"""
        return f"""# Chrome {version} {area_display} Digest

> No new features in the {area_display} area for this release.
"""

    async def _load_prompt(self, language: str, target_area: Optional[str], debug: bool) -> str:
        prompt_files = {
            'en': self.base_path / 'prompts' / 'webplatform-prompts' / 'webplatform-prompt-en.md',
            'zh': self.base_path / 'prompts' / 'webplatform-prompts' / 'webplatform-prompt-zh.md',
        }

        if language == 'bilingual':
            language = 'en'

        prompt_path = prompt_files.get(language, prompt_files['en'])

        if debug:
            print(f"Loading prompt from: {prompt_path}")

        if prompt_path.exists():
            content = prompt_path.read_text(encoding='utf-8')
            if target_area:
                return content.replace('[AREA]', target_area)

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

        if language == 'zh':
            return "你是 Chrome 更新分析专家，擅长处理所有 Web 平台技术领域的更新摘要。"
        return "You are a Chrome Update Analyzer with expertise across all Web Platform technologies."

    async def _load_area_prompt(self, language: str, area: str, debug: bool) -> str:
        prompt_path = self.base_path / 'prompts' / 'webplatform-prompts' / f'webplatform-prompt-{language}.md'

        if prompt_path.exists():
            content = prompt_path.read_text(encoding='utf-8')
            area_display = self.focus_manager.get_area_display_name(area)
            return content.replace('[AREA]', area_display)

        area_display = self.focus_manager.get_area_display_name(area)
        if language == 'zh':
            return f"生成 Chrome {area_display} 领域的更新摘要。"
        return f"Generate a Chrome update digest for the {area_display} area."

    def _truncate_features(self, yaml_data: Dict[str, Any], max_content_length: int = 300) -> Dict[str, Any]:
        truncated = yaml_data.copy()
        truncated['features'] = []

        for feature in yaml_data.get('features', []):
            truncated_feature = feature.copy()
            content = truncated_feature.get('content', '')
            if len(content) > max_content_length:
                truncated_feature['content'] = content[:max_content_length] + '...'
            truncated['features'].append(truncated_feature)

        return truncated

    def _format_features_for_llm(self, yaml_data: Dict[str, Any]) -> str:
        lines: List[str] = []
        lines.append(f"version: {yaml_data.get('version', 'Unknown')}")
        lines.append(f"channel: {yaml_data.get('channel', 'Unknown')}")
        lines.append(f"area: {yaml_data.get('area', 'all')}")
        lines.append("features:")

        for feature in yaml_data.get('features', []):
            lines.append("  - title: " + self._escape_yaml_value(feature.get('title', 'Untitled')))
            lines.append("    summary: " + self._escape_yaml_value(feature.get('summary', '')))
            lines.append("    content: |")
            content = feature.get('content', '').replace('\n', '\n      ')
            lines.append("      " + content)
            lines.append("    importance: " + self._escape_yaml_value(feature.get('importance', 'medium')))

            links = feature.get('links', [])
            if links:
                lines.append("    links:")
                for link in links:
                    if isinstance(link, dict):
                        lines.append("      - title: " + self._escape_yaml_value(link.get('title', 'Link')))
                        lines.append("        url: " + self._escape_yaml_value(link.get('url', '')))
                    else:
                        lines.append("      - " + self._escape_yaml_value(str(link)))
            else:
                lines.append("    links: []")

            tags = feature.get('primary_tags', [])
            if tags:
                lines.append("    primary_tags:")
                for tag in tags:
                    if isinstance(tag, dict):
                        lines.append("      - name: " + self._escape_yaml_value(tag.get('name', '')))
                        lines.append("        confidence: " + str(tag.get('confidence', 0)))
                    else:
                        lines.append("      - " + self._escape_yaml_value(str(tag)))
            else:
                lines.append("    primary_tags: []")

            lines.append("")

        return '\n'.join(lines)

    def _escape_yaml_value(self, value: Any) -> str:
        if value is None:
            return '""'
        text = str(value)
        if any(char in text for char in [':', '-', '#', '{', '}', '[', ']', ',', '&', '*', '!', '|', '>', '\n', '"']):
            escaped = text.replace('"', '\\"')
            return f'"{escaped}"'
        return text
