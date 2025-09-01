# Pipeline 调整计划

## 当前问题分析

### 1. 重复内容问题
通过测试发现，Graphics-WebGPU area中存在重复的feature：
- Chrome release notes中有简短版本的WebGPU feature
- WebGPU release notes中有详细版本的同一个feature
- 例如："3D texture support for BC and ASTC compressed formats" 同时出现在两个源中

### 2. 数据处理逻辑需要调整
现在的merging逻辑简单拼接了Chrome Graphics + WebGPU内容，但没有做去重处理。

### 3. 最终输出格式
最终需要输出YAML格式，而不是markdown文件。

## 调整方案

### 第一阶段：改进去重逻辑

#### 1.1 Feature去重策略
- **识别重复feature的方法**：
  - 基于标题相似度（normalize后比较）
  - 基于issue ID匹配（ChromeStatus链接、tracking bug等）
  - 基于关键词匹配
  
- **优先级规则**：
  - WebGPU release notes > Chrome release notes（因为WebGPU更详细）
  - 长内容 > 短内容（更详细的描述）
  - 有代码示例 > 无代码示例

#### 1.2 实现步骤
1. 解析Chrome Graphics section中的features（h3级别）
2. 解析WebGPU release notes中的features（h2级别，降级为h3）
3. 对比feature标题和内容，识别重复
4. 应用优先级规则，保留最佳版本
5. 合并去重后的features

### 第二阶段：集成YAML输出管道

#### 2.1 调用现有YAML Pipeline
- 使用 `src/utils/yaml_pipeline.py` 中的 `YAMLPipeline` 类
- 为每个area调用YAML转换
- Graphics-WebGPU使用去重后的markdown内容

#### 2.2 输出结构调整
```
upstream_docs/processed_releasenotes/processed_forwebplatform/areas/
├── css/
│   ├── chrome-139-stable.md                    # Human-readable content
│   └── chrome-139-stable.yml                   # Structured data
├── graphics-webgpu/
│   ├── chrome-139-stable.md                    # 去重后的合并内容  
│   └── chrome-139-stable.yml                   # Structured data
├── webapi/
│   ├── chrome-139-stable.md                    # Human-readable content
│   └── chrome-139-stable.yml                   # Structured data
└── ...
```

### 第三阶段：Pipeline集成

#### 3.1 修改现有Pipeline
1. **替换splitting逻辑**：
   - 用新的 `CleanDataPipeline` 替代 `ReleaseNoteSplitter`
   - 保持相同的接口和输出格式

2. **增强WebGPU处理**：
   - 在 `merge_webgpu_graphics.py` 中集成去重逻辑
   - 或者直接在 `CleanDataPipeline` 中完成所有处理

3. **YAML生成集成**：
   - 修改 `split_and_process_release_notes.py` 使用新pipeline
   - 确保YAML生成步骤使用去重后的内容

#### 3.2 向后兼容性
- 保持现有的文件结构和命名
- MCP tools可以无缝切换到新pipeline
- 现有的YAML配置和area映射继续有效

## 具体实现计划

### 步骤1：增强Feature去重功能
```python
def deduplicate_features(self, chrome_features: List[Feature], 
                        webgpu_features: List[Feature]) -> List[Feature]:
    """
    去重逻辑：WebGPU优先，基于标题和issue ID匹配
    """
    # 1. 标题标准化和匹配
    # 2. Issue ID提取和匹配  
    # 3. 应用优先级规则
    # 4. 返回去重后的feature列表
```

### 步骤2：修改merge_graphics_webgpu方法
```python
def merge_graphics_webgpu(self, chrome_graphics: str, 
                         webgpu_content: str, version: str) -> str:
    """
    改进的合并逻辑，包含去重
    """
    # 1. 解析Chrome Graphics features
    # 2. 解析WebGPU features  
    # 3. 执行去重
    # 4. 生成合并后的markdown
```

### 步骤3：集成YAML输出
```python
def process_version_with_yaml(self, version: str) -> Dict[str, Path]:
    """
    完整处理：markdown提取 + YAML生成
    """
    # 1. 生成area markdown files
    # 2. 对每个area调用YAMLPipeline
    # 3. 输出YAML files
    # 4. 返回YAML file paths
```

## 预期效果

### 1. 数据质量提升
- 消除Graphics-WebGPU中的重复features
- 保留最详细和最准确的feature描述
- 清理WebGPU中的无效历史信息

### 2. 输出结构优化
- 统一的area-based结构
- 清晰的YAML输出用于下游处理
- 向后兼容现有工具链

### 3. 维护性改善
- 简化的去重规则，易于调试
- 模块化的处理步骤
- 清晰的数据流向

## 风险评估

### 1. 去重准确性
- **风险**：可能误删不同的features
- **缓解**：严格的匹配规则，保留边界情况的features

### 2. 性能影响
- **风险**：去重算法增加处理时间
- **缓解**：优化匹配算法，批量处理

### 3. 兼容性
- **风险**：现有工具依赖特定格式
- **缓解**：保持文件结构和接口不变