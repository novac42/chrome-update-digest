#!/usr/bin/env python3
"""
Generate GitHub Pages dual navigation system for Chrome Release Digests.
Creates both version-centric and area-centric navigation structures.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple
from collections import defaultdict
try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

class GitHubPagesNavigationGenerator:
    def __init__(self, base_path: str = ".", language: str = "en"):
        self.base_path = Path(base_path)
        normalized_language = (language or "en").lower()
        if normalized_language not in {"en", "zh", "bilingual"}:
            normalized_language = "en"
        self.language_mode = normalized_language
        self.languages: List[str] = ["en", "zh"] if normalized_language == "bilingual" else [normalized_language]
        self.channel = "stable"
        self.source_dir = self.base_path / "digest_markdown" / "webplatform"
        self.digest_dir = self.base_path / "digest_markdown"
        self.versions_dir = self.digest_dir / "versions"  # default English output
        self.areas_dir = self.digest_dir / "areas"
        self.language_configs: Dict[str, Dict[str, Path]] = {}
        for lang in self.languages:
            suffix = "" if lang == "en" else f"-{lang}"
            self.language_configs[lang] = {
                "versions_dir": self.digest_dir / f"versions{suffix}",
                "areas_dir": self.digest_dir / f"areas{suffix}",
                "index_path": self.digest_dir / ("index.md" if suffix == "" else f"index{suffix}.md")
            }
        
        # Area metadata sourced from config/focus_areas.yaml
        self.area_metadata = self.load_focus_area_metadata()
        self.area_order = list(self.area_metadata.keys())
        
        # Fallback names for areas not yet in the config
        self.fallback_display_names = {
            "webrtc": "WebRTC"
        }

    @staticmethod
    def _trans(language: str, english: str, chinese: str) -> str:
        """Return content in the requested language."""
        return chinese if language == "zh" else english

    def load_focus_area_metadata(self) -> Dict[str, Dict[str, str]]:
        """Load area display metadata from the shared focus areas config."""
        metadata: Dict[str, Dict[str, str]] = {}
        config_path = self.base_path / "config" / "focus_areas.yaml"

        if not config_path.exists():
            return metadata

        if yaml:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}

            focus_areas = config.get("focus_areas", {})

            for area_key, attrs in focus_areas.items():
                display_name = attrs.get("name") or area_key.replace("-", " ").title()
                description = attrs.get("description", "").strip()
                metadata[area_key] = {
                    "name": display_name,
                    "description": description
                }

            return metadata

        return self._parse_focus_area_metadata_without_yaml(config_path)

    def _parse_focus_area_metadata_without_yaml(self, config_path: Path) -> Dict[str, Dict[str, str]]:
        """Fallback parser when PyYAML is unavailable."""
        metadata: Dict[str, Dict[str, str]] = {}
        current_area: Optional[str] = None
        in_focus_section = False

        with open(config_path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n")
                stripped = line.strip()

                if not stripped or stripped.startswith("#"):
                    continue

                if not in_focus_section:
                    if stripped in {"focus_areas:", "focus_areas"}:
                        in_focus_section = True
                    continue

                indent = len(line) - len(line.lstrip(" "))

                # Exit when we leave the focus_areas block
                if indent == 0:
                    break

                if indent == 2 and stripped.endswith(":"):
                    area_key = stripped[:-1]
                    current_area = area_key
                    metadata[current_area] = {
                        "name": area_key.replace("-", " ").title(),
                        "description": ""
                    }
                    continue

                if indent == 4 and current_area:
                    if stripped.startswith("name:"):
                        value = stripped.split("name:", 1)[1].strip().strip('"')
                        metadata[current_area]["name"] = value or metadata[current_area]["name"]
                    elif stripped.startswith("description:"):
                        value = stripped.split("description:", 1)[1].strip().strip('"')
                        metadata[current_area]["description"] = value

        return metadata

    def get_area_display_name(self, area_key: str) -> str:
        """Resolve the display name for an area."""
        if area_key in self.area_metadata:
            return self.area_metadata[area_key]["name"]
        if area_key in self.fallback_display_names:
            return self.fallback_display_names[area_key]
        return area_key.replace("-", " ").title()

    def get_area_description(self, area_key: str) -> str:
        """Resolve the marketing description for an area if present."""
        return self.area_metadata.get(area_key, {}).get("description", "")

    @staticmethod
    def pluralize(count: int, singular: str, plural: str = None) -> str:
        """Return the proper singular/plural label for a count."""
        if count == 1:
            return singular
        return plural if plural else f"{singular}s"

    def order_areas(self, areas: Iterable[str]) -> List[str]:
        """Order areas using the config ordering first, then alphabetically."""
        ordered: List[str] = []
        seen = set()

        for area_key in self.area_order:
            if area_key in areas:
                ordered.append(area_key)
                seen.add(area_key)

        for area_key in sorted(set(areas) - seen):
            ordered.append(area_key)

        return ordered
        
    def scan_content(self, languages: Optional[Iterable[str]] = None) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
        """Scan source directory to find all versions and areas for given languages."""
        langs = list(languages) if languages is not None else list(self.languages)
        version_areas = defaultdict(set)  # version -> set of areas
        area_versions = defaultdict(set)  # area -> set of versions

        if not self.source_dir.exists():
            print(f"Source directory {self.source_dir} does not exist")
            return version_areas, area_versions

        patterns = {
            lang: re.compile(
                rf"chrome-(\d+)-(\w+)-{re.escape(lang)}\.md$"
            )
            for lang in langs
        }

        for area_dir in self.source_dir.iterdir():
            if not area_dir.is_dir():
                continue

            area_name = area_dir.name

            for lang, pattern in patterns.items():
                for md_file in area_dir.glob(f"chrome-*-{lang}.md"):
                    match = pattern.match(md_file.name)
                    if not match:
                        continue

                    version, channel = match.groups()

                    if channel == self.channel:
                        version_areas[version].add(area_name)
                        area_versions[area_name].add(version)

        return dict(version_areas), dict(area_versions)
    
    def ensure_directories(self, config: Dict[str, Path]) -> None:
        """Create necessary directory structure for a specific language."""
        config["versions_dir"].mkdir(parents=True, exist_ok=True)
        config["areas_dir"].mkdir(parents=True, exist_ok=True)
        
    def write_single_language_page(self, source_file: Path, dest_file: Path) -> bool:
        """Copy a single-language digest into the navigation structure."""
        if not source_file.exists():
            return False
            
        # Read original content
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title from content
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else dest_file.stem
        
        # Add Jekyll front matter
        front_matter = f"""---
layout: default
title: {title}
---

"""
        
        # Write to destination
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(front_matter + content)
            
        return True


    def generate_version_pages(
        self,
        language: str,
        version_areas: Dict[str, Set[str]],
        config: Dict[str, Path]
    ) -> None:
        """Generate version-centric navigation pages for a language."""
        versions_dir = config["versions_dir"]
        versions = sorted(version_areas.keys(), reverse=True)

        title_value = self._trans(language, "Chrome Versions", "Chrome 各版本")
        index_lines = [
            "---",
            "layout: default",
            f"title: {title_value}",
            "---",
            "",
            f"# {self._trans(language, 'Chrome Release Digests by Version', '按版本浏览 Chrome 发布摘要')}",
            "",
            self._trans(
                language,
                "Browse Chrome release notes organized by version number.",
                "按版本号浏览整理后的 Chrome 发布说明。"
            ),
            "",
            f"## {self._trans(language, 'Available Versions', '可用版本')}",
            ""
        ]

        for version in versions:
            is_latest = version == versions[0]
            en_latest_badge = " **(Latest Stable)**" if is_latest else ""
            zh_latest_badge = " **（最新稳定版）**" if is_latest else ""
            areas_count = len(version_areas[version])
            area_label = self.pluralize(areas_count, "area")

            english_line = (
                f"- [Chrome {version}{en_latest_badge}](./chrome-{version}/) - "
                f"{areas_count} {area_label} with updates"
            )
            chinese_line = (
                f"- [Chrome {version}{zh_latest_badge}](./chrome-{version}/) - "
                f"包含 {areas_count} 个更新领域"
            )
            index_lines.append(self._trans(language, english_line, chinese_line))

        index_lines.append("")
        with open(versions_dir / "index.md", 'w', encoding='utf-8') as f:
            f.write("\n".join(index_lines).rstrip() + "\n")

        for version in versions:
            version_dir = versions_dir / f"chrome-{version}"
            version_dir.mkdir(exist_ok=True)

            overview_title = self._trans(
                language,
                f"Chrome {version} Release Notes",
                f"Chrome {version} 发布说明"
            )
            overview_lines = [
                "---",
                "layout: default",
                f"title: {overview_title}",
                "---",
                "",
                f"# {self._trans(language, f'Chrome {version} Release Notes', f'Chrome {version} 发布说明')}",
                "",
                self._trans(language, "[← Back to all versions](../)", "[← 返回所有版本](../)"),
                "",
                f"## {self._trans(language, 'Areas with Updates', '包含更新的领域')}",
                ""
            ]

            areas_for_version = self.order_areas(version_areas[version])

            for area in areas_for_version:
                display_name = self.get_area_display_name(area)
                description = self.get_area_description(area)
                description_suffix = f" — {description}" if description else ""

                english_bullet = f"- [{display_name}](./{area}.html){description_suffix}"
                chinese_bullet = f"- [{display_name}](./{area}.html){description_suffix}"
                overview_lines.append(self._trans(language, english_bullet, chinese_bullet))

                source_file = self.source_dir / area / f"chrome-{version}-{self.channel}-{language}.md"
                dest_file = version_dir / f"{area}.md"
                if not self.write_single_language_page(source_file, dest_file):
                    print(
                        f"Warning: missing digest for area '{area}' in Chrome {version} ({language}); "
                        "navigation entry will reference existing summaries only."
                    )

            overview_lines.append("")
            overview_lines.append(f"## {self._trans(language, 'Navigation', '页面导航')}")
            overview_lines.append("")

            version_idx = versions.index(version)
            if version_idx > 0:
                newer_version = versions[version_idx - 1]
                overview_lines.append(
                    self._trans(
                        language,
                        f"- [← Chrome {newer_version} (Newer)](../chrome-{newer_version}/)",
                        f"- [← Chrome {newer_version}（较新版本）](../chrome-{newer_version}/)"
                    )
                )
            if version_idx < len(versions) - 1:
                older_version = versions[version_idx + 1]
                overview_lines.append(
                    self._trans(
                        language,
                        f"- [Chrome {older_version} (Older) →](../chrome-{older_version}/)",
                        f"- [Chrome {older_version}（较旧版本） →](../chrome-{older_version}/)"
                    )
                )

            overview_lines.append(self._trans(language, "- [View all versions](../)", "- [查看全部版本](../)"))
            overview_lines.append(
                self._trans(language, "- [Browse by feature area](../../areas/)", "- [按功能领域浏览](../../areas/)")
            )

            with open(version_dir / "index.md", 'w', encoding='utf-8') as f:
                f.write("\n".join(overview_lines).rstrip() + "\n")


    def generate_area_pages(
        self,
        language: str,
        area_versions: Dict[str, Set[str]],
        config: Dict[str, Path]
    ) -> None:
        """Generate area-centric navigation pages for a language."""
        areas_dir = config["areas_dir"]
        areas = self.order_areas(area_versions.keys())

        title_value = self._trans(language, "Feature Areas", "功能领域")
        index_lines = [
            "---",
            "layout: default",
            f"title: {title_value}",
            "---",
            "",
            f"# {self._trans(language, 'Chrome Release Digests by Feature Area', '按功能领域浏览 Chrome 发布摘要')}",
            "",
            self._trans(
                language,
                "Browse Chrome release notes organized by feature area to track evolution over time.",
                "按功能领域查看 Chrome 更新，追踪功能演进。"
            ),
            "",
            f"## {self._trans(language, 'Available Feature Areas', '可用功能领域')}",
            ""
        ]

        for area in areas:
            display_name = self.get_area_display_name(area)
            description = self.get_area_description(area)
            versions_count = len(area_versions[area])
            versions_label = self.pluralize(versions_count, "version")
            description_suffix = f" — {description}" if description else ""

            english_line = (
                f"- [{display_name}](./{area}/) - Updates in {versions_count} {versions_label}{description_suffix}"
            )
            chinese_line = (
                f"- [{display_name}](./{area}/) - 在 {versions_count} 个版本中有更新{description_suffix}"
            )
            index_lines.append(self._trans(language, english_line, chinese_line))

        index_lines.append("")
        with open(areas_dir / "index.md", 'w', encoding='utf-8') as f:
            f.write("\n".join(index_lines).rstrip() + "\n")

        for area in areas:
            area_dir = areas_dir / area
            area_dir.mkdir(exist_ok=True)

            display_name = self.get_area_display_name(area)
            description = self.get_area_description(area)
            versions = sorted(area_versions[area], reverse=True)

            area_title = self._trans(language, f"{display_name} Updates", f"{display_name} 更新")
            hub_lines = [
                "---",
                "layout: default",
                f"title: {area_title}",
                "---",
                "",
                f"# {self._trans(language, f'{display_name} Updates', f'{display_name} 更新')}",
                "",
                self._trans(language, "[← Back to all areas](../)", "[← 返回所有领域](../)"),
                "",
                f"## {self._trans(language, 'Version History', '版本历史')}",
                "",
                self._trans(
                    language,
                    f"Track the evolution of {display_name} features across Chrome releases.",
                    f"追踪 {display_name} 在各个 Chrome 版本中的功能演进。"
                ),
                ""
            ]

            if description:
                hub_lines.append(description)
                hub_lines.append("")

            hub_lines.append(f"### {self._trans(language, 'Available Versions', '可用版本')}")
            hub_lines.append("")

            for version in versions:
                is_latest = version == versions[0]
                en_badge = " **(Latest)**" if is_latest else ""
                zh_badge = " **（最新）**" if is_latest else ""

                english_line = f"- [Chrome {version}{en_badge}](./chrome-{version}.html)"
                chinese_line = f"- [Chrome {version}{zh_badge}](./chrome-{version}.html)"
                hub_lines.append(self._trans(language, english_line, chinese_line))

                source_file = self.source_dir / area / f"chrome-{version}-{self.channel}-{language}.md"
                dest_file = area_dir / f"chrome-{version}.md"
                if not self.write_single_language_page(source_file, dest_file):
                    print(
                        f"Warning: missing digests for area '{area}' in Chrome {version} ({language}); skipping area detail copy."
                    )

            hub_lines.append("")
            hub_lines.append(f"## {self._trans(language, 'Navigation', '页面导航')}")
            hub_lines.append("")
            hub_lines.append(self._trans(language, "- [View all feature areas](../)", "- [查看全部领域](../)"))
            hub_lines.append(
                self._trans(language, "- [Browse by Chrome version](../../versions/)", "- [按 Chrome 版本浏览](../../versions/)")
            )

            with open(area_dir / "index.md", 'w', encoding='utf-8') as f:
                f.write("\n".join(hub_lines).rstrip() + "\n")


    def update_main_index(
        self,
        language: str,
        version_areas: Dict[str, Set[str]],
        area_versions: Dict[str, Set[str]],
        config: Dict[str, Path]
    ) -> None:
        """Update the language-specific main index."""
        versions = sorted(version_areas.keys(), reverse=True)
        areas = self.order_areas(area_versions.keys())
        top_areas = sorted(areas, key=lambda a: len(area_versions[a]), reverse=True)[:5]

        title_value = self._trans(language, "Chrome Release Digests", "Chrome 发布摘要")
        index_lines = [
            "---",
            "layout: default",
            f"title: {title_value}",
            "---",
            "",
            f"# {self._trans(language, 'Chrome Release Digests', 'Chrome 发布摘要')}",
            "",
            self._trans(
                language,
                "Comprehensive release notes for Chrome web platform features, organized for easy navigation.",
                "为 Chrome Web 平台功能提供结构化、易于浏览的发布摘要。"
            ),
            "",
            f"## {self._trans(language, 'Browse by Version', '按版本浏览')}",
            "",
            self._trans(language, "Explore what's new in each Chrome release:", "查看每个 Chrome 版本的新变化："),
            ""
        ]

        for version in versions[:3]:
            is_latest = version == versions[0]
            en_badge = " **(Latest Stable)**" if is_latest else ""
            zh_badge = " **（最新稳定版）**" if is_latest else ""
            areas_count = len(version_areas[version])
            area_label = self.pluralize(areas_count, "area")

            english_line = (
                f"- [Chrome {version}{en_badge}](./versions/chrome-{version}/) - "
                f"{areas_count} {area_label} with updates"
            )
            chinese_line = (
                f"- [Chrome {version}{zh_badge}](./versions/chrome-{version}/) - "
                f"包含 {areas_count} 个更新领域"
            )
            index_lines.append(self._trans(language, english_line, chinese_line))

        index_lines.append(
            self._trans(
                language,
                f"- [View all {len(versions)} versions →](./versions/)",
                f"- [查看全部 {len(versions)} 个版本 →](./versions/)"
            )
        )
        index_lines.append("")

        index_lines.append(f"## {self._trans(language, 'Browse by Feature Area', '按功能领域浏览')}")
        index_lines.append("")
        index_lines.append(
            self._trans(
                language,
                "Track the evolution of specific features across Chrome versions:",
                "追踪特定功能在不同 Chrome 版本中的演进："
            )
        )
        index_lines.append("")

        for area in top_areas:
            display_name = self.get_area_display_name(area)
            versions_count = len(area_versions[area])
            versions_label = self.pluralize(versions_count, "version")

            english_line = (
                f"- [{display_name}](./areas/{area}/) - Updates in {versions_count} {versions_label}"
            )
            chinese_line = (
                f"- [{display_name}](./areas/{area}/) - 在 {versions_count} 个版本中有更新"
            )
            index_lines.append(self._trans(language, english_line, chinese_line))

        index_lines.append(
            self._trans(
                language,
                f"- [View all {len(areas)} feature areas →](./areas/)",
                f"- [查看全部 {len(areas)} 个功能领域 →](./areas/)"
            )
        )
        index_lines.append("")

        latest_version = versions[0] if versions else ""
        top_area_names = [self.get_area_display_name(area) for area in top_areas[:3]]

        index_lines.append(f"## {self._trans(language, 'Quick Links', '快速入口')}")
        index_lines.append("")
        index_lines.append(
            self._trans(
                language,
                f"- **Latest Release**: [Chrome {latest_version}](./versions/chrome-{latest_version}/)",
                f"- **最新版本**：[Chrome {latest_version}](./versions/chrome-{latest_version}/)"
            )
        )
        index_lines.append(
            self._trans(
                language,
                f"- **Most Active Areas**: {', '.join(top_area_names)}",
                f"- **最活跃的领域**：{', '.join(top_area_names)}"
            )
        )
        index_lines.append(
            self._trans(
                language,
                "- **All Versions**: [Browse every release](./versions/)",
                "- **全部版本**：[查看所有发布](./versions/)"
            )
        )
        index_lines.append(
            self._trans(
                language,
                "- **All Areas**: [Explore feature areas](./areas/)",
                "- **全部领域**：[浏览功能领域](./areas/)"
            )
        )
        index_lines.append(
            self._trans(
                language,
                "- **Search**: Use browser search (Ctrl+F) on any page",
                "- **搜索**：在任意页面使用浏览器搜索（Ctrl+F）"
            )
        )
        index_lines.append("")

        index_lines.append(f"## {self._trans(language, 'About', '关于')}")
        index_lines.append("")
        index_lines.append(
            self._trans(
                language,
                "This site provides structured, searchable release notes for Chrome's web platform features. Content is automatically generated from official Chrome release notes and organized for developer convenience.",
                "本站提供结构化、可搜索的 Chrome Web 平台更新摘要，内容根据官方发布说明自动生成，方便开发者查阅。"
            )
        )
        index_lines.append("")
        index_lines.append(f"### {self._trans(language, 'Navigation Tips', '导航提示')}")
        index_lines.append("")
        index_lines.append(
            self._trans(
                language,
                "- **By Version**: See all changes in a specific Chrome release",
                "- **按版本**：查看某个 Chrome 版本的全部更新"
            )
        )
        index_lines.append(
            self._trans(
                language,
                "- **By Area**: Track how a feature area evolves over time",
                "- **按领域**：追踪特定功能领域的演进"
            )
        )
        index_lines.append(
            self._trans(
                language,
                "- **Breadcrumbs**: Use navigation links on each page to explore related content",
                "- **面包屑导航**：使用页面上的导航链接继续探索"
            )
        )
        index_lines.append("")
        index_lines.append(f"### {self._trans(language, 'Update Frequency', '更新频率')}")
        index_lines.append("")
        index_lines.append(
            self._trans(
                language,
                "New Chrome stable releases are typically published every 4 weeks. This site is updated shortly after each stable release.",
                "Chrome 稳定版通常每 4 周发布一次，本网站会在稳定版发布后尽快更新。"
            )
        )
        index_lines.append("")
        index_lines.append("---")
        index_lines.append("")
        index_lines.append(
            self._trans(
                language,
                "*Generated from [Chrome Release Notes](https://developer.chrome.com/release-notes/)*",
                "*内容来源：[Chrome 发布说明](https://developer.chrome.com/release-notes/)*"
            )
        )

        if self.language_mode == 'bilingual' and language == 'en':
            index_lines.append("")
            index_lines.append("## Other Languages")
            index_lines.append("")
            index_lines.append("- [中文版](./index-zh.md)")
        elif self.language_mode == 'bilingual' and language == 'zh':
            index_lines.append("")
            index_lines.append("## 其他语言")
            index_lines.append("")
            index_lines.append("- [English](./index.md)")

        with open(config["index_path"], 'w', encoding='utf-8') as f:
            f.write("\n".join(index_lines).rstrip() + "\n")

    def generate_jekyll_config(self):
        """Update Jekyll configuration for GitHub Pages."""
        config = {
            'title': 'Chrome Release Digests',
            'description': 'Comprehensive Chrome web platform release notes with version selection',
            'theme': 'minima',
            'plugins': ['jekyll-feed', 'jekyll-sitemap'],
            'defaults': [
                {
                    'scope': {
                        'path': '',
                        'type': 'pages'
                    },
                    'values': {
                        'layout': 'default'
                    }
                }
            ]
        }
        
        config_path = self.digest_dir / "_config.yml"
        if yaml:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            content_lines = [
                "title: Chrome Release Digests",
                "description: Comprehensive Chrome web platform release notes with version selection",
                "theme: minima",
                "plugins:",
                "  - jekyll-feed",
                "  - jekyll-sitemap",
                "defaults:",
                "  - scope:",
                "      path: ''",
                "      type: pages",
                "    values:",
                "      layout: default",
            ]
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(content_lines) + "\n")
            
    def clean_old_structure(self):
        """Preserve source digests for reuse in future runs."""
        print("Preserving digest_markdown/webplatform for subsequent orchestrations")
            
    def run(self) -> bool:
        """Execute the navigation generation workflow."""
        print("Starting GitHub Pages navigation generation...")
        processed: List[Tuple[str, Dict[str, Set[str]], Dict[str, Set[str]]]] = []

        for language in self.languages:
            print(f"\n[{language}] Scanning source content...")
            version_areas, area_versions = self.scan_content([language])

            if not version_areas:
                print(f"[{language}] No digests found; skipping this language")
                continue

            print(f"[{language}] Found {len(version_areas)} versions and {len(area_versions)} areas")
            config = self.language_configs[language]

            print(f"[{language}] Creating directory structure...")
            self.ensure_directories(config)

            print(f"[{language}] Generating version-centric pages...")
            self.generate_version_pages(language, version_areas, config)

            print(f"[{language}] Generating area-centric pages...")
            self.generate_area_pages(language, area_versions, config)

            print(f"[{language}] Updating index page...")
            self.update_main_index(language, version_areas, area_versions, config)

            processed.append((language, version_areas, area_versions))

        if not processed:
            print("No digest content found for requested language mode.")
            return False

        print("\nUpdating Jekyll configuration...")
        self.generate_jekyll_config()

        print("Cleaning old structure...")
        self.clean_old_structure()

        print("\nGeneration complete!")
        print(f"- Languages processed: {', '.join(lang for lang, _, _ in processed)}")
        for lang, v_areas, a_areas in processed:
            print(f"  · {lang}: {len(v_areas)} versions, {len(a_areas)} areas")
        print(f"- Language mode: {self.language_mode}")
        print(f"- Output root: {self.digest_dir}")

        return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate GitHub Pages navigation for Chrome Release Digests')
    parser.add_argument('--base-path', default='.', help='Base path of the project')
    parser.add_argument('--clean', action='store_true', help='Clean existing structure before generating')
    parser.add_argument(
        '--language',
        default='en',
        choices=['en', 'zh', 'bilingual'],
        help='Language variant to use as the source for navigation content'
    )

    args = parser.parse_args()

    selected_language = args.language.lower()

    generator = GitHubPagesNavigationGenerator(args.base_path, selected_language)
    
    if args.clean:
        print("Cleaning existing structure...")
        for cfg in generator.language_configs.values():
            versions_dir = cfg["versions_dir"]
            areas_dir = cfg["areas_dir"]
            index_path = cfg["index_path"]
            if versions_dir.exists():
                shutil.rmtree(versions_dir)
            if areas_dir.exists():
                shutil.rmtree(areas_dir)
            if index_path.exists():
                index_path.unlink()
            
    success = generator.run()
    
    if success:
        print("\n✅ Successfully generated GitHub Pages navigation structure")
        print("\nTo preview locally:")
        print("  cd digest_markdown")
        print("  jekyll serve")
        print("\nThen visit http://localhost:4000")
    else:
        print("\n❌ Generation failed")
        return 1
        
    return 0


if __name__ == '__main__':
    exit(main())
