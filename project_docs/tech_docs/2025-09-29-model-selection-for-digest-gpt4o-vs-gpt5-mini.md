# WebPlatform 摘要生成模型选型建议：gpt‑4o vs gpt5‑mini

更新时间：2025-09-29

## 摘要
- 生产首选 gpt‑4o：更稳定遵守结构化提示、较少重试、语义质量更高，适合大 YAML（如 css/webapi）与一稿过的发布场景。
- 成本/批量首选 gpt5‑mini：结合现有“分区生成 + 结构/链接校验 + 重试 + 降级”管线，可达到可用质量，但更易触发一次重试或降级。
- 性价比高的混合方案：英文摘要用 gpt‑4o、中文翻译用 gpt5‑mini；或体量/复杂度高的领域（css/webapi/graphics-webgpu）用 gpt‑4o，其他领域用 gpt5‑mini。

## 当前生成管线要点
- 入口工具：`src/mcp_tools/enhanced_webplatform_digest.py`
  - 英文摘要：`_generate_digest_from_yaml()` 内调用 `ctx.sample(...)`，有超时+指数退避重试（默认 `temperature=0.7`，`WEBPLATFORM_MAX_TOKENS` 默认为 12000，可调）。
  - 分区并行：按领域（CSS、WebAPI、WebGPU 等）并行生成，含进度记录与结果落盘。
  - 英文摘要校验：`_validate_digest()` 检查 YAML 特性标题覆盖率及未知链接数，不通过会基于问题重试一次，仍失败则走降级模板。
  - 中文产出：`_translate_digest()` 使用 `prompts/webplatform-prompts/webplatform-translation-prompt-zh.md` 将英文摘要翻译为中文；`_validate_translation()` 强约束结构与链接集合一致，失败重试一次，否则降级。
- 提示词：
  - 英文摘要提示：`prompts/webplatform-prompts/webplatform-prompt-en.md`（强约束：H3 特性标题、References 保留全部链接、仅用 YAML 数据）。
  - 中文翻译提示：`prompts/webplatform-prompts/webplatform-translation-prompt-zh.md`（结构/链接严格一致，不允许新增/丢失）。
- YAML 输入：`upstream_docs/processed_releasenotes/processed_forwebplatform/areas/*/chrome-*-stable.yml`，单文件通常 5–20 KB 文本级别。

## 适配 gpt5‑mini 的可行性评估
- 上下文体量：单领域 YAML + 提示词低于常见 8k–16k 窗口，分区生成避免超长上下文；可行。
- 任务类型：以 YAML 为源的结构化摘要与严格受限的翻译，均适合 mini 模型；现有校验/重试/降级路径可兜底。
- 风险点：mini 更易出现轻微结构漂移（标题级别/顺序）或链接遗漏/新增；但英文有缺失率与“未知链接数”阈值校验，中文有结构/链接集合比对，整体可控。

## 选型建议
1) 生产与高质量发布：优先使用 gpt‑4o
   - 优势：
     - 更稳定遵循提示词结构，减少 `_validate_digest()` 和 `_validate_translation()` 的重试命中率；
     - 叙述质量更高，技术措辞更细腻，特别适合体量大或复杂度高的领域（css、webapi、graphics-webgpu）。

2) 成本敏感或批量处理：可用 gpt5‑mini
   - 前提：保留现有“分区 + 校验 + 重试 + 降级”机制；
   - 预期：偶发一次重试或个别领域降级可接受。

3) 混合策略（推荐的性价比方案）
   - 英文摘要用 gpt‑4o，中文翻译用 gpt5‑mini（翻译有强结构校验，mini 足以胜任）；
   - 或者对 css/webapi/graphics-webgpu 用 gpt‑4o，其余领域（devices/multimedia/identity 等）用 gpt5‑mini。

## 模型参数与执行建议
- gpt5‑mini：
  - 温度建议从 0.7 下调至 0.2–0.3，降低结构漂移风险（代码位于 `_safe_sample_with_retry()` 的 `temperature=0.7`）。
  - `WEBPLATFORM_MAX_TOKENS` 建议 8000–10000，以平衡失败率与输出完整度。
  - 如遇速率限制，降低分区并发度（现有实现易于加信号量控制）。
- gpt‑4o：
  - 温度 0.3–0.5 可在稳定与语义质量间取得平衡。
- 两者通用：
  - 继续使用 `_validate_digest()` 与 `_validate_translation()` 的严格校验与一次重试策略，必要时触发降级生成/占位；
  - 监控 `.monitoring/webplatform-progress.json` 进度，以及时发现异常领域并人工复核。

## 可落地改动（小改即可提升稳健性）
1. 把温度与并发度做成配置项：
   - 在 `EnhancedWebplatformDigestTool._safe_sample_with_retry()` 支持从环境变量或配置文件读取 `temperature` 与并发上限；
   - 为 mini 档位预设低温度、适中 `max_tokens`、限制并发。
2. 按领域设定模型档位：
   - 在 orchestrator 增加“领域→模型档位”的映射表（如 css/webapi/WebGPU → gpt‑4o，其他 → gpt5‑mini）。
3. 失败路径的观测性：
   - 记录每个领域的重试次数、触发原因（缺失率/未知链接数/翻译结构不一致），便于后续微调提示词或参数。

## 结论
- 在现有“分区 + 校验 + 重试 + 降级”的架构下，gpt5‑mini 可满足成本/批量场景；
- 面向稳定生产与更高文本质量，首选 gpt‑4o；
- 建议采用“英文摘要 gpt‑4o + 中文翻译 gpt5‑mini”的混合方案，并将温度/并发做配置化以进一步降低失败率。

