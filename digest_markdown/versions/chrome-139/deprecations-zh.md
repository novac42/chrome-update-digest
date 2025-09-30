---
layout: default
title: deprecations-zh
---

### 1. 领域摘要

Chrome 139 的弃用侧重于通过移除遗留行为和旧平台支持来强化安全性并现代化平台行为。关键更改包括移除遗留的 fetch 标头（Purpose: prefetch）、放弃对 macOS 11 的支持，以及取消对 `ISO-2022-JP` 字符集的自动检测。这些更改减少了攻击面和兼容性复杂性，鼓励使用标准化的标头和现代操作系统版本，并使 Chrome 与其他浏览器的更安全默认设置保持一致。开发者应计划对标头检测进行迁移，更新针对性的 macOS 支持矩阵，并确保正确声明字符集。

## 详细更新

下面列出 Chrome 139 引入的弃用，与上文摘要相对应，包含简洁的技术说明和后续链接。

### Stop sending Purpose: prefetch header from prefetches and prerenders（停止在预取和预渲染请求中发送 Purpose: prefetch 标头）

#### 新增内容
Chrome 将停止在 prefetch 和 prerender 请求中发送遗留的 Purpose: prefetch 标头；这些投机性请求将改用 Sec-Purpose。为了缓解兼容性回归，移除受一个功能标志/回退开关控制。

#### 技术细节
- 该更改将投机性 fetch 的信号迁移到 Sec-Purpose 标头。
- 推送受功能标志/回退开关保护，以便在出现兼容性问题时回滚。
- 依赖 Purpose: prefetch 的开发者应观察 Sec-Purpose 的语义并更新服务器端逻辑。

#### 适用场景
- 以前检查 Purpose: prefetch 的服务器端分析或路由逻辑必须迁移到 Sec-Purpose。
- 提高清晰度以便处理 prerender/prefetch 的抓取意图，并与导航投机规范对齐。

#### 参考资料
- https://issues.chromium.org/issues/420724819
- https://chromestatus.com/feature/5088012836536320
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch

### Remove support for macOS 11（移除对 macOS 11 的支持）

#### 新增内容
Chrome 138 是最后一个支持 macOS 11 的版本；从 Chrome 139 开始，不再支持 macOS 11。Chrome 仍将在 macOS 11 上运行，但会显示警告信息条并且不再接收后续更新。

#### 技术细节
- 保留在 macOS 11 的系统将不会在稳定通道收到 Chrome 更新；用户必须升级 macOS 才能继续接收 Chrome 更新。
- 此更改减少对较旧操作系统版本的测试和维护负担。

#### 适用场景
- 更新项目兼容性矩阵和最低支持的 macOS 版本说明。
- 在 macOS 上运行浏览器测试的 CI 与自动化应切换到受支持的 macOS 版本，以继续接收 Chrome 更新。

#### 参考资料
- https://chromestatus.com/feature/4504090090143744

### Remove auto-detection of `ISO-2022-JP` charset in HTML（移除在 HTML 中对 `ISO-2022-JP` 字符集的自动检测）

#### 新增内容
由于已知的安全问题和极低的使用率，Chrome 139 取消了对 HTML 中 `ISO-2022-JP` 字符集的自动检测；Safari 已经不支持此类自动检测。

#### 技术细节
- 禁用对 `ISO-2022-JP` 的自动检测以缓解基于编码的安全差异。
- 依赖自动检测的页面必须通过正确的 Content-Type 标头或 meta charset 声明显式指定字符编码。

#### 适用场景
- 审计旧的日文内容页面，确保通过 meta charset 或 HTTP 标头显式声明字符集，以避免渲染回归。
- 对安全敏感的应用，应优先使用显式编码以消除歧义。

#### 参考资料
- https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/
- https://issues.chromium.org/issues/40089450
- https://chromestatus.com/feature/6576566521561088
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies
