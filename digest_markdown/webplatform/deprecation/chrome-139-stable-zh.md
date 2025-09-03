````markdown
digest_markdown/webplatform/deprecation/chrome-139-stable-zh.md
---

# Chrome 更新分析器 – 弃用领域摘要

## Chrome 139（稳定版）– 弃用

---

### 1. 执行摘要

Chrome 139 推出了多项重要弃用，影响 Web 平台的兼容性和安全性。主要变更包括移除旧版 `Purpose: prefetch` 请求头，推荐使用标准化的 `Sec-Purpose` 请求头，停止对 macOS 11 的支持，以及在 HTML 中不再自动检测 `ISO-2022-JP` 字符集。这些更新旨在简化浏览器行为、提升安全性并减少技术债务。

---

### 2. 主要影响

#### 技术影响

- **请求头变更**：预取和预渲染请求将不再发送旧版 `Purpose: prefetch` 请求头，仅依赖 `Sec-Purpose` 请求头。这可能影响依赖旧请求头的服务器端逻辑。
- **平台支持**：Chrome 将不再在 macOS 11 上更新，用户需升级操作系统以继续获得浏览器更新。
- **字符集检测**：移除对 `ISO-2022-JP` 的自动检测，减少攻击面，但可能影响依赖此编码的旧内容。

#### 新能力

- 与 Web 标准更好地对齐（Sec-Purpose 请求头）。
- 通过移除高风险字符集自动检测，提升安全性。

#### 技术债务考量

- 依赖已弃用请求头或字符集检测的旧代码需重构。
- 基础设施需更新，仅支持当前受支持的操作系统版本。

---

### 3. 风险评估

**关键风险：**

- **破坏性更改**：移除 `Purpose: prefetch` 请求头和字符集自动检测可能导致集成或旧内容出现问题。
- **安全考量**：字符集变更解决已知漏洞，降低用户风险。

**中等风险：**

- **弃用**：停止支持 macOS 11 可能导致部分用户停留在过时且不安全的浏览器版本。
- **性能影响**：影响较小，但服务器端逻辑可能需更新以避免不必要的处理。

---

### 4. 推荐措施

#### 立即行动

- 检查服务器逻辑是否依赖 `Purpose: prefetch` 请求头，并迁移至 `Sec-Purpose`。
- 通知 macOS 11 用户停止支持，并建议升级操作系统。
- 检查任何依赖 `ISO-2022-JP` 自动检测的内容或系统。

#### 短期规划

- 更新文档和开发者指南，反映请求头和字符集变更。
- 监控用户反馈和错误日志，关注相关弃用问题。

#### 长期策略

- 持续跟踪浏览器弃用，主动重构旧代码。
- 在部署策略中规划操作系统支持生命周期。

---

### 5. 功能分析

---

### Stop sending Purpose: prefetch header from prefetches and prerenders（停止在预取和预渲染中发送 Purpose: prefetch 请求头）

**影响级别**：🔴 关键

**变更内容**：
Chrome 将停止在预取和预渲染请求中发送旧版 `Purpose: prefetch` 请求头，全面转向标准化的 `Sec-Purpose` 请求头。此变更通过功能标志/紧急开关控制，以缓解兼容性问题。

**重要性说明**：
此弃用使 Chrome 与现代 Web 标准保持一致，减少请求处理中的歧义。依赖旧请求头的服务器端逻辑可能失效，需及时更新。

**实施建议**：
- 更新服务器逻辑，检测并处理 `Sec-Purpose` 请求头，替代 `Purpose: prefetch`。
- 测试预取和预渲染流程，确保兼容性。
- 监控是否出现回退或异常行为。

**参考资料**：
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

---

### Remove support for macOS 11（移除对 macOS 11 的支持）

**影响级别**：🟡 重要

**变更内容**：
Chrome 139 不再支持 macOS 11。该系统上的用户将无法获得后续更新，并会看到警告信息栏。升级 Chrome 需先升级至受支持的 macOS 版本。

**重要性说明**：
确保 Chrome 用户能够获得最新的安全和功能更新。组织需规划操作系统升级，以维持浏览器支持。

**实施建议**：
- 向受影响用户和相关方传达此变更。
- 更新部署和支持文档。
- 鼓励迁移至受支持的 macOS 版本。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

---

### Remove auto-detection of `ISO-2022-JP` charset in HTML（移除 HTML 中对 ISO-2022-JP 字符集的自动检测）

**影响级别**：🔴 关键

**变更内容**：
由于已知安全问题和使用率低，Chrome 不再在 HTML 文档中自动检测 `ISO-2022-JP` 字符集。此举与 Safari 保持一致，Safari 也不支持该自动检测。

**重要性说明**：
解决与字符集自动检测相关的安全漏洞，降低用户和开发者风险。可能影响依赖该编码的旧内容。

**实施建议**：
- 检查并更新任何依赖 `ISO-2022-JP` 自动检测的旧内容或系统。
- 在 HTML 文档中明确指定字符集（charset）参数。
- 更新后关注编码相关问题。

**参考资料**：
- [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/)
- [Tracking bug #40089450](https://issues.chromium.org/issues/40089450)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

---

**摘要结束**
````