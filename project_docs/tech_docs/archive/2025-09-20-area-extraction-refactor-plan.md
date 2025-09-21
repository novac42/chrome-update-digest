# Chrome 140 多领域提取修复与层级分析改进计划

日期: 2025-09-20
状态: 进行中
负责人: （自动生成）

## 背景
在处理 Chrome 140 WebPlatform release notes 时，流水线仅生成了 `graphics-webgpu` 一个领域，缺失了 CSS / DOM / JavaScript / Web APIs / Service worker / Origin trials / Removals 等其它区域。经分析：

1. `focus_areas.yaml` 初始加载路径曾失败，导致使用空配置 fallback。
2. 层级分析 `detect_heading_hierarchy()` 在标准结构（H2 = 领域，H3 = feature）情况下未强制判定，退化为单一区块。
3. 领域映射 `_map_area_name` 虽大小写不敏感，但缺少：
   - `JavaScript` 专门配置
   - `Isolated Web Apps (IWAs)` 归属策略
   - 更明确的 `Removals` → `deprecations` / `Service worker` → `pwa-service-worker` / 别名
4. WebGPU 具有特殊多版本格式（有时只有一级 heading，有时嵌套），当前逻辑对其做了更多兼容，需要保留。

## 目标
- 正确解析 Chrome 140 全量领域并输出对应 markdown + YAML。
- 增加 JavaScript / Isolated Web Apps 领域支持。
- 保持/强化 WebGPU 自适应层级解析，避免对 136–139 版本发生回归。
- 提供后续回归测试和覆盖率改进方向。

## TODO 列表（同步自交互式任务追踪）
| ID | 状态 | 任务 | 说明 |
|----|------|------|------|
| 1 | ✅ 完成 | Explain原因与修复计划 | 形成根因分析与修复路径 |
| 2 | ⏳ 待办 | 更新focus_areas.yaml | 新增 javascript / isolated-web-apps 区域 |
| 3 | ⏳ 待办 | 改进detect_heading_hierarchy算法 | H2/H3 快速路径：≥2个 H2 且存在 H3 → 直接 section=2 feature=3 |
| 4 | ⏳ 待办 | 保留并强化WebGPU专用层级分析 | 对 WebGPU 内容继续使用动态推断分支 |
| 5 | ⏳ 待办 | 扩展_map_area_name别名映射 | 新增多组别名匹配逻辑 |
| 6 | ⏳ 待办 | 重新运行140处理流水线 | 生成多领域 markdown + YAML |
| 7 | ⏳ 待办 | 验证生成的领域文件 | 检查目录与 feature 数量 |
| 8 | ⏳ 待办 | 回归测试其它版本 | 采样 136–139 重新跑并对比差异 |
| 9 | ⏳ 待办 | 总结与后续建议 | 输出改进报告 |
| 10 | ✅ 进行中 | 保存TODO计划为Markdown | 本文件 |

## 设计方案
### 1. focus_areas.yaml 变更
新增：
```yaml
  javascript:
    name: "JavaScript"
    description: "JavaScript language and runtime features"
    priority: 2
    heading_patterns:
      - "JavaScript"

  isolated-web-apps:
    name: "Isolated Web Apps"
    description: "IWA platform and controlled frame APIs"
    priority: 3
    heading_patterns:
      - "Isolated Web Apps"
      - "Isolated Web Apps (IWAs)"
```

### 2. 层级快速判定逻辑
伪代码：
```python
h2_count = count('^## ')
h3_count = count('^### ')
if h2_count >= 2 and h3_count >= 2:
    section=2; feature=3
else:
    # fallback to现有 detect_heading_hierarchy()
```

### 3. WebGPU 专用保留策略
- 进入 `merge_graphics_webgpu` 时，WebGPU 原文处理仍调用动态层级检测，不走快速强制模式。
- 条件：若文件标题包含 `WebGPU` 且来源于独立 webgpu note，则不套用快速路径。

### 4. 别名映射增强
新增规则：
- `service worker` / `service workers` → `pwa-service-worker`
- `removals` → `deprecations`
- `isolated web apps` / `isolated web apps (iwas)` → `isolated-web-apps`
- 保留已有 fallback（未命中则 kebab-case 原样输出）。

### 5. 回归测试策略
| 版本 | 关注点 | 验证项 |
|------|--------|--------|
| 136 | WebGPU 历史结构 | feature 数不减少 |
| 137 | 正常结构 | h2/h3 分层正确 |
| 138 | 单层 WebGPU | 仍能提取所有 features |
| 139 | Dawn 更新段落 | 去重合并逻辑不变 |
| 140 | 多领域 | 领域总数≥8 |

### 6. 潜在风险与缓解
| 风险 | 影响 | 缓解 |
|------|------|------|
| 错误强制 H2/H3 | 破坏非标准结构 | 仅在双条件(h2≥2 & h3≥2)下启用 |
| WebGPU 回归 | 丢失特性 | 保留动态分支与判定标志 |
| 新增领域影响统计 | 旧脚本未识别 | 增加回归测试清单 |

### 7. 后续增强建议
- 引入简单 snapshot（每版本 area→feature_count JSON）用于自动 diff。
- 集成 `pytest` fixture 生成临时解析结果并断言领域数量。
- 增加 CLI 参数 `--debug-hierarchy` 输出判定细节。
- 增加 `--areas-filter` 仅处理指定区域加速调试。

## 执行步骤（实施顺序）
1. 编辑 `config/focus_areas.yaml` 添加新区域。
2. 修改 `detect_heading_hierarchy()` + 调用入口逻辑条件分支。
3. 扩展 `_map_area_name` 别名判断。
4. 重跑 140 → 验证。
5. 采样重跑 136–139 → 观察输出差异（行数、feature计数）。
6. 汇总结果，补充改动说明。

## 完成标准
- 运行 140 后 `areas/` 目录含目标领域子目录，每个有 markdown（≥1 feature）。
- WebGPU YAML 仍生成且 feature 数 == 6（当前）。
- 其它领域非空：例如 `css` > 5 features，`javascript` ≥1，`origin-trials` ≥3。
- 回归版本未出现显著 feature 丢失（阈值 <5% 变动）。

---
（自动生成文档，后续更新进度可在此文件追加 “进度” 小节）
