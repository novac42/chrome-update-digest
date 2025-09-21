# Chrome 140 Web API 发布分析

## 摘要

Chrome 140 引入了三项重要的 Web API 增强功能，专注于流媒体能力、跨平台应用集成和 Cookie 安全性。最值得注意的新增功能包括：通过最小读取保证改进字节流读取、扩展 Get Installed Related Apps API 的桌面支持，以及通过前缀机制增强 HTTP Cookie 安全性。

## 功能详情

### `ReadableStreamBYOBReader` `min` 选项

**更改内容**：
此增强功能为 `ReadableStreamBYOBReader.read(view)` 方法添加了 `min` 选项，解决了当前 Streams API 中的一个关键限制。以前，虽然该方法接受 `ArrayBufferView` 来读取数据，但无法保证在读取操作解决之前会写入多少元素。新的 `min` 参数允许开发者指定在 promise 解决之前必须读取的最小字节数，提供更可预测和高效的流式行为。这对于需要在处理前确保足够数据可用性的应用程序特别有价值，例如媒体流、文件处理或网络协议实现。

**参考资料**：
- [Tracking bug #40942083](https://issues.chromium.org/issues/40942083)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6396991665602560)
- [Spec](https://streams.spec.whatwg.org/#byob-reader-read)

### 桌面端 Get Installed Related Apps API

**更改内容**：
Get Installed Related Apps API (`navigator.getInstalledRelatedApps`) 将其可用性扩展到桌面平台，基于其在 Chrome 80 中的初始发布。此 API 使网站能够检测其对应的原生应用程序是否安装在用户设备上，但仅当 Web 源和应用程序之间存在已建立的关联时才可用。桌面扩展显著拓宽了 API 的实用性，允许 Web 应用程序在不同平台上提供无缝集成体验。这支持了诸如在可用时提示用户在原生应用中打开内容、提供应用特定功能，或在未检测到相关应用时提供安装建议等场景。

**参考资料**：
- [Tracking bug #895854](https://issues.chromium.org/issues/895854)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5695378309513216)
- [Spec](https://wicg.github.io/get-installed-related-apps/spec)

### HTTP Cookie 前缀

**更改内容**：
此安全增强功能引入了 HTTP Cookie 前缀，帮助服务器区分由服务器设置的 Cookie 与由客户端代码设置的 Cookie。这种区分对于安全敏感场景至关重要，在这些场景中 Cookie 通常由服务器控制，但可能通过 XSS 漏洞、恶意浏览器扩展或开发者错误而受到攻击。前缀机制提供了一种标准化方式来标记 Cookie 的来源，使服务器能够验证 Cookie 真实性并实施更强大的安全策略。此功能通过在可信的服务器设置 Cookie 和潜在不可信的客户端设置 Cookie 之间提供明确分离，加强了 Web 应用程序安全性。

**参考资料**：
- [Tracking bug #426096760](https://issues.chromium.org/issues/426096760)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5170139586363392)
- [Spec](https://github.com/httpwg/http-extensions/pull/3110)