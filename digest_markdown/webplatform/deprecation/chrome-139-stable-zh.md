## Area Summary

Chrome 139 的弃用工作集中于移除带来安全、兼容性或维护成本的旧行为和平台支持。主要主题包括淘汰遗留请求头（prefetch Purpose）、终止对旧版 macOS（11）的支持，以及移除存在风险的字符集自动检测（ISO-2022-JP）。对开发者影响最大的变化是推测性预取/预渲染行为可能出现差异、旧版 macOS 上无法接收更新，以及更严格的编码处理会暴露声明不正确的页面。这些更改通过减少攻击面、简化实现不变式并鼓励开发者显式控制编码和平台支持来推动 Web 平台的发展。

## Detailed Updates

The following entries expand on the summary above and provide technical and practical guidance for development teams.

### Stop sending Purpose: prefetch header from prefetches and prerenders (停止在 prefetch 和 prerender 中发送 Purpose: prefetch 请求头)

#### What's New
Chrome 正在移除用于 prefetch 和 prerender 的遗留请求头 `Purpose: prefetch`；这些请求将改用 `Sec-Purpose` 头。

#### Technical Details
遗留请求头的移除将通过功能标志/开关（feature flag/kill switch）来控制，以避免兼容性问题。此更改的范围限定在按 nav-speculation 与 fetch 交互的推测性导航功能（prefetch 和 prerender）。

#### Use Cases
- 确保依赖 `Purpose: prefetch` 的服务器端逻辑改为读取 `Sec-Purpose`。
- 更新检查请求头以识别 prefetch/prerender 信号的分析或访问控制规则。
- 利用此更改通过统一使用 `Sec-Purpose` 来简化头处理。

#### References
- [Tracking bug #420724819](https://issues.chromium.org/issues/420724819)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320)
- [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

### Remove support for macOS 11 (移除对 macOS 11 的支持)

#### What's New
Chrome 139 放弃对 macOS 11 的支持。Chrome 138 是最后一个支持该操作系统的版本。

#### Technical Details
在 macOS 11 设备上，Chrome 将继续可运行，但会显示警告信息栏并不再接收更新。用户必须升级其操作系统以接收新的 Chrome 版本。

#### Use Cases
- 规划测试与支持基线：CI 与 QA 应将 macOS 测试运行器迁移到受支持的 macOS 版本。
- 向用户和运维团队传达为继续接收 Chrome 更新所需的操作系统升级信息。
- 考虑将自动更新和企业管理工作流定位到受支持的 macOS 版本。

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

### Remove auto-detection of `ISO-2022-JP` charset in HTML (移除 HTML 中对 `ISO-2022-JP` 字符集的自动检测)

#### What's New
Chrome 139 移除了对 HTML 中 `ISO-2022-JP` 字符集的自动检测支持，原因是已知的安全问题且使用率极低。

#### Technical Details
对 `ISO-2022-JP` 的自动检测已被移除；页面必须显式声明其编码。该决定与其他浏览器一致（Safari 不支持此自动检测），并能缓解安全分析中描述的风险。

#### Use Cases
- 审计依赖字符集自动检测的页面，确保显式声明字符集（通过 `Content-Type` header 或 <meta charset>）。
- 对于使用 `ISO-2022-JP` 的遗留内容，将文件转换为 UTF-8 或提供显式的字符集头。
- 更新服务器和构建管线以强制正确的字符集元数据，避免错误解释。

#### References
- [known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/)
- [Tracking bug #40089450](https://issues.chromium.org/issues/40089450)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)