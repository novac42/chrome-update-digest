# 0817 WebPlatform 按 Focus Area 拆分 Digest 设计与实施计划（更新版）

> 本文件已在 2025-08-16 更新：采纳“不要直接用脚本生成每个 area 的 deterministic digest”，改为：YAML 只提供权威特性列表；每个 area 的 digest 仍由 LLM 生成（结构 + 解释），脚本仅负责遍历、输入裁剪、验证、重试与落盘。之前 draft 中的“规则式风险分类 / 纯脚本 digest”已废弃。

## 背景
当前 WebPlatform digest 生成通过增强版工具 (EnhancedWebplatformDigestTool) 主要输出“全领域”综合摘要，或单个 target_area。采样生成的 digest 需求与 pipeline 设计不一致：期望一次运行即可为所有 focus areas 生成各自的 digest（支持多语言），而当前仅在 YAML 层可以 `split_by_area`，后续 LLM 生成未批量执行。

## 目标
一次调用（`split_by_area=True`）实现：
1. 遍历所有 focus areas，逐个向 LLM 提供经裁剪的 YAML 特性列表，由 LLM 生成该 area 的 digest（en / zh 或 bilingual）。
2. Prompt 中用对应 area 展示名替换 `[AREA]`；强调“只能使用给定 feature 标题与链接，不得虚构”。
3. 脚本负责：YAML 缓存检查、area 遍历、特性截断、拼装 prompt、结果验证（标题/链接子集）、异常与重试、输出路径组织。
4. 统计准确：每个 digest 的量化信息来自其 area YAML，不由 LLM 推断。
5. 返回结构化 JSON：成功 / 失败 / 重试 / 验证警告（missing_titles, extra_links 等）。
6. 可选全局执行摘要（单次 LLM）基于各 area 的 stats 汇总。
7. 双语模式改为：先生成英文权威版本（唯一“语义源”），再通过独立“翻译 / 本地化” prompt 将英文 digest 转换为中文；翻译阶段不得增删特性、不得改链接、不得引入新内容。

## Root Cause 不一致点
| 问题 | 现状 | 影响 |
|------|------|------|
| 产物粒度 | 仅全局 / 单 area | 无法批量产出按领域 digest |
| `split_by_area` 只限 YAML | LLM 未循环生成 | 丢失设计意图 |
| Prompt 未针对所有 area 自动替换 | 仅全领域替换 | 每 area 缺乏专属语境 |
| Area 名归一化不统一 | 只特判 webgpu | 目录 / 文件命名不稳 |
| 错误处理粗粒度 | 整体 try/except | 局部失败会中断全流程 |
| 测试缺失 | 无 per-area 覆盖 | 回归风险高 |
| 小样本优化缺失 | 统一走 LLM | 资源浪费、易超限 |

## 范围
In-scope:
- 生成逻辑增强
- Prompt 替换 & area 展示名
- 错误/结果结构 & 测试
- 文档更新

Out-of-scope（暂不做）:
- LLM 并发优化
- Incremental hashing 去重
- Web API 子分类拆分

## 实施步骤
### 1. Area 归一化
新增帮助函数：`normalize_area(name)`，映射保持不变：
- webgpu/gpu/graphics → graphics-webgpu
- security/privacy → security-privacy
- pwa/service-worker → pwa-service-worker
- loading/navigation → navigation-loading
- trials/origin-trials → origin-trials
- 余下按 key 直接匹配

### 2. 缓存与提取
- 若 `split_by_area=True`：检测根 tagged YAML 与各 area 子目录 YAML 是否存在；缺失则运行一次 `process_release_notes(... split_by_area=True)`。
- 保留现有 `-tagged.yml` 以便全领域 digest 仍可生成。

### 3. Per-area 循环 + LLM 生成（无纯脚本 digest）
伪代码：
```
areas = yaml_data.get('areas') or scan(cache_dir)
langs = ['en','zh'] if bilingual else [language]
for area in areas:
  load area_yaml
  build feature list (title + truncated content + links)
  prompt = build_system_prompt(area) + build_user_prompt(feature_yaml)
  resp = sample()
  validate(resp, area_yaml)
    if failed: retry (<= retry_limit) with corrective note
    if still failed: fallback = minimal markdown (列出所有标题与链接 + 失败说明)
  save digest
  collect status / anomalies
```

特性截断策略：每个 feature content 取前 N 字符（默认 300，按 UTF-8 字符长度），避免 token 膨胀。

### 3.1 双语输出策略 (English → Translation)
原逻辑（分别针对 en/zh 生成）存在：
- 语义漂移风险（两次独立生成可能结构不一致）
- Token & 成本翻倍

新策略：
1. 每个 area 只进行一次英文生成（English Canonical Digest）。
2. 通过翻译/本地化 prompt 输入：
  - 原英文 markdown digest（不再提供 YAML）
  - 约束列表（保留标题层级、保留链接、保留 Impact Level 表情符号、保留引用列表）
3. 翻译输出：中文 digest（同结构、同标题顺序）
4. 验证：
  - 标题数量 & 顺序与英文一致
  - 链接集合完全相同
  - 不新增英文原文中未出现的特性标题
5. 失败处理：一次重试，仍失败则 fallback（附说明：翻译失败，请人工处理），但英文版本仍可用。

翻译 prompt（已落盘 / 权威版本）：`prompts/webplatform-prompts/webplatform-translation-prompt-zh.md`

说明：
1. 下面保留摘要片段仅用于文档速览；实际实现时请直接读取上述文件内容，以确保术语映射与约束同步更新。
2. 该文件中已包含术语映射（含 “performance regression → 性能回退” 等），以及结构 / 链接保持等硬性约束；如需扩展术语请修改文件后同步更新测试。
3. 若英文 prompt / 术语表升级，只更新该文件，不在代码里硬编码多份副本。
（摘要片段示例，非完整内容）：
```
System: You are a professional bilingual technical localizer. Translate the provided Chrome Web Platform area digest from English to Simplified Chinese.

Key Hard Constraints (see file for full list):
1. Preserve ALL markdown structure (headings hierarchy, bullet/numbered lists, blockquotes, tables, code fences).
2. Feature titles: keep exact original wording; if需要补充中文，可采用「原英文（中文说明）」形式，但不得删除英文核心术语。
3. Order immutability: do NOT reorder, merge, split, add, or remove features / sections.
4. Links: preserve every URL & anchor text exactly; no new links.
5. Emojis & impact indicators (🔴 / 🟡 / 🟢) unchanged.
6. Only translate narrative prose; keep code identifiers, API names, spec IDs, issue numbers as-is.
7. No hallucination, no speculative additions.
8. Terminology mapping MUST be applied (e.g., performance regression → 性能回退).
9. If ambiguity: choose literal, concise translation; avoid explanatory expansion.

User Content Placeholder: <ENGLISH_DIGEST_MARKDOWN>
```

翻译验证逻辑：
- `extract_headings(en)` vs `extract_headings(zh)` → 序列相等
- `extract_links(en)` 集合 == `extract_links(zh)` 集合
- 若不一致：补充纠错提示与差异列表再重试一次。

### 4. Prompt 替换
`_load_prompt`：
- `display_name = FocusAreaManager.get_area_display_name(area)`
- 替换 `[AREA]` 为 display_name；中文模板特殊短语也调整。
- 全领域模式保留现有 “all areas” 替换逻辑。

### 5. 验证 & Fallback 策略
验证规则（脚本）：
1. 抽取输出 Markdown 的 feature 标题（H3/H4 或保留原始标题精确匹配）。
2. `missing_titles_ratio = missing / total_yaml_titles`；若 > 0.3 视为失败。
3. 发现输出中“未知标题”或“未知链接”视为失败；未知链接 = 不在 YAML 链接集合。
4. 警告级别：`extra_links` 数量 >0 且 ≤2；严重：>2 或出现未知标题。

重试：
```
attempt 1 -> fail -> prepend corrective note (列出缺失/非法条目) -> attempt 2
attempt 2 -> fail -> fallback (minimal list + failure note)
```

Fallback 格式：
```
# Chrome {version} {Area Display} Digest (Fallback)
> LLM generation failed after {retries} attempts. Below is the raw feature list.

## Features
### {Feature Title}
Links: - [Spec](...) - [Issue](...)
```

不再使用规则引擎进行风险分类；风险与影响全部由 LLM 负责表述。

翻译 Fallback：
```
# Chrome {version} {Area Display} Digest (中文翻译失败)
> 自动翻译失败（{retries} attempts）。请参考英文版：{english_path}
```

### 6. 结果 JSON 结构
```
{
  success: bool,
  mode: "per_area",
  version, channel,
  language: "bilingual" | "en" | "zh",
  languages: ["en","zh"],
  areas: [...],
  outputs: { area: { en: path, zh: path } },
  errors: { "area:lang": "message" }
}
```

### 7. Others 处理
保持生成：
- 若 features=0 → 直接生成 fallback 风格 minimal（无需调用 LLM）。
- 若 features>0 正常走 LLM。

### 8. 文件命名 & 路径
英文（canonical）：`digest_markdown/webplatform/<area>/chrome-<version>-<channel>-en.md`
中文（翻译）：`digest_markdown/webplatform/<area>/chrome-<version>-<channel>-zh.md`
失败 fallback：添加后缀 `(fallback)` 说明写入文件头部，而非文件名（保持路径稳定）。

### 9. 测试计划
新增测试 `tests/test_webplatform_per_area_generation.py`：
- Mock ctx.sample → 固定输出（避免真实 LLM）。
- 调用 run(version, channel, split_by_area=True, language='bilingual').
- 断言：
  - 返回 JSON success 且 `outputs` 至少包含配置里前若干核心 area（css, webapi, graphics-webgpu）。
  - 每个生成文件存在且非空。
  - bilingual：同一 area 下 en 与 zh 文件都存在，且标题序列 & 链接集合与英文一致。
  - 小样本 fallback（可构造极简 YAML）情况下内容含 fallback 标题。
- 断言错误收集：人为注入一个缺失 YAML 场景时保留其余成功。
 - 注入翻译错误（模拟输出缺失几个标题）→ 触发翻译重试并最终 fallback。
 - 翻译 Prompt 文件读取验证：在测试前向 `prompts/webplatform-prompts/webplatform-translation-prompt-zh.md` 末尾临时追加唯一标识注释（如 `<!-- TEST_TOKEN_123 -->`），运行翻译后断言发送给 LLM 的 prompt（或构造的 prompt 文本缓存）包含该标识，从而确认未使用硬编码常量。测试结束后回滚文件（或使用临时写入+恢复）。
 - 术语映射动态性：在测试中临时添加新的术语映射行（如 `throughput variance → 吞吐波动`），并在英文 digest 中植入该短语，验证翻译结果包含预期中文且英文术语结构保持（用于保证读取的是最新文件内容）。
 - 防止多份副本：静态扫描实现代码（utils / mcp_tools）中不应出现大段翻译 prompt 主体（> 30 连续英文单词），否则测试失败。

### 10. 文档更新
- `docs/tech_docs`：本文件。
- `README.md`：新增使用示例：
  - 参数说明 `split_by_area=True`。
  - bilingual 与单语言示例。
  - 输出目录结构。
- `output_configuration.md`：补充 per-area digest 命名规范。

### 11. 质量与风险
| 风险 | 缓解 |
|------|------|
| LLM 虚构特性/链接 | 严格标题/链接白名单校验 + 重试纠错提示 |
| Token 过长 (webapi) | 内容截断 + 仅保留首段；未来可分片 |
| 多次失败导致空洞输出 | Fallback 最小清单保障信息完整性 |
| 并发调用速率限制 | 初始串行；后续可配置并发池 |
| Bilingual 成本高 | 改为单次英文 + 翻译第二次调用，减少重复生成风险与代价 |
| 翻译结构破坏 | 结构/链接/标题序列校验 + 纠错重试 |

### 12. 后续可选优化
- Hash 内容避免重复生成。
- 并发 + 速率限制管理。
- 分块 summarization（先 area 内小特性→再汇总）。
- 统计汇总生成 `summary-index.md` 方便导航。

## 实施优先级顺序（微里程碑）
1. Area YAML 读取 + 遍历框架 + 输出路径组织
2. 英文 Prompt builder + 英文生成 + 英文验证
3. 翻译 prompt + 翻译执行 + 翻译验证 + 翻译重试
4. Fallback 处理（英文 & 翻译）
5. Bilingual 汇总 JSON 扩展字段（translation_status）
6. 全局摘要（可选）
7. 测试用例（包括翻译验证场景）
8. README / 文档更新
9. 日志与参数优化

## 验收标准
1. 单次运行（mock LLM）为所有 areas 生成英文 digest 并随后生成中文翻译（或 fallback），无未捕获异常。
2. 英文与中文文件标题序列完全一致（测试断言）。
3. 中文 digest 链接集合与英文完全一致（集合相等）。
4. 翻译重试逻辑在模拟异常时被触发并正确 fallback。
5. JSON 返回含 `translation_status` 字段，记录每个 area 的 zh 状态（ok/retry/fallback）。
6. README 更新包含新的 bilingual 架构说明。
7. Fallback 中文文件包含指向英文原文的路径引用。
 8. 翻译 prompt 与术语映射必须在运行时从文件 `prompts/webplatform-prompts/webplatform-translation-prompt-zh.md` 读取；修改该文件（添加测试标记或新增术语）无需改动代码即可反映在翻译结果中（测试证明）。
 9. 代码库中无硬编码冗长翻译 prompt 文本（通过测试的静态扫描验证），仅允许最少的占位符拼接逻辑。

---
作者: 自动生成计划（更新）
日期: 2025-08-16
