#!/usr/bin/env python3
"""
Profile Features Extractor
从Chrome Enterprise Release Notes中提取与profile相关的功能特性
基于 prompts/profile-keywords.txt 中定义的关键词
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from datetime import datetime

# 重用已有的Feature数据结构
sys.path.append(str(Path(__file__).parent.parent))
from process_enterprise_release_note import (
    Feature, 
    EnterpriseReleaseNotesProcessor as ReleaseNotesProcessorV2
)


@dataclass
class ProfileFeature:
    """Profile相关的特性，继承自Feature并添加匹配信息"""
    feature: Feature
    matched_keywords: List[str]
    relevance_score: float
    match_context: str  # 匹配到关键词的上下文


class ProfileFeatureExtractor:
    """Profile特性提取器"""
    
    def __init__(self, keywords_file: str = None):
        """初始化提取器"""
        self.keywords_file = keywords_file or self._get_default_keywords_file()
        self.profile_keywords = self._load_keywords()
        self.processor = ReleaseNotesProcessorV2()
        
    def _get_default_keywords_file(self) -> str:
        """获取默认关键词文件路径"""
        base_path = Path(__file__).parent.parent
        return str(base_path / "prompts" / "profile-keywords.txt")
    
    def _load_keywords(self) -> str:
        """加载profile关键词"""
        try:
            with open(self.keywords_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找核心关键词组合行
            for line in content.split('\n'):
                line = line.strip()
                if not line.startswith('#') and '|' in line and 'profile' in line.lower():
                    print(f"Loaded profile keywords: {line}")
                    return line
            
            # 如果没找到，使用默认关键词
            default_keywords = "profile|Profile|account|Account|identity|Identity|sync|Sync|sign-in|signin|multiple.*account|separate.*profile|data.*separation"
            print(f"Using default keywords: {default_keywords}")
            return default_keywords
            
        except FileNotFoundError:
            print(f"Warning: Keywords file not found: {self.keywords_file}")
            default_keywords = "profile|Profile|account|Account|identity|Identity|sync|Sync|sign-in|signin"
            print(f"Using fallback keywords: {default_keywords}")
            return default_keywords
    
    def _calculate_relevance_score(self, feature: Feature, matched_keywords: List[str], 
                                 match_context: str) -> float:
        """计算特性与profile的相关性得分"""
        score = 0.0
        
        # 基础匹配得分 - 每个关键词匹配加分
        score += len(matched_keywords) * 10
        
        # 标题中的匹配权重更高
        title_lower = feature.title.lower()
        for keyword in matched_keywords:
            if keyword.lower() in title_lower:
                score += 20
        
        # 特定高价值关键词加分
        high_value_keywords = ['profile', 'multiple.*account', 'separate.*profile', 'data.*separation']
        for hvk in high_value_keywords:
            if any(re.search(hvk, kw, re.IGNORECASE) for kw in matched_keywords):
                score += 15
        
        # 管理类别的profile功能通常更重要
        if "Management" in feature.categories:
            score += 10
        
        # 描述长度影响（更详细的描述通常更重要）
        if len(feature.description) > 200:
            score += 5
        
        return score
    
    def _extract_match_context(self, text: str, keyword: str, context_length: int = 100) -> str:
        """提取关键词匹配的上下文"""
        pattern = re.compile(f'({re.escape(keyword)})', re.IGNORECASE)
        match = pattern.search(text)
        
        if match:
            start = max(0, match.start() - context_length)
            end = min(len(text), match.end() + context_length)
            context = text[start:end].strip()
            
            # 高亮匹配的关键词
            context = pattern.sub(r'**\1**', context)
            return context
        
        return ""
    
    def _is_profile_related(self, feature: Feature) -> tuple[bool, List[str], str]:
        """判断feature是否与profile相关"""
        # 组合所有文本进行搜索
        search_text = f"{feature.title} {feature.description}"
        
        # 查找匹配的关键词
        matched_keywords = []
        match_contexts = []
        
        # 将关键词模式分割并逐一匹配
        keyword_patterns = self.profile_keywords.split('|')
        
        for pattern in keyword_patterns:
            pattern = pattern.strip()
            if not pattern:
                continue
                
            # 搜索匹配
            matches = re.finditer(pattern, search_text, re.IGNORECASE)
            for match in matches:
                matched_keyword = match.group()
                if matched_keyword not in matched_keywords:
                    matched_keywords.append(matched_keyword)
                    context = self._extract_match_context(search_text, matched_keyword)
                    if context:
                        match_contexts.append(context)
        
        # 如果有匹配的关键词，则认为是profile相关
        is_related = len(matched_keywords) > 0
        context = " | ".join(match_contexts[:3])  # 最多显示3个上下文
        
        return is_related, matched_keywords, context
    
    def extract_from_processed_features(self, features: Dict[str, Feature]) -> List[ProfileFeature]:
        """从已处理的features中提取profile相关特性"""
        profile_features = []
        
        for feature_name, feature in features.items():
            is_related, matched_keywords, context = self._is_profile_related(feature)
            
            if is_related:
                # 计算相关性得分
                score = self._calculate_relevance_score(feature, matched_keywords, context)
                
                profile_feature = ProfileFeature(
                    feature=feature,
                    matched_keywords=matched_keywords,
                    relevance_score=score,
                    match_context=context
                )
                profile_features.append(profile_feature)
                
                print(f"Found profile feature: {feature_name} (score: {score:.1f})")
                print(f"  Keywords: {matched_keywords}")
                print(f"  Context: {context[:100]}...")
        
        # 按相关性得分排序
        profile_features.sort(key=lambda x: x.relevance_score, reverse=True)
        return profile_features
    
    def parse_processed_file(self, file_path: str) -> Dict[str, Feature]:
        """解析已处理的markdown文件"""
        features = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取版本号
        version_match = re.search(r'Chrome (\d+)', content)
        chrome_version = int(version_match.group(1)) if version_match else 138
        
        # 解析features
        # 按 ### 分割sections
        sections = re.split(r'^### (.+)$', content, flags=re.MULTILINE)
        
        current_category = None
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                category = sections[i].strip()
                section_content = sections[i + 1].strip()
                
                if category in ["User productivity/Apps", "Security/Privacy", "Management"]:
                    current_category = category
                    
                    # 解析这个category下的features
                    features.update(self._parse_category_features(section_content, current_category, chrome_version))
        
        return features
    
    def _parse_category_features(self, content: str, category: str, chrome_version: int) -> Dict[str, Feature]:
        """解析单个category下的features"""
        features = {}
        
        # 按 * ** 分割features
        feature_blocks = re.split(r'\n\* \*\*(.+?)\*\*', content)
        
        for i in range(1, len(feature_blocks), 2):
            if i + 1 < len(feature_blocks):
                title = feature_blocks[i].strip()
                feature_content = feature_blocks[i + 1].strip()
                
                # 确定状态
                status = "upcoming" if "Upcoming" in content[:200] else "current"
                
                # 解析feature内容
                feature = self._parse_single_feature(title, feature_content, category, status, chrome_version)
                if feature:
                    features[title] = feature
        
        return features
    
    def _parse_single_feature(self, title: str, content: str, category: str, 
                            status: str, chrome_version: int) -> Optional[Feature]:
        """解析单个feature"""
        try:
            # 提取类型
            type_match = re.search(r'• Type: (.+)', content)
            change_type = type_match.group(1) if type_match else "Chrome Browser changes"
            
            # 提取平台
            platform_match = re.search(r'• Platform: (.+)', content)
            platforms = []
            if platform_match:
                platform_text = platform_match.group(1)
                # 解析平台信息
                desktop_match = re.search(r'Desktop \(([^)]+)\)', platform_text)
                mobile_match = re.search(r'Mobile \(([^)]+)\)', platform_text)
                
                if desktop_match:
                    platforms.extend([p.strip() for p in desktop_match.group(1).split(',')])
                if mobile_match:
                    platforms.extend([p.strip() for p in mobile_match.group(1).split(',')])
            
            # 提取描述
            update_match = re.search(r'• Update: (.+)', content, re.DOTALL)
            description = update_match.group(1).strip() if update_match else ""
            
            # 提取policy
            policy_match = re.search(r'`([A-Za-z]+[A-Za-z0-9]*)`', description)
            policy = policy_match.group(1) if policy_match else None
            
            # 提取版本信息
            version_info = None
            if status == "upcoming":
                version_match = re.search(r'Chrome (\d+)', description)
                if version_match:
                    version_info = f"Chrome {version_match.group(1)}"
            
            feature = Feature(
                title=title,
                change_type=change_type,
                categories=[category],
                status=status,
                platforms=platforms,
                description=description,
                policy=policy,
                version_info=version_info
            )
            
            return feature
            
        except Exception as e:
            print(f"Error parsing feature '{title}': {e}")
            return None
    
    def process_release_notes(self, file_path: str) -> List[ProfileFeature]:
        """处理已处理的release notes文件并提取profile相关特性"""
        print(f"Processing processed file: {file_path}")
        
        # 解析已处理的markdown文件
        features = self.parse_processed_file(file_path)
        
        print(f"Total features found: {len(features)}")
        
        # 提取profile相关特性
        profile_features = self.extract_from_processed_features(features)
        
        print(f"Profile-related features found: {len(profile_features)}")
        return profile_features
    
    def generate_profile_report(self, profile_features: List[ProfileFeature], 
                              chrome_version: int = None) -> str:
        """生成profile特性报告"""
        if not chrome_version:
            chrome_version = self.processor.current_version or "Unknown"
        
        # 生成报告
        report = []
        report.append(f"# Chrome {chrome_version} Profile-Related Features Report")
        report.append(f"")
        report.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report.append(f"")
        report.append(f"## Summary")
        report.append(f"")
        report.append(f"- **Total features analyzed**: {len(self.processor.features)}")
        report.append(f"- **Profile-related features found**: {len(profile_features)}")
        report.append(f"- **Keywords used**: `{self.profile_keywords}`")
        report.append(f"")
        
        if not profile_features:
            report.append("No profile-related features found in this release.")
            return '\n'.join(report)
        
        # 按类别组织特性
        categories = {
            "User productivity/Apps": [],
            "Security/Privacy": [],
            "Management": []
        }
        
        for pf in profile_features:
            for category in pf.feature.categories:
                if category in categories:
                    categories[category].append(pf)
        
        # 处理没有分类或不在主要分类中的特性
        uncategorized = []
        for pf in profile_features:
            if not pf.feature.categories or not any(cat in categories for cat in pf.feature.categories):
                uncategorized.append(pf)
        
        # 生成各个分类的报告
        for category, features in categories.items():
            if not features:
                continue
                
            report.append(f"## {category}")
            report.append(f"")
            
            for pf in sorted(features, key=lambda x: x.relevance_score, reverse=True):
                report.append(self._format_profile_feature(pf))
                report.append("")
        
        # 处理未分类的特性
        if uncategorized:
            report.append(f"## Other Profile Features")
            report.append(f"")
            
            for pf in sorted(uncategorized, key=lambda x: x.relevance_score, reverse=True):
                report.append(self._format_profile_feature(pf))
                report.append("")
        
        # 添加关键词统计
        report.append(f"## Keyword Analysis")
        report.append(f"")
        
        # 统计关键词频率
        keyword_counts = {}
        for pf in profile_features:
            for keyword in pf.matched_keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # 按频率排序
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        
        report.append("| Keyword | Frequency |")
        report.append("|---------|-----------|")
        for keyword, count in sorted_keywords:
            report.append(f"| {keyword} | {count} |")
        
        return '\n'.join(report)
    
    def _format_profile_feature(self, pf: ProfileFeature) -> str:
        """格式化单个profile特性"""
        feature = pf.feature
        
        lines = []
        lines.append(f"### {feature.title}")
        lines.append(f"")
        lines.append(f"**Relevance Score**: {pf.relevance_score:.1f}")
        lines.append(f"")
        lines.append(f"**Type**: {feature.change_type}")
        
        if feature.platforms:
            platform_info = self._format_platforms(feature.platforms)
            lines.append(f"**Platform**: {platform_info}")
        
        lines.append(f"**Status**: {feature.status.title()}")
        
        if feature.categories:
            lines.append(f"**Categories**: {', '.join(feature.categories)}")
        
        if pf.matched_keywords:
            lines.append(f"**Matched Keywords**: {', '.join(pf.matched_keywords)}")
        
        lines.append(f"")
        lines.append(f"**Description**:")
        lines.append(f"{feature.description}")
        
        if pf.match_context:
            lines.append(f"")
            lines.append(f"**Key Context**: {pf.match_context}")
        
        if feature.policy:
            lines.append(f"")
            lines.append(f"**Related Policy**: `{feature.policy}`")
        
        if feature.version_info:
            lines.append(f"")
            lines.append(f"**Version Info**: {feature.version_info}")
        
        return '\n'.join(lines)
    
    def _format_platforms(self, platforms: List[str]) -> str:
        """格式化平台信息"""
        desktop_platforms = []
        mobile_platforms = []
        
        platform_mapping = {
            'Windows': 'desktop', 'macOS': 'desktop', 'Linux': 'desktop', 'ChromeOS': 'desktop',
            'Android': 'mobile', 'iOS': 'mobile'
        }
        
        for platform in platforms:
            if platform_mapping.get(platform) == 'desktop':
                desktop_platforms.append(platform)
            elif platform_mapping.get(platform) == 'mobile':
                mobile_platforms.append(platform)
        
        platform_parts = []
        if desktop_platforms:
            platform_parts.append(f"Desktop ({', '.join(sorted(desktop_platforms))})")
        if mobile_platforms:
            platform_parts.append(f"Mobile ({', '.join(sorted(mobile_platforms))})")
        
        return ', '.join(platform_parts) if platform_parts else 'All platforms'


def find_processed_files():
    """查找已处理的文件"""
    base_path = Path("/Users/lyzh/Documents/Nova_Projects/chrome-update-digest")
    processed_dir = base_path / "upstream_docs" / "processed_forenterprise"
    
    processed_files = {}
    for file in processed_dir.glob("*-organized_chromechanges-enterprise.md"):
        # 提取版本号
        match = re.search(r'^(\d+)-organized_chromechanges-enterprise\.md$', file.name)
        if match:
            version = int(match.group(1))
            processed_files[version] = file
    
    return processed_files


def main():
    parser = argparse.ArgumentParser(description='Extract profile-related features from Chrome Enterprise release notes')
    parser.add_argument('version', nargs='?', type=int, help='Chrome version to process (e.g., 137, 138)')
    parser.add_argument('--all', action='store_true', help='Process all available versions')
    parser.add_argument('--keywords', help='Path to keywords file (default: prompts/profile-keywords.txt)')
    parser.add_argument('--output', help='Output directory (default: profile_reports/)')
    parser.add_argument('--list', action='store_true', help='List available versions')
    
    args = parser.parse_args()
    
    # 查找已处理的文件
    processed_files = find_processed_files()
    
    if args.list:
        if processed_files:
            print("Available processed Chrome versions:")
            for version in sorted(processed_files.keys()):
                print(f"  - Chrome {version}: {processed_files[version].name}")
        else:
            print("No processed files found.")
        return
    
    # 确定要处理的版本
    versions_to_process = []
    if args.version:
        if args.version in processed_files:
            versions_to_process = [args.version]
        else:
            print(f"Error: Chrome {args.version} processed file not found.")
            print(f"Available versions: {sorted(processed_files.keys())}")
            sys.exit(1)
    elif args.all:
        versions_to_process = sorted(processed_files.keys())
    else:
        # 默认处理最新版本
        if processed_files:
            latest_version = max(processed_files.keys())
            versions_to_process = [latest_version]
            print(f"No version specified. Processing latest: Chrome {latest_version}")
        else:
            print("No processed files found.")
            return
    
    # 设置输出目录
    output_dir = Path(args.output) if args.output else Path("profile_reports")
    output_dir.mkdir(exist_ok=True)
    
    # 创建提取器
    extractor = ProfileFeatureExtractor(keywords_file=args.keywords)
    
    # 处理每个版本
    for version in versions_to_process:
        input_file = processed_files[version]
        output_file = output_dir / f"chrome-{version}-profile-features.md"
        
        print(f"\n{'='*60}")
        print(f"Processing Chrome {version}")
        print(f"Input: {input_file}")
        print(f"Output: {output_file}")
        print(f"{'='*60}")
        
        try:
            # 提取profile相关特性
            profile_features = extractor.process_release_notes(str(input_file))
            
            # 生成报告
            report = extractor.generate_profile_report(profile_features, version)
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"✅ Profile report generated: {output_file.name}")
            print(f"✅ Found {len(profile_features)} profile-related features")
            
            if profile_features:
                print(f"✅ Top features by relevance:")
                for i, pf in enumerate(profile_features[:3], 1):
                    print(f"   {i}. {pf.feature.title} (score: {pf.relevance_score:.1f})")
            
        except Exception as e:
            print(f"❌ Error processing Chrome {version}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 Profile feature extraction complete!")
    print(f"[DIR] Reports saved to: {output_dir}")


if __name__ == "__main__":
    main()