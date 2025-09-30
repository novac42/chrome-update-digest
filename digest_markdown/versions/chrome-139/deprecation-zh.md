---
layout: default
title: deprecation-zh
---

## 领域摘要

Chrome 139 专注于移除遗留行为和攻击面：遗留请求头、旧操作系统支持以及有风险的字符集自动检测将被弃用。对开发者影响最大的更改包括移除遗留的 `Purpose: prefetch` 标头（服务器必须依赖 `Sec-Purpose`）、停止在 macOS 11 上的更新，以及因安全问题移除 `ISO-2022-JP` 的自动检测。这些弃用简化了平台，使行为与现代规范一致，并降低安全和兼容性负担。团队应审计服务器端的标头处理、更新 macOS 测试环境，并验证对遗留内容的编码处理。

## 详细更新

Below are concise, developer-focused descriptions of each deprecation listed above and what teams should consider when preparing for Chrome 139.

### Stop sending Purpose: prefetch header from prefetches and prerenders（停止在预取和预渲染中发送 Purpose: prefetch 标头）

#### 新增内容
Chrome 将停止为预取和预渲染发送遗留的 `Purpose: prefetch` 标头；此类请求现在使用 `Sec-Purpose` 标头。该移除操作将通过功能开关/终止开关控制，以避免广泛的兼容性中断。

#### 技术细节
平台已采用 `Sec-Purpose` 标头作为预取/预渲染意图的标准化信号。仍解析 `Purpose: prefetch` 的实现应迁移以识别 `Sec-Purpose`。此更改已在 nav-speculation prerendering 规范中进行跟踪与协调，以确保行为一致。

#### 适用场景
- 服务器端请求处理、分析和缓存层应更新为读取 `Sec-Purpose`。
- 基于 `Purpose` 分支逻辑的广告平台或中间件应在该标头被关停前添加对 `Sec-Purpose` 的支持。
- QA 应根据规范验证推测性导航和预取流程。

#### 参考资料
- https://issues.chromium.org/issues/420724819
- https://chromestatus.com/feature/5088012836536320
- https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch

### Remove support for macOS 11（移除对 macOS 11 的支持）

#### 新增内容
Chrome 138 是最后一个支持 macOS 11 的版本；从 Chrome 139 开始，Chrome 将不再在 macOS 11 上提供更新。

#### 技术细节
在运行 macOS 11 的系统上，Chrome 仍可运行，但会显示警告信息条并且不会收到后续更新。用户必须将 macOS 升级到受支持的版本以继续接收 Chrome 更新。

#### 适用场景
- IT 管理员必须为受管设备规划操作系统升级，以继续接收 Chrome 更新。
- 开发者和 QA 应停止在持续浏览器测试中依赖 macOS 11；将测试覆盖迁移到受支持的 macOS 版本。

#### 参考资料
- https://chromestatus.com/feature/4504090090143744

### Remove auto-detection of `ISO-2022-JP` charset in HTML（在 HTML 中移除对 `ISO-2022-JP` 字符集的自动检测）

#### 新增内容
由于已知的安全问题和低使用率，Chrome 139 在 HTML 中移除了对 `ISO-2022-JP` 字符集的自动检测；Safari 也不支持此类自动检测。

#### 技术细节
为了缓解编码差异导致的安全风险，已放弃对 `ISO-2022-JP` 的自动检测。依赖隐式检测的网站必须显式声明其字符集以确保正确渲染。对此移除的跟踪与协调记录在项目问题和平台状态条目中。

#### 适用场景
- Web 开发者应确保使用 `ISO-2022-JP` 的页面显式声明字符集（例如，通过 <meta charset> 或 HTTP 头）。
- 安全团队应注意这会减少基于编码的攻击向量。
- 兼容性测试应在没有自动检测的情况下验证遗留日文编码内容的行为。

#### 参考资料
- https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/
- https://issues.chromium.org/issues/40089450
- https://chromestatus.com/feature/6576566521561088
- https://creativecommons.org/licenses/by/4.0/
- https://www.apache.org/licenses/LICENSE-2.0
- https://developers.google.com/site-policies

文件已保存至： digest_markdown/webplatform/deprecation/chrome-139-stable-en.md
