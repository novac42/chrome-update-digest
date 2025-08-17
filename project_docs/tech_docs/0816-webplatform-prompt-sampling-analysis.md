# 0816 WebPlatform Prompt & Sampling 结构改进分析副本

(本文件为 `0816-webplatform-sampling-diff.md` 的补充/派生，聚焦 prompt 设计与单次英文采样策略。)

> 来源文件：0816-webplatform-sampling-diff.md 复制于 2025-08-16

---

（以下为原始内容复制，便于在本副本上继续迭代 prompt 方案）

```markdown
# 0816 WebPlatform 与 Enterprise Digest Sampling 实现差异分析

更新时间: 2025-08-16
作者: 内部技术记录

## 结论速览
WebPlatform 版本的 sampling 可靠性与输出质量低于 Enterprise，核心原因是：调用模式（system prompt 传递方式 + messages 结构）、缺少超时与严格失败信号、Fallback 设计掩盖真实错误、上下文体量偏大、与 Enterprise 不一致的重试与日志策略。

---
## 1. 调用接口与参数差异
| 维度 | Enterprise | WebPlatform | 影响 |
|------|------------|-------------|------|
| system prompt 传递 | 单独 system_prompt 参数 + 单一 messages 字符串 | 作为第一条 system role 消息放在 messages 列表 | 可能与 fastmcp.sample 内部分支不一致，降低系统指令权重 |
| messages 结构 | str（完整 prompt + 数据） | list[system, user, user] | API 行为差异风险；token 估算不同 |
| 模型偏好 | ["claude-4-sonnet", "gpt5"] | ["claude-3-5-sonnet-latest", "gpt-4"] | 命中可用模型概率 & 能力差异 |
| temperature | 0.7 | 0.4 | 风格/多样性 vs 稳定性，不是主因但影响输出形态 |
| max_tokens | 50000 | 40000 | 长上下文截断风险不同 |
| timeout | asyncio.wait_for(timeout=60) | 无显式 timeout | WebPlatform 可能挂起/等待无反馈 |
| 重试间隔 | 指数退避 1,2,4 秒（统一） | 指数退避 1,2,4 秒 | 相同，但缺少 timeout 分支区分 |
| 错误分类 | 区分 TimeoutError & Exception | 不区分，统一处理 | 难以定位是超时还是其他错误 |

---
## 2. Prompt / 上下文组织方式
- Enterprise: 在开头硬编码 MANDATORY FORMAT REQUIREMENTS，强约束章节结构与语言规则，减少 LLM 偏移。
- WebPlatform: 依赖模板 + YAML 数据块（```yaml ...```）。约束语义更松散，输出结构易漂移。
- WebPlatform 已经实现“按 area 生成/缓存”拆分 (split_by_area / area 子目录)，但在当前 bilingual 流程中：
	* 若一次生成全局 digest（不指定 target_area），仍会加载汇总 tagged YAML（体积仍大）。
	* 每个单独 area 生成时上下文已较小——进一步优化空间主要在字段裁剪与特性筛选，而非再次分拆。
	* 双语言模式对同一 YAML 再调用一次，导致总体 token *2。

---
## 3. 资源加载策略
- Enterprise: 优先 `ctx.read_resource("enterprise-prompt")`（支持资源层热更新 / 环境切换）。
- WebPlatform: 直接文件系统读取，不利用 MCP 资源抽象 → 难以动态替换。

---
## 4. 失败与回退 (Fallback) 行为
| 方面 | Enterprise | WebPlatform | 问题 |
|------|------------|-------------|------|
| 失败后返回 | 抛异常，外层 JSON 包装 success=False | 静默 fallback 生成“Unknown”版本摘要 | 掩盖真实失败，监控难 |
| fallback 内容 | 不生成伪结果（直接失败） | 生成极简摘要（丢失 YAML 统计） | 误导调用方“成功” |
| 诊断信息 | 打印 timeout / failure 原因 | debug=True 时才打印 attempt | 默认情况下信息缺失 |

---
## 5. 多语言策略
- Enterprise: 一次生成（中文正文 + 英文标题） → 单次风险。
- WebPlatform: EN 与 ZH 各调用一次（或 bilingual 两次） → 失败概率翻倍；重复传入大 YAML。

---
## 6. 质量与一致性风险清单
1. system_prompt 未通过专用参数传递 → 可能失去内部加权。  
2. 无 timeout → 阻塞时无快速失败。  
3. Fallback 静默 → 真实失败被吞。  
4. YAML 体积大 + 双语言重复 → token 压力高。  
5. messages list 与 Enterprise 字符串模式不一致 → 行为差异未验证。  
6. 模型列表不统一 → 成功率差异。  
7. 缺少结构化返回（无 success 字段） → 难以自动监测失败。  
8. Prompt 约束力较弱 → 输出结构漂移。  

---
## 7. 优先级排序改进建议（按 ROI）
| 优先级 | 改进项 | 目标 | 预估难度 | 预期收益 |
|--------|--------|------|----------|----------|
| P0 | 增加 timeout + 分类重试 | 防止挂起，区分超时 vs 其他错误 | 低 | 提升可控性 |
| P0 | 去除静默 fallback；返回结构化错误 | 真实暴露失败 | 低 | 避免假成功 |
| P0 | 与 Enterprise 对齐 system_prompt 参数使用 | 统一模型行为 | 低 | 减少不可解释差异 |
| P1 | YAML 字段裁剪（已按 area 分拆，继续移除冗余字段：统计/未用 tag 细节） | 降低 token 与延迟 | 中 | 减少超时/截断 |
| P1 | 输出统一 JSON：success, path, preview, stats | 监控 & 自动化 | 低 | 运维友好 |
| P1 | 单次生成后二次翻译（减少双大调用） | 减少调用次数 | 中 | 失败面减半 |
| P2 | 统一模型偏好列表，增加后备 | 提高命中率 | 低 | 稳定性提升 |
| P2 | 强化模板：显式章节 & 必填校验指令 | 稳定结构 | 低 | 输出更一致 |
| P3 | 引入 resource 读取 prompt | 动态配置 | 低 | 长期维护便利 |
| P3 | 失败时保留 YAML 统计并写入错误文件 | 现场复盘 | 低 | 排错加速 |

---
## 8. 建议的最小改动补丁轮廓（示意）
```python
# 1. 构造 system_prompt + user_content 合并为单字符串 OR 保留 messages 但同时传 system_prompt
response = await asyncio.wait_for(ctx.sample(system_prompt=system_prompt, messages=messages, ...), timeout=60)

# 2. 统一返回结构
def _result(success, **kwargs):
	return json.dumps({"success": success, **kwargs}, ensure_ascii=False)

# 3. 失败不直接 fallback，而是 success=False；保留 debug 信息
```

---
## 9. 验收指标 (Proposed KPIs)
| 指标 | 基线 (估计) | 目标 |
|------|-------------|------|
| WebPlatform 采样成功率 (无 fallback) | 未监控 | ≥ 95% |
| 平均生成耗时 (单语言) | 未测 | < 25s (p95 < 40s) |
| 超时占比 | 未监控 | < 2% |
| 结构校验失败率 (章节缺失) | 偶发 | < 1% |
| 重试平均次数 | 未监控 | < 1.3 |

---
## 10. 后续实施顺序
1. 引入 timeout + 结构化错误返回（P0）。
2. 移除静默 fallback（保留可手动触发的 debug fallback）。
3. 同步 system_prompt 传参形式并统一模型列表。
4. 添加 JSON 返回封装层，接入监控（日志 or 指标埋点）。
5. 减少上下文体积（当前已按 area 分拆 → 继续做字段裁剪 & 特性筛选 + 单次英文采样策略）。
6. 增强模板硬约束（章节、语言、不可编造链接）。
7. 资源化 prompt 与失败工件持久化。

---
## 11. 风险与注意点
- 大幅裁剪 YAML 需确保后续分类/引用逻辑不依赖被移除字段。
- 二次翻译策略需验证不会引入链接/术语丢失。
- timeout 设置过短会造成不必要重试；建议先 60s，再依据 p95 调整。
- 模型列表需与后端可用清单校验，避免无效名称导致全部重试。

---
## 12. 快速检查清单 (实施后自测)
- [ ] EN / ZH 输出都包含核心章节 & 无“Unknown”占位。
- [ ] JSON 返回 success=true 且有 content_length / path。
- [ ] 人为制造网络异常能看到 success=false 明确 error_type。
- [ ] 超时场景在 60s 左右即返回，不超过 70s。
- [ ] retry 日志包含 attempt 次数与等待间隔。
- [ ] YAML 体积裁剪后 token 计数下降（可打印估值）。

---
## 13. TL;DR
WebPlatform sampling 不稳定主要源于：缺失超时、静默 fallback、上下文体量偏大、system_prompt 用法不统一。先对齐 Enterprise 的调用契约 + 增加可观测性，再做上下文优化与多语言策略收敛，可快速提高成功率与可维护性。

---
## 14. “单次英文采样 + 二次翻译”策略设计（新增）
目标：用一次高质量英文 LLM 采样生成结构化 digest，再用轻量翻译步骤派生中文，降低失败面 & 成本，提高可控性。

### 14.1 核心动机
| 问题 | 当前双采样影响 | 单采样+翻译缓解方式 |
|------|----------------|----------------------|
| 采样调用次数 | 2 次 (EN, ZH) | 1 次 (EN) |
| 失败概率 | p_fail^2 级叠加 | 降为 p_fail |
| Token 成本 | 两份大 YAML 上下文 | 只对英文调用大模型；翻译成本小 |
| 结构漂移 | 两次各自可能偏移 | 结构先锁定，再镜像翻译保持 |
| 结果一致性 | EN / ZH 可能章节不匹配 | ZH 基于 EN 结构逐段翻译 |

### 14.2 流程概述
1. 英文采样：生成严格结构化 Markdown（带必备章节 / 标题 / feature 列表 / 原始链接）。
2. 结构校验：正则 + 章节清单校验 + 链接计数（避免翻译前就出现缺失）。
3. 翻译阶段（英文→中文）：
   - 逐段解析（Heading / 段落 / 列表 / 表格 / 链接 / 代码块 AST）。
   - 仅翻译可翻译节点（段落文本、列表项、表格单元格）。
   - 不翻译：Markdown 链接 URL、代码块、行内代码、纯英文专有名词白名单（Chromium, WebGPU, Service Worker 等）。
   - 应用术语表（glossary）做一致替换。
4. 产出：
   - 独立中文文件：`chrome-{version}-{channel}-zh.md`
   - （可选）组合双语文件：`chrome-{version}-{channel}-bilingual.md`（英文在前，中文紧随其后或并列对照）。
5. QA 校验：
   - Heading 层级/数量与英文一致。
   - 链接数量与顺序一致。
   - 特性条目计数一致。
   - 术语表命中率统计（覆盖率 < 阈值报警）。

### 14.3 翻译实现选项
| 方案 | 描述 | Pros | Cons | 场景 |
|------|------|------|------|------|
| 规则 + 小模型 (preferred) | 先 AST 切块，调用小/便宜模型逐段翻译 | 成本低，可缓存 | 复杂度中等 | 稳定批量生成 |
| 全文一次翻译 | 直接把英文全文丢给模型 | 简单 | 结构风险高，链接被改写风险 | 快速 PoC |
| 术语优先替换 + 统计 | 纯规则替换 + 机器翻译后校正 | 可审计 | 质量依赖词表覆盖 | 术语密集文档 |

推荐：AST 分段 + 小温度模型（temperature <=0.2）。

### 14.4 AST 与保护规则
解析后节点类型：Heading / Paragraph / List(Item) / Table(Row/Cell) / CodeBlock / InlineCode / Link / Emphasis。
保护策略：
- 链接节点：保留 `[text](url)` 中的 `url`；`text` 可翻译（若 text 是专有名词白名单则跳过）。
- 代码块 / 行内代码：完全跳过。
- 标题级别：原封不动，只翻译标题文本。
- 表格：逐 cell 翻译，保持竖线与对齐结构。

### 14.5 术语表 (glossary) 设计
文件：`config/term_glossary.yaml`
示例：
```yaml
terms:
  Service Worker: Service Worker
  WebGPU: WebGPU
  Origin Trial: 来源试用
  Deprecation: 弃用
  Feature Flag: 功能开关
```
使用顺序：翻译前先做不可翻译锁定（替换成占位符）→ 翻译 → 还原占位符 → 术语后处理统一。

### 14.6 校验脚本要点
Checkpoints：
1. heading_count(EN) == heading_count(ZH)
2. feature_item_count(EN)==feature_item_count(ZH)
3. links(md) URL 集合相等 & 顺序一致
4. 未出现裸露占位符 (e.g. GLOSS_TERM_*)
5. 术语覆盖率 >= 95%

### 14.7 伪代码示例
```python
def translate_markdown(en_md: str, glossary: dict) -> str:
	ast = parse_markdown(en_md)
	lock_terms(ast, glossary)
	out_nodes = []
	for node in ast:
		if node.type in TRANSLATABLE_TYPES:
			segs = split_inline_preserving_links(node)
			zh_parts = [llm_translate(s) for s in segs]
			out_nodes.append(rebuild(node, zh_parts))
		else:
			out_nodes.append(node)  # unchanged
	text = render(out_nodes)
	return restore_terms(text, glossary)
```

### 14.8 指标与收益估计
| 指标 | 当前 (估计) | 目标 (实施后) |
|------|-------------|---------------|
| LLM 采样调用数 (bilingual) | 2 | 1 |
| 失败概率 (assuming 8% 单次失败) | ~15.36% | 8% → 通过其他优化可降到 <5% |
| 平均 Token 成本 | 100% 基线 | ~55–65% (翻译段落更短) |
| 结构不一致事件 | 偶发 | 接近 0（结构复制） |

### 14.9 风险 & 缓解
| 风险 | 描述 | 缓解 |
|------|------|------|
| 翻译丢失 Markdown 语法 | 模型改写列表/表格 | AST 重建 + 单元测试 diff |
| 链接文本被误改 | 模型翻译导致语义偏差 | 保护 URL，必要时保持英文 anchor |
| 术语不一致 | 未命中词表 | 扩充词表 + 统计覆盖率 |
| 性能开销 | 多次分段调用 | 分段缓存 + 批量翻译接口 |
| 模型漂移 | 不同时间翻译风格差 | temperature=0.2 + 固定模型版本 |

### 14.10 最小实施步骤 (Incremental)
1. 实现英文采样结构校验函数 (regex + 清单)。
2. Markdown → AST 解析（可用 `markdown-it-py` 或现有轻量 parser；若不新增依赖，可写简化 parser）。
3. 术语表 YAML 读取 + 占位符锁定流程。
4. 分段翻译 (先用同 `ctx.sample` 小模型；后续可抽象为 `ctx.translate`).
5. 校验 + 报告（JSON 输出对比指标）。
6. 集成到当前工具：`language=bilingual` 时走新路径，保留旧路径为 fallback（受 feature flag 控制）。
7. 监控：记录 per-run metrics (duration, token_estimates, glossary_coverage)。

### 14.11 Feature Flag 建议
环境变量：`WEBPLATFORM_SINGLE_PASS=1` 启用；缺省保持现状，便于灰度对比。

### 14.12 后续扩展
- 术语表自动扩展：统计高频未翻译英文短语，人工确认后入库。
- 机器翻译质量评分：随机采样段落通过第二模型做逆向回译计算 BLEU/ChrF 近似指标。
- 多区域 (target_area) 时支持并行翻译批处理。

### 14.13 与 Enterprise 模式对齐点
| 维度 | Enterprise | 改造后 WebPlatform |
|------|------------|--------------------|
| 主采样次数 | 1 | 1 |
| 结构锚点 | Prompt 强约束 | EN 结构 + 校验锁定 |
| 多语言策略 | 内嵌双语（中内容+英标题） | 二次翻译派生 ZH |
| 回退策略 | 明确 success=False | 同步采用 JSON 结构 |

更新：实施前不改现有代码，仅作为设计定稿参考。

---
## 15. MCP Server 分层 Prompt 资源化方案（结构模版 + 指令模版）
目标：将“结构不变 / 策略可迭代”与“单次英文采样”结合，降低漂移、方便灰度 & 回滚。

### 15.1 分层概念
| 层 | 文件示例 | 职责 | 更新频率 | 版本控制 |
|----|----------|------|----------|----------|
| 结构层 (Structure) | `structure-schema-v1.md` | 固定章节/锚点/Feature 模板/meta block 占位符 | 低 | schema_version 递增 |
| 指令层 (Instructions/Policy) | `instructions-policy-v1.md` | 影响判定、截断、风险分类、错误条件 | 中 | policy_version 递增 |
| 数据层 (Runtime YAML) | 运行期注入 | 特性/链接原始数据 | 高 | 不版本化（依版本号缓存） |

### 15.2 结构模版核心要素
```
SCHEMA_VERSION: 1
```meta
version: {{VERSION}}
channel: {{CHANNEL}}
area: {{AREA_OR_GLOBAL}}
feature_count_input: {{FEATURE_COUNT}}
feature_count_included: <TO_FILL>
truncated: <TO_FILL true|false>
schema_version: 1
```
<!-- SECTION:EXEC_SUMMARY -->
### 1. Executive Summary
<!-- END:EXEC_SUMMARY -->
...（依次列出所有章节锚点）...
<!-- FEATURES_START -->
{{FEATURE_BLOCK}}
<!-- FEATURES_END -->
```
Feature 单条模板只保留标签行/占位说明，不含策略文本。

### 15.3 指令模版要素
- Impact 判定规则（基于 primary_tags / risk keywords）
- 截断策略 ( >N 时优先级排序 & 记录 truncated: true )
- 链接保持与顺序约束（禁止新增/改写）
- 错误触发条件（缺 meta 字段、缺章节锚点、link 数不匹配）
- 术语保留列表（仅列名，不解释）
- 输出失败格式：`ERROR: STRUCTURE_VALIDATION_FAILED`

### 15.4 运行期拼装流程
1. 读取资源：`structure = ctx.read_resource("webplatform-structure@v1")`
2. 读取指令：`policy = ctx.read_resource("webplatform-instructions@v1")`
3. 占位替换（VERSION / CHANNEL / AREA / FEATURE_COUNT）
4. 构造最终 user message:
```
{policy}\n\nDATA:\n```yaml\n{yaml_data}\n```\n\nSTRUCTURE_SKELETON:\n{structure_filled}
```
5. system_prompt 极简：强调“只填充结构 / 校验失败输出错误码”

### 15.5 校验器 (Validator) 规则
| 规则 | 描述 | 失败处理 |
|------|------|----------|
| meta 完整性 | 所有关键键存在且 schema_version 匹配 | 标记失败 |
| 锚点唯一性 | 每个 SECTION 注释出现 1 次 | 失败 |
| feature_count_included 合理 | 1 ≤ included ≤ input | 失败 |
| LINKS 匹配 | 每特性 REFERENCES 数量 == YAML links 数量且顺序一致 | 失败 |
| Error 码检测 | 若输出错误码且无额外文本则直接返回 | 透传 |

### 15.6 版本升级策略
- 新结构文件 `structure-schema-v2.md` 引入时：
	* schema_version=2；老版本 v1 保留
	* 采样请求参数附带 `desired_schema=2`；失败可降级一次
- 指令层独立升级：`instructions-policy-v2.md`，不改结构层

### 15.7 渐进式灰度
| 阶段 | 范围 | 行为 |
|------|------|------|
| Phase 0 | 内部版本 (单 area) | 采样后仅日志校验，不写新文件 |
| Phase 1 | 全 area 英文 | 校验通过写入 `-en.md`，失败回退旧 Prompt 路径 |
| Phase 2 | 启用单次英文 + 翻译 | 中文使用翻译流水线；旧双采样保留 feature flag |
| Phase 3 | 全量切换 | 移除旧路径 & fallback |

### 15.8 风险 & 规避
- 结构文件变更破坏兼容 → 引入 schema_version + 双文件保留
- 模型忽略锚点注释 → 使用更醒目的标签 (`#==SECTION:...` 或 HTML 注释双轨冗余)
- 长度截断导致尾部锚点缺失 → 先前置 meta + 章节，再输出特性列表，限制特性总数
- Error 码被模型“解释” → system_prompt 明确“不得添加解释文本”

### 15.9 最小实现清单
1. 新增：`prompts/webplatform-prompts/structure-schema-v1.md`
2. 新增：`prompts/webplatform-prompts/instructions-policy-v1.md`
3. Server 注册两个 resource 名称
4. 采样调用前拼装替换 (不改现有 Prompt 路径；通过 flag 启用)
5. 实现基础 validator（正则 + 计数）日志输出
6. 对比旧输出差异（feature_count / 章节完整度）

### 15.10 预期收益对照
| 指标 | 现状 | 目标 (分层后) |
|------|------|---------------|
| 结构漂移率 | 偶发缺章节 | ≈ 0 |
| 模版修改频率影响面 | 改一次全量重测 | 结构稳定，策略热更 |
| 回滚成本 | 高 (需替换大 Prompt) | 低 (切换 resource 版本) |
| 校验实现复杂度 | 混杂结构+策略 | 简化：结构固定正则即可 |

### 15.11 与翻译流水线衔接
翻译阶段可直接识别并跳过：meta fenced block、SECTION 注释、FEATURES_START/END；按锚点拆分段落，保证中英文对齐。

### 15.12 下一步动作建议
- [ ] 起草结构 v1 文件草案
- [ ] 起草指令 v1 文件草案（引用现有 webplatform-prompt-en 中策略语句）
- [ ] 编写 validator 伪代码 & 单元测试框架占位
- [ ] 增加 feature flag：`WEBPLATFORM_PROMPT_LAYERED=1`

（以上方案已整合进分析，后续可在 TODO 区域跟踪执行。）
```

---

## TODO（在此副本增量讨论，不回写原文档前一律保持独立）
- [ ] 起草 v2 Prompt 初稿骨架
- [ ] 定义 meta block 字段最终列表
- [ ] 设计正则校验脚本规范
- [ ] 术语表首批条目与格式约定

