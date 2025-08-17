# Chrome Enterprise Release Notes Processor - Design Document

## 概述

设计一个能够自动识别并处理两种不同格式的Chrome Enterprise Release Notes的处理器，实现向后兼容性并提供统一的输出格式。

## 格式分析

### Current Release 格式（当前格式）
```markdown
## Chrome 138 release summary

### Chrome browser changes
| Feature | Security/Privacy | User productivity/Apps | Management |
|---------|:----------------:|:---------------------:|:----------:|
| [Feature Name](#feature-name) | ✓ | | |

## Chrome browser changes

### Feature Name
Feature description here...
- Chrome 138 on Windows, macOS, Linux
```

**特征：**
- 简单的三列表格格式
- 使用 `###` 标题作为feature标识
- 清晰的markdown结构
- Feature名称作为标题

### History Release 格式（历史格式）
```markdown
## Chrome 137 release summary

|Chrome browser changes|Security/ Privacy|User productivity/ Apps|Management|Chrome Enterprise Core changes|Security/ Privacy|User productivity/ Apps|Management|Chrome Enterprise Premium changes|Security/ Privacy|User productivity/ Apps|Management|Upcoming Chrome browser changes|Security/ Privacy|User productivity/ Apps|Management|Upcoming Chrome Enterprise Core changes|Security/ Privacy|User productivity/ Apps|Management|Upcoming Chrome Enterprise Premium changes|Security/ Privacy|User productivity/ Apps|Management|
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|Gemini in Chrome||✓||
|Blob URL Partitioning: Fetching/Navigation|✓|||

## Chrome browser changes

- Gemini in ChromeGemini is now integrated into Chrome...
- Blob URL Partitioning: Fetching/NavigationAs a continuation...
```

**特征：**
- 复杂的多section水平表格（24列）
- Feature内容使用bullet point格式（`-`）
- Feature名称没有空格分隔内容
- 包含multiple product sections在一个表格中

## 设计架构

### 1. 格式检测器 (Format Detector)

```python
class ReleaseNotesFormatDetector:
    def detect_format(self, content: str) -> str:
        """
        检测release notes格式
        返回: 'current' 或 'history'
        """
        # 检测方法：
        # 1. 检查表格列数
        # 2. 检查是否有 ### feature headers
        # 3. 检查表格结构复杂度
```

**检测逻辑：**
1. **表格列数检测**：History格式有24+列，Current格式只有4列
2. **Feature标题检测**：Current格式有`### Feature Name`，History格式没有
3. **表格结构检测**：History格式表格包含多个product sections

### 2. 解析器接口 (Parser Interface)

```python
class ReleaseNotesParser(ABC):
    @abstractmethod
    def extract_version(self, content: str) -> Optional[int]:
        """提取Chrome版本号"""
        pass
    
    @abstractmethod
    def parse_features(self, content: str) -> Dict[str, Feature]:
        """解析所有features"""
        pass
    
    @abstractmethod
    def categorize_features(self, content: str) -> Dict[str, Dict]:
        """从表格提取feature分类信息"""
        pass
```

### 3. Current Release 解析器

```python
class CurrentReleaseParser(ReleaseNotesParser):
    def categorize_features(self, content: str) -> Dict[str, Dict]:
        """
        解析简单表格格式
        | Feature | Security/Privacy | User productivity/Apps | Management |
        """
        # 实现简单表格解析
        # 寻找 "| Feature |" 开头的表格
        # 解析3列分类信息
    
    def parse_features(self, content: str) -> Dict[str, Feature]:
        """
        基于 ### 标题解析features
        """
        # 查找所有 ### 开头的feature sections
        # 提取feature内容直到下一个 ### 或 ##
```

### 4. History Release 解析器

```python
class HistoryReleaseParser(ReleaseNotesParser):
    def categorize_features(self, content: str) -> Dict[str, Dict]:
        """
        解析复杂表格格式（24列）
        |Chrome browser changes|Security/ Privacy|...|Upcoming Chrome Enterprise Premium changes|Security/ Privacy|User productivity/ Apps|Management|
        """
        # 1. 找到大表格
        # 2. 解析表格header，识别各个section的列位置
        # 3. 为每个feature确定所属section和分类
        
    def parse_features(self, content: str) -> Dict[str, Feature]:
        """
        基于bullet point格式解析features
        """
        # 1. 从表格获取feature列表
        # 2. 在内容中查找对应的 "- Feature Name" bullet points
        # 3. 提取详细内容直到下一个bullet point
```

### 5. 统一处理器

```python
class ReleaseNotesProcessorV2:
    def __init__(self):
        self.detector = ReleaseNotesFormatDetector()
        self.parsers = {
            'current': CurrentReleaseParser(),
            'history': HistoryReleaseParser()
        }
    
    def process_release_notes(self, file_path: str):
        """
        主处理流程
        """
        # 1. 读取文件
        # 2. 检测格式
        # 3. 选择对应解析器
        # 4. 解析和处理
        # 5. 生成统一输出
```

## 实现细节

### 1. 格式检测实现

```python
def detect_format(self, content: str) -> str:
    # 检查表格复杂度
    table_match = re.search(r'\|([^|]+\|){20,}', content)  # 20+列表格
    if table_match:
        return 'history'
    
    # 检查是否有### feature headers
    feature_headers = re.findall(r'^### [^#].*$', content, re.MULTILINE)
    simple_table = re.search(r'\| Feature \| Security/Privacy \|', content)
    
    if feature_headers and simple_table:
        return 'current'
    
    # 默认fallback逻辑
    return 'history' if not feature_headers else 'current'
```

### 2. History Release 表格解析

```python
def parse_history_table(self, content: str) -> Dict[str, Dict]:
    """
    解析History格式的复杂表格
    表格结构：
    |Chrome browser changes|Sec|User|Mgmt|Chrome Enterprise Core|Sec|User|Mgmt|Chrome Enterprise Premium|Sec|User|Mgmt|Upcoming Chrome browser|Sec|User|Mgmt|...|
    """
    # 1. 找到表格
    table_pattern = r'\|Chrome browser changes\|.*?\n\|--.*?\n((?:\|.*?\n)*)'
    
    # 2. 解析header，确定列映射
    header_columns = {
        'Chrome browser changes': {'start': 0, 'sec': 1, 'user': 2, 'mgmt': 3},
        'Chrome Enterprise Core changes': {'start': 4, 'sec': 5, 'user': 6, 'mgmt': 7},
        'Chrome Enterprise Premium changes': {'start': 8, 'sec': 9, 'user': 10, 'mgmt': 11},
        'Upcoming Chrome browser changes': {'start': 12, 'sec': 13, 'user': 14, 'mgmt': 15},
        # ... 更多sections
    }
    
    # 3. 解析每一行，确定feature所属section和categories
    features = {}
    for row in table_rows:
        feature_name = row[0].strip('|').strip()
        if feature_name:
            features[feature_name] = self._determine_feature_info(row, header_columns)
    
    return features
```

### 3. History Release 内容提取

```python
def extract_history_feature_content(self, feature_name: str, content: str) -> str:
    """
    从History格式中提取feature详细内容
    """
    # 查找bullet point: "- Feature NameContent here..."
    pattern = rf'^-\s*{re.escape(feature_name)}(.*?)(?=^-\s*[A-Z]|\n##|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    
    if match:
        feature_content = match.group(1).strip()
        # 清理和格式化内容
        return self._clean_feature_content(feature_content)
    
    return ""
```

### 4. 统一Feature数据结构

```python
@dataclass
class Feature:
    title: str
    change_type: str  # "Chrome Browser changes", "Chrome Enterprise Core changes", etc.
    categories: List[str]  # ["Security/Privacy", "User productivity/Apps", "Management"]
    status: str  # "current" or "upcoming"
    platforms: List[str] = field(default_factory=list)
    description: str = ""
    policy: Optional[str] = None
    version_info: Optional[str] = None
    source_format: str = ""  # "current" or "history"
```

## 测试策略

### 1. 格式检测测试
```python
def test_format_detection():
    # 测试Current格式检测
    current_content = load_sample_current_content()
    assert detector.detect_format(current_content) == 'current'
    
    # 测试History格式检测
    history_content = load_sample_history_content()
    assert detector.detect_format(history_content) == 'history'
```

### 2. 解析器测试
```python
def test_history_parsing():
    parser = HistoryReleaseParser()
    content = load_history_sample()
    
    # 测试表格解析
    features_info = parser.categorize_features(content)
    assert len(features_info) > 0
    assert 'Gemini in Chrome' in features_info
    
    # 测试内容提取
    features = parser.parse_features(content)
    assert len(features) > 0
    assert features['Gemini in Chrome'].description != ""
```

### 3. 端到端测试
```python
def test_end_to_end_processing():
    processor = ReleaseNotesProcessorV2()
    
    # 测试History格式文件
    processor.process_release_notes('137-chrome-enterprise.md')
    assert len(processor.features) > 20  # 应该处理20+个features
    
    # 测试Current格式文件
    processor.process_release_notes('138-chrome-enterprise.md')
    assert len(processor.features) > 15  # 应该处理15+个features
```

## 配置和扩展性

### 1. 配置文件
```yaml
# config.yaml
parsers:
  history:
    table_column_threshold: 20
    feature_bullet_pattern: '^-\s*([^:]+)'
    section_headers:
      - "Chrome browser changes"
      - "Chrome Enterprise Core changes"
      - "Chrome Enterprise Premium changes"
  
  current:
    feature_header_pattern: '^### (.+)$'
    simple_table_pattern: '\| Feature \| Security/Privacy \|'
```

### 2. 插件架构
```python
class ParserPlugin(ABC):
    @abstractmethod
    def can_handle(self, content: str) -> bool:
        """判断是否能处理此格式"""
        pass
    
    @abstractmethod
    def parse(self, content: str) -> Dict[str, Feature]:
        """解析内容"""
        pass

# 支持注册新的解析器
processor.register_parser('future', FutureReleaseParser())
```

## 错误处理和降级策略

### 1. 格式检测失败
```python
def detect_format_with_fallback(self, content: str) -> str:
    try:
        return self.detect_format(content)
    except Exception as e:
        logger.warning(f"Format detection failed: {e}")
        # 使用启发式方法或用户输入
        return self.fallback_detection(content)
```

### 2. 解析失败处理
```python
def parse_with_fallback(self, content: str) -> Dict[str, Feature]:
    primary_format = self.detect_format(content)
    try:
        return self.parsers[primary_format].parse_features(content)
    except Exception as e:
        logger.error(f"Primary parser {primary_format} failed: {e}")
        # 尝试其他解析器
        for format_name, parser in self.parsers.items():
            if format_name != primary_format:
                try:
                    return parser.parse_features(content)
                except:
                    continue
        raise Exception("All parsers failed")
```

## 输出格式标准化

不管输入格式如何，都生成统一的输出格式：

```markdown
### User productivity/Apps

**Current — Chrome [version]**

* **Feature Name**
  • Type: Chrome Browser changes
  • Platform: Desktop (Windows, macOS, Linux)
  • Update: Feature description with policy info
    Additional details and rollout information

**Upcoming — Chrome [version+1] and beyond**

* **Upcoming Feature** (Chrome 139)
  • Type: Chrome Enterprise Core changes
  • Update: Upcoming feature description
```

## 迁移和维护

### 1. 版本兼容性矩阵
| Chrome Version | Format  | Parser              | Status        |
|----------------|---------|---------------------|---------------|
| 137            | History | HistoryReleaseParser| ✅ Supported |
| 138+           | Current | CurrentReleaseParser| ✅ Supported |
| Future         | TBD     | Extensible          | 🔄 Planned   |

### 2. 监控和告警
```python
def validate_parsing_results(self, features: Dict[str, Feature]) -> bool:
    """验证解析结果质量"""
    if len(features) < 5:
        logger.warning("Parsed fewer than 5 features - possible parsing issue")
        return False
    
    empty_descriptions = sum(1 for f in features.values() if not f.description.strip())
    if empty_descriptions / len(features) > 0.3:
        logger.warning("More than 30% features have empty descriptions")
        return False
    
    return True
```

这个设计提供了完整的向后兼容性，同时为未来格式变化提供了扩展性。