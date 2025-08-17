#!/usr/bin/env python3
"""
Chrome Enterprise Release Notes Processor V2
支持多种格式的自动检测和处理
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class Feature:
    """Chrome feature数据结构"""
    title: str
    change_type: str  # "Chrome Browser changes", "Chrome Enterprise Core changes", etc.
    categories: List[str]  # ["Security/Privacy", "User productivity/Apps", "Management"]
    status: str  # "current" or "upcoming"
    platforms: List[str] = field(default_factory=list)
    description: str = ""
    policy: Optional[str] = None
    version_info: Optional[str] = None
    source_format: str = ""  # "current" or "history"


class ReleaseNotesFormatDetector:
    """Release Notes格式检测器"""
    
    def detect_format(self, content: str) -> str:
        """
        检测release notes格式
        返回: 'current' 或 'history'
        """
        # 1. 检查表格复杂度 - History格式有24+列
        complex_table = re.search(r'\|([^|\n]+\|){20,}', content)
        if complex_table:
            return 'history'
        
        # 2. 检查是否有### feature headers - Current格式特征
        feature_headers = re.findall(r'^### [^#].*$', content, re.MULTILINE)
        simple_table = re.search(r'\| Feature \| Security/Privacy \|', content)
        
        if feature_headers and simple_table:
            return 'current'
        
        # 3. 检查是否有标准的三列表格
        standard_table_pattern = r'\|\s*Feature\s*\|\s*Security/Privacy\s*\|\s*User productivity/Apps\s*\|\s*Management\s*\|'
        if re.search(standard_table_pattern, content, re.IGNORECASE):
            return 'current'
        
        # 4. 默认fallback逻辑 - 基于feature headers的存在
        return 'history' if not feature_headers else 'current'


class ReleaseNotesParser(ABC):
    """Release Notes解析器基类"""
    
    @abstractmethod
    def extract_version(self, content: str) -> Optional[int]:
        """提取Chrome版本号"""
        pass
    
    @abstractmethod
    def categorize_features(self, content: str) -> Dict[str, Dict]:
        """从表格提取feature分类信息"""
        pass
    
    @abstractmethod
    def parse_features(self, content: str, feature_info: Dict[str, Dict]) -> Dict[str, Feature]:
        """解析所有features"""
        pass
    
    def identify_upcoming_features(self, content: str) -> Set[str]:
        """识别upcoming features - 通用实现"""
        upcoming = set()
        lines = content.split('\n')
        
        in_upcoming = False
        for line in lines:
            # 检查upcoming section标记
            if re.match(r'^#+.*\b(upcoming|coming soon)\b', line, re.IGNORECASE):
                in_upcoming = True
                continue
            
            # 检查返回到current features或文档结束
            if in_upcoming and (re.match(r'^## (?!.*upcoming)(?!.*coming soon)', line, re.IGNORECASE) or 
                               line.startswith('## Download Release Notes')):
                in_upcoming = False
            
            # 提取upcoming section中的feature标题
            if in_upcoming and (line.startswith('### ') or line.startswith('#### ')):
                title = line.replace('### ', '').replace('#### ', '').strip()
                title = title.lstrip('#').strip()
                if title not in ['Upcoming Chrome browser changes', 'Chrome browser changes']:
                    upcoming.add(title)
        
        return upcoming


class CurrentReleaseParser(ReleaseNotesParser):
    """Current Release格式解析器 (Chrome 138+)"""
    
    def extract_version(self, content: str) -> Optional[int]:
        """提取版本号"""
        match = re.search(r'## Chrome (\d+) release summary', content)
        if match:
            return int(match.group(1))
        return None
    
    def categorize_features(self, content: str) -> Dict[str, Dict]:
        """解析简单表格格式"""
        feature_info = {}
        lines = content.split('\n')
        
        current_section = None
        current_status = "current"
        in_table = False
        
        for i, line in enumerate(lines):
            # 跟踪当前section
            if '## Chrome browser changes' in line:
                current_section = "Chrome Browser changes"
            elif '## Chrome Enterprise Core changes' in line:
                current_section = "Chrome Enterprise Core changes"
            elif '## Chrome Enterprise Premium changes' in line:
                current_section = "Chrome Enterprise Premium changes"
            
            # 检测upcoming sections
            if re.match(r'^#+.*\b(upcoming|coming soon)\b', line, re.IGNORECASE):
                current_status = "upcoming"
            elif re.match(r'^## (?!.*upcoming)(?!.*coming soon)', line, re.IGNORECASE):
                current_status = "current"
            
            # 检测表格头
            if '| Feature |' in line and 'Security/Privacy' in line:
                in_table = True
                continue
            
            # 跳过表格分隔符
            if '|---------|' in line or '|:-------' in line:
                continue
            
            # 表格结束
            if in_table and (not line.strip() or line.startswith('#')):
                in_table = False
                continue
            
            # 解析表格行
            if in_table and '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5:  # 有效表格行
                    # 提取feature名称
                    feature_match = re.search(r'\[([^\]]+)\]|\*\*([^*]+)\*\*|([^|#*\[\]]+)', parts[1])
                    if feature_match:
                        feature_name = (feature_match.group(1) or 
                                      feature_match.group(2) or 
                                      feature_match.group(3)).strip()
                        if feature_name:
                            categories = []
                            
                            # 检查分类标记
                            if '✓' in parts[2]:
                                categories.append("Security/Privacy")
                            if '✓' in parts[3]:
                                categories.append("User productivity/Apps")
                            if '✓' in parts[4]:
                                categories.append("Management")
                            
                            feature_info[feature_name] = {
                                'categories': categories,
                                'change_type': current_section or "Chrome Browser changes",
                                'status': current_status
                            }
        
        return feature_info
    
    def parse_features(self, content: str, feature_info: Dict[str, Dict]) -> Dict[str, Feature]:
        """基于### headers解析features"""
        features = {}
        upcoming_features = self.identify_upcoming_features(content)
        
        # 查找所有### headers
        for match in re.finditer(r'^###\s*(.+)$', content, re.MULTILINE):
            title = match.group(1).strip()
            
            # 跳过section headers
            skip_titles = [
                'Chrome browser changes',
                'Chrome Enterprise Core changes', 
                'Chrome Enterprise Premium changes'
            ]
            if title in skip_titles:
                continue
            
            feature = self._extract_feature_from_section(
                title, content, match.start(), feature_info, upcoming_features
            )
            if feature:
                feature.source_format = "current"
                features[title] = feature
        
        return features
    
    def _extract_feature_from_section(self, title: str, content: str, start_pos: int,
                                    feature_info: Dict, upcoming_features: Set[str]) -> Optional[Feature]:
        """从section提取feature信息"""
        # 查找feature内容
        lines = content[start_pos:].split('\n')
        feature_text = []
        
        for line in lines[1:]:  # 跳过标题行
            # 停在下一个feature或major section
            if line.startswith('###') or line.startswith('##'):
                break
            feature_text.append(line)
        
        # 确定状态
        status = "upcoming" if title in upcoming_features else "current"
        if title in feature_info and 'status' in feature_info[title]:
            status = feature_info[title]['status']
        
        # 创建feature对象
        feature = Feature(
            title=title,
            change_type="Chrome Browser changes",
            categories=[],
            status=status
        )
        
        # 使用表格信息
        if title in feature_info:
            feature.categories = feature_info[title]['categories']
            feature.change_type = feature_info[title]['change_type']
        
        # 解析内容
        full_text = '\n'.join(feature_text)
        feature.platforms = self._extract_platforms(full_text)
        feature.policy = self._extract_policy(full_text)
        feature.description = self._extract_description(feature_text)
        
        # 提取版本信息
        if feature.status == "upcoming":
            version_match = re.search(r'Chrome (\d+)', full_text)
            if version_match:
                feature.version_info = f"Chrome {version_match.group(1)}"
        
        return feature
    
    def _extract_platforms(self, text: str) -> List[str]:
        """提取平台信息"""
        platforms = []
        known_platforms = ['Android', 'ChromeOS', 'Linux', 'macOS', 'Windows', 'iOS']
        
        for platform in known_platforms:
            patterns = [
                rf'Chrome \d+ on .*\b{platform}\b',
                rf'\*\*Chrome \d+ on .*\b{platform}\b\*\*',
                rf'- \*?Chrome \d+ on .*\b{platform}\b',
            ]
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    if platform not in platforms:
                        platforms.append(platform)
                    break
        
        return platforms
    
    def _extract_policy(self, text: str) -> Optional[str]:
        """提取策略信息"""
        policy_patterns = [
            r'\[([A-Za-z]+[A-Za-z0-9]*)\]\(https://chromeenterprise\.google/policies/#',
            r'policy,?\s*\[([A-Za-z]+[A-Za-z0-9]*)\]',
            r'controlled by(?: the)?\s*\[([A-Za-z]+[A-Za-z0-9]*)\]',
            r'using(?: the)?\s*\[([A-Za-z]+[A-Za-z0-9]*)\]\s*policy',
        ]
        
        for pattern in policy_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_description(self, feature_lines: List[str]) -> str:
        """提取描述信息"""
        desc_lines = []
        
        for line in feature_lines:
            line_stripped = line.strip()
            
            if not line_stripped and not desc_lines:
                continue
            
            if line_stripped:
                desc_lines.append(line_stripped)
            elif desc_lines:
                desc_lines.append('')
        
        return re.sub(r'\n{3,}', '\n\n', '\n'.join(desc_lines)).strip()


class HistoryReleaseParser(ReleaseNotesParser):
    """History Release格式解析器 (Chrome 137)"""
    
    def extract_version(self, content: str) -> Optional[int]:
        """提取版本号"""
        match = re.search(r'## Chrome (\d+) release summary', content)
        if match:
            return int(match.group(1))
        return None
    
    def categorize_features(self, content: str) -> Dict[str, Dict]:
        """解析复杂表格格式（24列）"""
        feature_info = {}
        
        # 查找表格 - 使用更可靠的标识符
        table_marker = 'Security/ Privacy|User productivity/ Apps|Management|'
        table_start = content.find(table_marker)
        
        if table_start == -1:
            print("Could not find table marker")
            return feature_info
        
        # 向前查找到行开始
        line_start = content.rfind('\n', 0, table_start)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1  # 跳过换行符
        
        table_start = line_start
        print(f"Found table at position {table_start}")
        
        # 找到表格内容
        table_section = content[table_start:]
        lines = table_section.split('\n')
        
        # 找到分隔符行
        separator_idx = -1
        for i, line in enumerate(lines):
            if '|--' in line or '|:--' in line:
                separator_idx = i
                break
        
        if separator_idx == -1:
            print("Could not find table separator")
            return feature_info
        
        print(f"Found table with {separator_idx} header lines")
        
        # 解析表格header
        header_line = lines[0]
        headers = [h.strip() for h in header_line.split('|')[1:-1]]  # 排除空的首尾
        print(f"Table has {len(headers)} columns")
        
        # 构建section到列的映射
        section_mappings = self._build_section_mappings(headers)
        print(f"Found {len(section_mappings)} sections in table")
        
        # 解析表格数据行
        for i in range(separator_idx + 1, len(lines)):
            line = lines[i].strip()
            if not line or not line.startswith('|'):
                break  # 表格结束
            
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 1 and parts[1]:  # 有feature名称
                feature_name = parts[1]
                info = self._determine_feature_info(parts, section_mappings)
                if info:
                    feature_info[feature_name] = info
                    print(f"  Found feature: {feature_name} -> {info['change_type']}")
        
        return feature_info
    
    def _build_section_mappings(self, headers: List[str]) -> Dict[str, Dict[str, int]]:
        """构建section到列索引的映射"""
        mappings = {}
        current_section = None
        
        for i, header in enumerate(headers):
            # 识别主要section headers
            if 'Chrome browser changes' in header:
                current_section = 'Chrome Browser changes'
                mappings[current_section] = {'start': i}
            elif 'Chrome Enterprise Core' in header:
                current_section = 'Chrome Enterprise Core changes'
                mappings[current_section] = {'start': i}
            elif 'Chrome Enterprise Premium' in header:
                current_section = 'Chrome Enterprise Premium changes'
                mappings[current_section] = {'start': i}
            elif 'Upcoming Chrome browser' in header:
                current_section = 'Upcoming Chrome Browser changes'
                mappings[current_section] = {'start': i}
            elif 'Upcoming Chrome Enterprise Core' in header:
                current_section = 'Upcoming Chrome Enterprise Core changes'
                mappings[current_section] = {'start': i}
            elif 'Upcoming Chrome Enterprise Premium' in header:
                current_section = 'Upcoming Chrome Enterprise Premium changes'
                mappings[current_section] = {'start': i}
            
            # 记录分类列
            if current_section and current_section in mappings:
                if 'Security' in header and 'Privacy' in header:
                    mappings[current_section]['security'] = i
                elif 'User productivity' in header or 'Apps' in header:
                    mappings[current_section]['productivity'] = i
                elif 'Management' in header:
                    mappings[current_section]['management'] = i
        
        return mappings
    
    def _determine_feature_info(self, row_parts: List[str], section_mappings: Dict[str, Dict[str, int]]) -> Dict:
        """确定feature的section和categories"""
        feature_name = row_parts[1] if len(row_parts) > 1 else ""
        
        # 找到feature所属的section
        for section_name, mapping in section_mappings.items():
            start_col = mapping.get('start', 0)
            
            # 检查这个section的列是否有标记
            has_mark_in_section = False
            categories = []
            
            # 检查各分类列
            if 'security' in mapping and len(row_parts) > mapping['security']:
                if '✓' in row_parts[mapping['security']]:
                    categories.append("Security/Privacy")
                    has_mark_in_section = True
            
            if 'productivity' in mapping and len(row_parts) > mapping['productivity']:
                if '✓' in row_parts[mapping['productivity']]:
                    categories.append("User productivity/Apps")
                    has_mark_in_section = True
            
            if 'management' in mapping and len(row_parts) > mapping['management']:
                if '✓' in row_parts[mapping['management']]:
                    categories.append("Management")
                    has_mark_in_section = True
            
            # 如果在这个section中有标记，就是这个section的
            if has_mark_in_section:
                status = "upcoming" if "Upcoming" in section_name else "current"
                change_type = section_name.replace("Upcoming ", "")
                
                return {
                    'categories': categories,
                    'change_type': change_type,
                    'status': status
                }
        
        # 默认返回
        return {
            'categories': [],
            'change_type': 'Chrome Browser changes',
            'status': 'current'
        }
    
    def parse_features(self, content: str, feature_info: Dict[str, Dict]) -> Dict[str, Feature]:
        """基于bullet point格式和表格信息解析features"""
        features = {}
        upcoming_features = self.identify_upcoming_features(content)
        
        # 基于表格中的feature列表来查找内容
        for feature_name in feature_info.keys():
            feature = self._extract_feature_from_bullet(
                feature_name, content, feature_info, upcoming_features
            )
            if feature:
                feature.source_format = "history"
                features[feature_name] = feature
        
        return features
    
    def _extract_feature_from_bullet(self, feature_name: str, content: str,
                                   feature_info: Dict, upcoming_features: Set[str]) -> Optional[Feature]:
        """从bullet point格式提取feature信息"""
        # 查找对应的bullet point
        pattern = rf'^-\s*{re.escape(feature_name)}(.*?)(?=^-\s*[A-Z]|\n##|\Z)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            # 如果找不到完全匹配，尝试模糊匹配
            escaped_name = re.escape(feature_name[:20])  # 使用前20个字符
            pattern = rf'^-\s*{escaped_name}(.*?)(?=^-\s*[A-Z]|\n##|\Z)'
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        
        if not match:
            return None
        
        # 创建feature对象
        feature = Feature(
            title=feature_name,
            change_type="Chrome Browser changes",
            categories=[],
            status="current"
        )
        
        # 使用表格信息
        if feature_name in feature_info:
            info = feature_info[feature_name]
            feature.categories = info['categories']
            feature.change_type = info['change_type']
            feature.status = info['status']
        
        # 解析内容
        feature_content = match.group(1).strip()
        feature.platforms = self._extract_platforms(feature_content)
        feature.policy = self._extract_policy(feature_content)
        feature.description = self._clean_description(feature_content)
        
        # 提取版本信息
        if feature.status == "upcoming":
            version_match = re.search(r'Chrome (\d+)', feature_content)
            if version_match:
                feature.version_info = f"Chrome {version_match.group(1)}"
        
        return feature
    
    def _extract_platforms(self, text: str) -> List[str]:
        """提取平台信息"""
        platforms = []
        known_platforms = ['Android', 'ChromeOS', 'Linux', 'macOS', 'Windows', 'iOS']
        
        for platform in known_platforms:
            patterns = [
                rf'Chrome \d+ on .*\b{platform}\b',
                rf'Chrome \d+on .*\b{platform}\b',  # 处理缺少空格的情况
                rf'- Chrome \d+ on .*\b{platform}\b',
                rf'\b{platform}\b(?:\s*,|\s+and\s+|:)',
            ]
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    if platform not in platforms:
                        platforms.append(platform)
                    break
        
        return platforms
    
    def _extract_policy(self, text: str) -> Optional[str]:
        """提取策略信息"""
        policy_patterns = [
            r'the\s*([A-Za-z]+[A-Za-z0-9]*)\s*policy',
            r'using the\s*([A-Za-z]+[A-Za-z0-9]*)\s*policy',
            r'controlled by the\s*([A-Za-z]+[A-Za-z0-9]*)\s*policy',
            r'setting the\s*([A-Za-z]+[A-Za-z0-9]*)\s*policy',
        ]
        
        for pattern in policy_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _clean_description(self, text: str) -> str:
        """清理和格式化描述文本"""
        # 移除多余的空行和空白
        lines = []
        for line in text.split('\n'):
            line_clean = line.strip()
            if line_clean:
                lines.append(line_clean)
            elif lines:  # 保持段落间的空行
                lines.append('')
        
        return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()


class ReleaseNotesProcessorV2:
    """统一的Release Notes处理器"""
    
    def __init__(self):
        self.detector = ReleaseNotesFormatDetector()
        self.parsers = {
            'current': CurrentReleaseParser(),
            'history': HistoryReleaseParser()
        }
        self.current_version = None
        self.features = {}
        self.detected_format = None
    
    def process_release_notes(self, file_path: str):
        """主处理流程"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. 检测格式
        self.detected_format = self.detector.detect_format(content)
        print(f"Detected format: {self.detected_format}")
        
        # 2. 选择对应解析器
        parser = self.parsers[self.detected_format]
        
        # 3. 提取版本信息
        self.current_version = parser.extract_version(content)
        if not self.current_version:
            print("Warning: Could not extract Chrome version")
            self.current_version = 138  # Fallback
        
        print(f"Processing Chrome {self.current_version}")
        
        # 4. 解析feature信息
        feature_info = parser.categorize_features(content)
        print(f"Found {len(feature_info)} features in tables")
        
        # 5. 解析feature详细内容
        self.features = parser.parse_features(content, feature_info)
        print(f"Successfully parsed {len(self.features)} features")
        
        # 6. 处理特殊features（如新增/删除的策略）
        special_features = self._handle_special_features(content)
        for feature in special_features:
            self.features[feature.title] = feature
    
    def _handle_special_features(self, content: str) -> List[Feature]:
        """处理特殊features，如策略变更"""
        special_features = []
        
        # 处理新增策略
        new_policies_match = re.search(
            r'### New policies in Chrome browser\n+(.*?)(?=\n###|\n##|\Z)',
            content, re.DOTALL
        )
        
        if new_policies_match:
            policy_content = new_policies_match.group(1).strip()
            policy_list = re.findall(r'\[([A-Za-z]+[A-Za-z0-9]*)\]', policy_content)
            
            if policy_list:
                feature = Feature(
                    title="New policies in Chrome browser",
                    change_type="Chrome Browser changes",
                    categories=["Management"],
                    status="current",
                    platforms=['Linux', 'macOS', 'Windows', 'ChromeOS'],
                    description=f"新增策略: {', '.join(policy_list)}",
                    source_format=self.detected_format
                )
                special_features.append(feature)
        
        return special_features
    
    def generate_organized_output(self) -> str:
        """生成组织化的markdown输出"""
        # 按分类和状态组织features
        organized = {
            "User productivity/Apps": {"current": [], "upcoming": []},
            "Security/Privacy": {"current": [], "upcoming": []},
            "Management": {"current": [], "upcoming": []}
        }
        
        # 组织features
        for feature in self.features.values():
            # 确保feature有分类
            if not feature.categories:
                feature.categories = self._infer_categories(feature)
            
            # 添加到对应分类
            for category in feature.categories:
                if category in organized:
                    organized[category][feature.status].append(feature)
        
        # 生成输出
        output = []
        
        for category, features_by_status in organized.items():
            output.append(f"### {category}\n")
            
            # Current features
            if features_by_status["current"]:
                output.append(f"**Current — Chrome {self.current_version}**\n")
                for feature in sorted(features_by_status["current"], key=lambda f: f.title):
                    output.append(self._format_feature(feature))
                output.append("")
            
            # Upcoming features
            if features_by_status["upcoming"]:
                output.append(f"**Upcoming — Chrome {self.current_version + 1} and beyond**\n")
                for feature in sorted(features_by_status["upcoming"], key=lambda f: f.title):
                    output.append(self._format_feature(feature))
                output.append("")
            
            output.append("---\n")
        
        # 移除最后的分隔符
        if output and output[-1] == "---\n":
            output.pop()
        
        return '\n'.join(output)
    
    def _infer_categories(self, feature: Feature) -> List[str]:
        """推断feature分类"""
        title_lower = feature.title.lower()
        desc_lower = feature.description.lower()
        
        if any(word in title_lower + desc_lower for word in 
               ['security', 'safe', 'privacy', 'protect', 'scam', 'malware', 'dlp']):
            return ["Security/Privacy"]
        elif any(word in title_lower for word in 
                 ['policy', 'policies', 'management', 'admin', 'insights']):
            return ["Management"]
        else:
            return ["User productivity/Apps"]
    
    def _format_feature(self, feature: Feature) -> str:
        """格式化单个feature"""
        output = [f"* **{feature.title}**"]
        
        # 添加版本信息
        if feature.status == "upcoming" and feature.version_info:
            output[0] += f" ({feature.version_info})"
        
        output.append(f"  • Type: {feature.change_type}")
        
        # 平台信息
        if feature.platforms:
            desktop_platforms = []
            mobile_platforms = []
            
            platform_mapping = {
                'Windows': 'desktop', 'macOS': 'desktop', 'Linux': 'desktop', 'ChromeOS': 'desktop',
                'Android': 'mobile', 'iOS': 'mobile'
            }
            
            for platform in feature.platforms:
                if platform_mapping.get(platform) == 'desktop':
                    desktop_platforms.append(platform)
                elif platform_mapping.get(platform) == 'mobile':
                    mobile_platforms.append(platform)
            
            platform_parts = []
            if desktop_platforms:
                platform_parts.append(f"Desktop ({', '.join(sorted(desktop_platforms))})")
            if mobile_platforms:
                platform_parts.append(f"Mobile ({', '.join(sorted(mobile_platforms))})")
            
            if platform_parts:
                output.append(f"  • Platform: {', '.join(platform_parts)}")
        
        # 描述信息
        desc = feature.description
        if feature.policy and feature.policy not in desc:
            if desc:
                desc += f"；受 `{feature.policy}` 策略控制"
            else:
                desc = f"受 `{feature.policy}` 策略控制"
        
        # 处理多行描述
        desc_lines = desc.split('\n')
        if desc_lines:
            output.append(f"  • Update: {desc_lines[0]}")
            for line in desc_lines[1:]:
                if line.strip():
                    output.append(f"    {line.strip()}")
        
        output.append("")
        
        return '\n'.join(output)


def get_unprocessed_versions():
    """查找未处理的版本"""
    base_path = Path("/Users/lyzh/Documents/Nova_Projects/chrome-update-digest")
    release_notes_dir = base_path / "upstream_docs" / "release_notes" / "Enterprise"
    processed_dir = base_path / "upstream_docs" / "processed_forenterprise"
    
    # 查找所有release note文件并提取版本
    release_versions = set()
    for file in release_notes_dir.glob("*.md"):
        match = re.search(r'(\d+)[-_]chrome[-_]enterprise', file.name, re.IGNORECASE)
        if match:
            release_versions.add(int(match.group(1)))
    
    # 查找已处理的版本
    processed_versions = set()
    for file in processed_dir.glob("*-organized_chromechanges-enterprise.md"):
        match = re.search(r'^(\d+)-organized_chromechanges-enterprise\.md$', file.name)
        if match:
            processed_versions.add(int(match.group(1)))
    
    unprocessed = release_versions - processed_versions
    return sorted(unprocessed), release_notes_dir, processed_dir


def find_release_file(version, release_notes_dir):
    """查找指定版本的release notes文件"""
    patterns = [
        f"{version}-chrome-enterprise.md",
        f"{version}_chrome_enterprise.md",
        f"*{version}*chrome*enterprise*.md"
    ]
    
    for pattern in patterns:
        matches = list(release_notes_dir.glob(pattern))
        if matches:
            return matches[0]
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Process Chrome Enterprise release notes with format auto-detection')
    parser.add_argument('version', nargs='?', type=int, help='Chrome version to process (e.g., 137)')
    parser.add_argument('--all', action='store_true', help='Process all unprocessed versions')
    parser.add_argument('--list', action='store_true', help='List unprocessed versions without processing')
    parser.add_argument('--format', choices=['current', 'history'], help='Force specific format detection')
    
    args = parser.parse_args()
    
    # 获取未处理的版本
    unprocessed_versions, release_notes_dir, processed_dir = get_unprocessed_versions()
    
    if args.list:
        if unprocessed_versions:
            print(f"Unprocessed versions: {', '.join(map(str, unprocessed_versions))}")
        else:
            print("All versions have been processed.")
        return
    
    # 确定要处理的版本
    versions_to_process = []
    
    if args.version:
        if args.version in unprocessed_versions:
            versions_to_process = [args.version]
        else:
            print(f"Version {args.version} has already been processed or release notes not found.")
            sys.exit(1)
    elif args.all:
        versions_to_process = unprocessed_versions
    else:
        if unprocessed_versions:
            versions_to_process = [unprocessed_versions[0]]
            print(f"No version specified. Processing Chrome {versions_to_process[0]}...")
        else:
            print("All versions have been processed. Nothing to do.")
            return
    
    # 处理每个版本
    for version in versions_to_process:
        input_file = find_release_file(version, release_notes_dir)
        if not input_file:
            print(f"Error: Could not find release notes for Chrome {version}")
            continue
        
        output_file = processed_dir / f"{version}-organized_chromechanges-enterprise.md"
        
        # 处理release notes
        processor = ReleaseNotesProcessorV2()
        
        # 强制格式检测（如果指定）
        if args.format:
            processor.detected_format = args.format
        
        print(f"\n{'='*50}")
        print(f"Processing Chrome {version} from {input_file.name}")
        print(f"{'='*50}")
        
        try:
            processor.process_release_notes(str(input_file))
            
            # 生成输出
            print("Generating organized output...")
            organized_content = processor.generate_organized_output()
            
            # 写入文件
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(organized_content)
            
            print(f"✅ Output written to: {output_file.name}")
            print(f"✅ Processed {len(processor.features)} features")
            print(f"✅ Detected format: {processor.detected_format}")
            
        except Exception as e:
            print(f"❌ Error processing Chrome {version}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 Processing complete!")


if __name__ == "__main__":
    main()