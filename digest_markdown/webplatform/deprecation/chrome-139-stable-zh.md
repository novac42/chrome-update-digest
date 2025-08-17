---
layout: default
title: Chrome 139 弃用更新摘要
---

````markdown
保存至: digest_markdown/webplatform/deprecation/chrome-139-stable-zh.md

---

# Chrome 139 弃用更新摘要

## 1. 执行摘要

Chrome 139 引入了多项重要弃用，影响 Web 平台的兼容性与安全性。最显著的变化包括移除传统的 `Purpose: prefetch` 头部，推荐使用 `Sec-Purpose` 头部，停止支持 macOS 11，以及不再自动检测 HTML 中的 `ISO-2022-JP` 字符集。这些更新旨在简化浏览器行为、提升安全性，并推动迁移到现代标准。

## 2. 主要影响

### 技术影响

- **现有实现**：依赖已弃用的 `Purpose: prefetch` 头部或 `ISO-2022-JP` 字符集自动检测的网站可能会遇到兼容性问题。Chrome 将不再在 macOS 11 上获得更新，用户可能因此面临安全风险。
- **新能力**：切换到 `Sec-Purpose` 头部使 Chrome 与现代导航推测标准保持一致，提升互操作性和安全性。
- **技术债务**：继续依赖弃用特性会增加维护负担和安全风险。为避免未来出现破坏性更改，需尽快迁移。

## 3. 风险评估

**关键风险**：
- **破坏性更改**：停止支持 macOS 11 及 `ISO-2022-JP` 字符集自动检测，可能导致旧有工作流或内容失效。
- **安全考量**：移除不安全的字符集自动检测可解决已知漏洞。

**中等风险**：
- **弃用**：从 `Purpose: prefetch` 迁移到 `Sec-Purpose` 可能需要后端和基础设施的更新。
- **性能影响**：影响较小，但头部或字符集处理不当可能降低用户体验。

## 4. 推荐措施

### 立即行动

- 检查代码库中是否使用 `Purpose: prefetch` 头部，并更新为 `Sec-Purpose`。
- 识别对 `ISO-2022-JP` 字符集自动检测的依赖，并迁移到显式字符集声明。
- 通知 macOS 11 用户停止支持，并建议升级操作系统。

### 短期规划

- 更新文档和开发者指南，反映相关弃用内容。
- 监控用户反馈，关注相关变更引发的问题。
- 针对头部变更，规划分阶段发布或特性标记，以减少影响。

### 长期策略

- 建立流程，及早发现即将弃用的特性。
- 鼓励采用现代 Web 标准并主动迁移。
- 定期审查平台支持政策，降低技术债务。

## 5. 特性分析

### Stop sending Purpose: prefetch header from prefetches and prerenders（停止在预取和预渲染中发送 Purpose: prefetch 头部）

**影响级别**：🟡 重要

**变更内容**：
Chrome 将不再为预取和预渲染请求发送传统的 `Purpose: prefetch` 头部，而是使用现代的 `Sec-Purpose` 头部。此变更受特性标记/紧急开关控制，以在发布过程中缓解兼容性问题。

**重要性说明**：
此举使 Chrome 与当前导航推测标准保持一致，减少传统头部的使用，并提升与其他浏览器及服务的安全性和互操作性。

**实施建议**：
- 更新服务器端逻辑，识别并处理 `Sec-Purpose` 头部，替代 `Purpose: prefetch`。
- 测试预取和预渲染流程，确保兼容性。
- 在过渡期间监控是否有异常行为。

**参考资料**：
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

---

### Remove support for macOS 11（移除对 macOS 11 的支持）

**影响级别**：🔴 严重

**变更内容**：
Chrome 138 是最后一个支持 macOS 11 的版本。从 Chrome 139 起，不再支持 macOS 11。Chrome 在 macOS 11 上仍可运行，但不会获得更新，用户将看到警告信息栏。

**重要性说明**：
使用不受支持操作系统版本的用户将无法获得安全或功能更新，面临更高的漏洞和兼容性风险。

**实施建议**：
- 向用户和相关方告知 macOS 11 停止支持的信息。
- 鼓励并协助用户升级到受支持的 macOS 版本。
- 相应更新内部文档和支持材料。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

---

### Remove auto-detection of `ISO-2022-JP` charset in HTML（移除 HTML 中 `ISO-2022-JP` 字符集的自动检测）

**影响级别**：🟡 重要

**变更内容**：
Chrome 139 移除了对 HTML 文档中 `ISO-2022-JP` 字符集自动检测的支持，原因是存在已知安全问题且使用率低。现在必须使用显式字符集声明。

**重要性说明**：
此变更缓解了与字符集自动检测相关的安全漏洞，并使 Chrome 与不支持该特性的 Safari 保持一致。

**实施建议**：
- 检查并更新依赖 `ISO-2022-JP` 自动检测的网页内容，改为使用显式字符集声明（如 `<meta charset="ISO-2022-JP">`）。
- 测试受影响页面，确保正确渲染和编码。
- 向内容作者和本地化团队传达相关变更。

**参考资料**：
- [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/)
- [Tracking bug #40089450](https://issues.chromium.org/issues/40089450)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

---
````