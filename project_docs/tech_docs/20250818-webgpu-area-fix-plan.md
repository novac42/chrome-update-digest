# WebGPU 分区（graphics-webgpu）错误归类修复方案

日期: 2025-08-18  
作者: （计划草案）  
状态: Draft

## 1. 背景 & 问题

当前按 area 生成的 YAML（例如 `graphics-webgpu-chrome-139-stable.yml`）包含大量与 WebGPU 无直接关系的特性（例如 Network / Security / Accept-Language / CSP / SPC 等）。

这些“非 WebGPU”特性之所以被放入 `graphics-webgpu`，原因是：

1. 在合并后的或 WebGPU 专题 markdown 中，顶层或上层 heading 含有 `WebGPU` 字样（例如 `What's New in WebGPU (Chrome 139)`），导致特性在 heading 继承路径中出现该词。
2. `HeadingBasedTagger` 中的匹配策略会遍历完整 heading path，对任意出现包含 `webgpu` / `graphics` / `gpu` 的 heading 赋予 `webgpu` tag。
3. area 分裂逻辑 `split_features_by_area` / `_determine_area` 根据 heading path 中任意层命中 `WebGPU` / `Graphics` 即归类到 `graphics-webgpu`（当前实现没有“位置限制”或“主要 heading”约束）。

结果：只要任一祖先 heading 有 “WebGPU”，子节点（即便实际主题为 Network / Security / Payments）也被视为 WebGPU 区域。

## 2. 目标

- 精确限定 `graphics-webgpu` 只包含真正的图形 / WebGPU 相关特性。
- 保留真正的 WebGPU 功能（格式、纹理、Dawn、兼容模式、core-features-and-limits 等）。
- 不破坏现有其它 area 分类（css/webapi/network/security 等）。
- 回溯再生时不需要手工修正。

## 3. Root Cause 细化

| 层面 | 问题 | 影响 |
|------|------|------|
| Tag 映射 | `graphics`、`webgpu`、`gpu` 全被等价映射为 webgpu | 提升误报概率 |
| Tag 判定位置 | 遍历所有 heading path（含远祖） | 远祖含 “WebGPU” 时即打 tag |
| Area 判定 | `_determine_area` 遍历所有 heading 层级简单包含匹配 | 任何祖先命中即可归类 |
| 数据合并 | WebGPU 合并逻辑将“说明文字 + 详细更新”嵌入 Graphics / WebGPU 分区 | 上层语义放大“WebGPU”覆盖范围 |
| 标题保留 | 专题文件中的 一级 Heading `# What's New in WebGPU (Chrome X)` 未在 merge 前完全剥离（或仅被降级），导致其作为祖先残留，引发后续所有子项继承 WebGPU 语义 | 扩大误分类范围 |

## 4. 约束 & 不做的内容

- 不改动外部提取（link extractor）基础结构。
- 不（立即）引入复杂 NLP；采用可解释的结构化规则。
- 不立即移除现有 tagger 的 `webgpu` 关键词（避免回归），改为在 area 归类阶段加强过滤。

## 5. 判定 WebGPU 归类的建议规则
引入“判定分值/条件集合”，只有满足“强相关”条件之一，且不触发“排除”条件，才归类为 `graphics-webgpu`。

### 5.1 强相关 (Positive Signals)

| 信号 | 描述 | 分值 (示意) |
|------|------|-------------|
| H_final 命中 | 最末级 heading（特性标题上一级或本级）包含 WebGPU/Graphics/纹理/Shader 等关键词 | +2 |
| 标题关键词 | 特性 title 含 texture / shader / WGSL / WebGPU / GPU / Dawn | +2 |
| 内容核心术语 | 内容正文出现 GPU buffer / pipeline / adapter / device / compute / WGSL | +1 |
| 仅 WebGPU 专题来源 | heading path 中含 `Detailed WebGPU Updates` / `What's New in WebGPU` 且同级小类为图形子主题（非 Network/Security 等通用分类词） | +1 |

设定：分值 ≥3 视为 WebGPU 归类候选。

### 5.2 弱相关 (Neutral)

- 祖先 heading 含 WebGPU，但中间/末级为通用分区（Network / Security / Navigation / Web APIs / Performance / Origin trials 等）。

### 5.3 排除 (Negative Signals)

| 条件 | 描述 |
|------|------|
| 末级或倒数第二级 heading 为通用域（network / security / privacy / payments / navigation / web apis / origin trials / deprecations / media / ai / performance 等）且标题不含任何强相关关键词 | 防止借祖先 WebGPU 污染 |
| 只有祖先远级（位置 index < len(path)-2）包含 WebGPU 关键字 | 认为是“背景”而非该特性的直接领域 |
| primary_tags 中 network/security/webapi/performance/payment 等分值权重大于 webgpu（或 webgpu 仅 secondary） | 优先归属非 WebGPU 领域 |

### 5.4 判定逻辑伪代码

```python
def is_strong_webgpu(feature):
    path = feature.heading_path
    title = feature.title.lower()
    content = feature.content.lower()
    last_two = path[-2:]

    webgpu_keywords = {...}
    core_terms = {...}
    generic_domains = {...}

    score = 0
    if any(k in h.lower() for k in webgpu_keywords for h in last_two):
        score += 2
    if any(k in title for k in webgpu_keywords | core_terms):
        score += 2
    if sum(1 for k in core_terms if k in content) >= 2:
        score += 1
    if any(special in path for special in ['Detailed WebGPU Updates']):
        score += 1

    # Exclusion
    if any(g in h.lower() for g in generic_domains for h in last_two) and score < 4:
        return False
    if not any(k in h.lower() for k in webgpu_keywords for h in last_two):
        return False
    return score >= 3
```

## 6. 具体实施步骤

| 阶段 | 任务 | 产出 |
|------|------|------|
| 1 | 基线采样：统计当前 139 版 `graphics-webgpu` 中非图形特性数量（按标题关键词+primary tag） | baseline.json 报告 |
| 2 | 新判定函数原型（独立 util，不改原接口） | `src/utils/area_classifier.py` (初稿) |
| 3 | 在 `_determine_area` 中注入“若目标 area = graphics-webgpu 则调用新判定”但 behind feature flag | 环境变量 `STRICT_WEBGPU_AREA=1` |
| 3.1 | 调整 WebGPU merge：在清洗阶段彻底删除（而不是保留/降级）一级标题 `# What's New in WebGPU*`，后续最顶层只出现 `##` | 清洗函数更新 & 单元测试 |
| 4 | 新增测试： |  |
| 4.1 | 正例：真正 WebGPU 特性应保留 |  |
| 4.2 | 反例：Accept-Language / CSP / SPC 不应出现在 graphics-webgpu |  |
| 4.3 | 边界：含 Dawn / pipeline / adapter 词汇 | `tests/test_area_webgpu_strict.py` |
| 5 | 回归所有现有测试（确保其它 area 不回归） | CI 通过 |
| 6 | 重新生成 137 / 138 / 139 样本，输出 diff 报告 | diff_md 报告 |
| 7 | 若无问题，移除 flag，默认启用；保留回退开关 | 文档更新 |

## 7. 测试设计
 
### 7.1 单元测试

- `test_is_strong_webgpu_positive()`：含 `GPUTexture` / `compute pipeline`。
- `test_is_strong_webgpu_negative_network()`：`Network` + 无 GPU 术语。
- `test_is_strong_webgpu_false_due_to_ancestor_only()`：祖先 path 含 WebGPU，但末级为 `Security`。

### 7.2 集成测试

- 运行管线生成 area YAML，断言 `graphics-webgpu` 中“不含”指定黑名单标题（列表存放 tests 里）。

### 7.3 统计校验

- 统计修复前后：
  - total_features_graphics_webgpu 变化
  - 真实 WebGPU 精确率 (manual labeled subset) 提升

## 8. 回退策略

- 通过环境变量 / config 切换回旧逻辑：`STRICT_WEBGPU_AREA=0`。
- 保留原 `_determine_area` 代码段注释说明 1 周。

## 9. 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 误删真实 WebGPU 特性（召回下降） | 高价值关键词白名单 + 手动审查前 2 个版本输出 |
| 规则过度复杂后续难维护 | 提取词表到配置 `config/webgpu_classification.yaml` |
| 与 primary tag 统计不一致 | 生成比对报告：按 tag vs area 双维度输出 |

## 10. 后续可拓展

- 用 embedding（本地向量）对“图形/渲染”语义聚类提高召回。
- 生成 explain 字段写入 YAML：记录为何判定为 WebGPU（score + 命中规则）。
- 统一 area 判定为可插拔策略模式。

## 11. 验收标准 (Acceptance Criteria)

| 编号 | 标准 |
| AC1 | `graphics-webgpu-chrome-139-stable.yml` 中不再包含 Accept-Language / CSP / SPC / Crash Reporting / Prompt API 等非图形特性 |
| AC2 | 真正 WebGPU 相关特性（压缩纹理 3D、compatibility mode、Dawn updates 等）全部保留 |
| AC3 | 其它 area 数量变化 ≤ 2（浮动只来源于剥离 webgpu 误归类） |
| AC4 | 新增测试全部通过，旧测试无回归 |
| AC5 | 方案文档与配置文件说明齐备 |
| AC6 | 合并后的 `*-merged-webgpu.md` 中不出现一级 `# What's New in WebGPU` 标题，最早 WebGPU 专题插入处直接以 `## WebGPU` 或下级内容开头 |

## 12. 工作量评估 (Rough Estimate)


---
如需补充：可附加当前错误样例列表（待 baseline 统计后更新）。

> 下一步：执行 阶段 1 基线统计脚本，产出非 WebGPU 特性清单。

## 13. 合并产物复检与改进建议（2025-08-18 新增）

### 13.1 当前合并产物问题总览

| 编号 | 问题 | 示例 / 说明 | 影响 |
|------|------|-------------|------|
| P1 | 重复特性 | 同一功能出现 `### WebGPU: 3D texture ...` 与 `## 3D texture ...` | 统计重复 / 噪声 |
| P2 | Heading 层级混乱 | `## WebGPU Features` 下直接跟多组 `##` | 解析粒度不稳定 |
| P3 | dedicated 内容整体视为单 feature | 无法对内部细粒度过滤/去重 | 后续分类困难 |
| P4 | 去重缺失 | 合并阶段未启用 dedup | 噪声传递到 YAML |
| P5 | 标题前缀未归一化 | `WebGPU:` / 标点差异 | 归一化 & 去重效果差 |
| P6 | 来源不可追溯 | feature 不携带 source meta | 调试困难 |
| P7 | H2 未统一降级 | 与包装层冲突 | 继承“WebGPU”语义放大 |
| P8 | 未来污染风险 | 祖先含 WebGPU 关键词 | 误分类持续扩散 |

### 13.2 目标补充

1. 结构规范：单一 heading 递进，不混平级包装。
2. 去重前置：降低后续 pipeline 负担。
3. 语义归一：标题、前缀、来源一致化。
4. 粒度统一：所有来源拆分到可比较粒度。
5. 可审计：每条 feature 可回溯来源集合。

### 13.3 策略选项

| 维度 | 方案 | 说明 | 推荐 |
|------|------|------|------|
| 包壳 `## WebGPU Features` | A 保留+内部降级 | 语义聚合清晰 | A |
|  | B 去除包壳 | 更扁平 | 备选 |
| dedicated 处理 | 拆分为多 feature | 按 H2 分段 | 推荐 |
| Heading 降级 | `##`→`###` (dedicated 内) | 避免冲突 | 必做 |
| 去重 | 启用 `deduplicate_features()` | 标题+issue+长度 | 必做 |
| 标题归一 | 新方法 `normalize_webgpu_title` | 去前缀/尾标点 | 必做 |
| 来源标记 | HTML 注释或字段 | `<!-- sources: a,b -->` | 必做 |
| 调试输出 | Footer 差异摘要 | 原/去重数量 & 列表 | 建议 |

### 13.4 标题归一化规则

1. 去前缀：`^(webgpu:?\s+)`（忽略大小写）
2. 去尾部多余标点 `[:：.。]`
3. 折叠多空格
4. 统一为原始大小写（不强制再格式化）

### 13.5 去重决策顺序

1. 标准化标题完全相同 → 比较优先级 (priority 数值小者胜)
2. 若优先级相同 → 内容长度（字符数）长者胜
3. 若仍相同 → issue id 数量多者胜
4. 最终合并来源集合（sources 去重）

### 13.6 伪代码补充

```python
def normalize_webgpu_title(t):
    t = re.sub(r'^webgpu:?\s+', '', t, flags=re.I)
    t = re.sub(r'[\s:：.。]+$', '', t)
    return ' '.join(t.split())

def choose(a, b):  # 返回保留项
    if a.priority != b.priority:
        return a if a.priority < b.priority else b
    if len(a.content) != len(b.content):
        return a if len(a.content) > len(b.content) else b
    if len(a.issue_ids) != len(b.issue_ids):
        return a if len(a.issue_ids) > len(b.issue_ids) else b
    return a  # 默认
```

### 13.7 新增验收标准

| 编号 | 新增 | 标准 |
|------|------|------|
| AC7 | 是 | 标准化后 WebGPU 标题唯一 |
| AC8 | 是 | 不出现包壳与内部同级 H2 冲突（策略 A 则内部无 `##`；策略 B 则无包壳） |
| AC9 | 是 | 每条 feature 输出来源注释或结构字段 |
| AC10 | 是 | Footer 含原始/去重计数与去除标题列表（<=10） |

### 13.8 实施顺序（增量）

1. 工具函数：标题归一 + 去重（独立、暂不接入）。
2. dry-run 模式：输出 diff（不改现有产物）。
3. 接入 merge：启用降级+拆分+去重（受 `MERGE_WEBGPU_STRICT` 控制）。
4. 添加来源注释与 footer 摘要。
5. 生成 137/138/139 diff 报告。
6. 增加结构 & 去重测试。
7. 默认开启，保留回退。

### 13.9 回退与配置

| 变量 | 用途 | 默认 | 说明 |
|------|------|------|------|
| MERGE_WEBGPU_STRICT | 启用新合并/去重/降级逻辑 | 0 | 1 时开启新策略 |

### 13.10 风险补充

| 风险 | 场景 | 缓解 |
|------|------|------|
| 代码块内误降级 | 代码 fenced 中含 "##" | 预处理：跳过 fenced 范围 |
| 去重误杀 | 单词标题 `Updates` 多来源 | 增加内容长度 + issue 数量比较 |
| 性能 | 多版本批处理 | 文件体积小，可忽略 |

### 13.11 后续增强（可选）

- 产出 `graphics-webgpu-index.json`（标题映射）。
- YAML 中加 `normalized_title` 字段。
- 统计被剥离前缀比例监控数据源质量。

### 13.12 待确认决策

| 决策 | 选项 | 推荐 | 状态 |
|------|------|------|------|
| 包壳策略 | A 保留 / B 去除 | A | 使用推荐选项 |
| dedicated 拆分 | 拆 / 不拆 | 拆 | 使用推荐选项 |
| 来源记录形式 | 注释 / 字段 / 二者 | 注释+字段 | 使用推荐选项 |

> 等待确认上述决策后再进入实现阶段。
