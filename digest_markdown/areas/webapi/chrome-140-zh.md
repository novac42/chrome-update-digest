---
layout: default
title: Chrome 140 Web API Updates
---

# Chrome 140 Web API Updates

## Area Summary

Chrome 140 为 Web API 领域带来了重要增强，通过三项关键更新加强了数据流处理、应用程序集成和安全机制。此版本通过新的 `ReadableStreamBYOBReader` `min` 选项引入了对可读流的精细控制，将 Get Installed Related Apps API 扩展到桌面平台以实现更好的跨平台应用发现，并实现了 HTTP cookie 前缀以通过区分服务器设置和客户端设置的 cookies 来增强安全性。这些更新共同推进了 Web 平台在性能优化、应用生态系统集成和安全强化方面的能力。

## Detailed Updates

这些 Web API 改进专注于增强开发者对数据流的控制、扩展平台能力以及加强 Web 应用程序的安全基础。

### `ReadableStreamBYOBReader` `min` option

#### What's New
`ReadableStreamBYOBReader.read(view)` 方法现在接受一个 `min` 选项，可以保证在读取操作解析之前写入最少数量的元素。

#### Technical Details
此前，`ReadableStreamBYOBReader.read()` 方法会将数据读取到 `ArrayBufferView` 中，但无法控制在解析之前写入多少元素。新的 `min` 参数允许开发者指定他们希望在单次读取操作中接收的最少数据量，提供对缓冲区管理的更好控制，并减少大数据传输所需的读取调用次数。

#### Use Cases
此增强对于处理分块流数据的应用程序特别有价值，例如媒体播放器、文件处理器或需要特定缓冲区大小的网络协议。开发者现在可以通过确保每次读取操作接收足够的数据量来优化其流实现，减少开销并提高性能。

#### References
- [Tracking bug #40942083](https://issues.chromium.org/issues/40942083)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6396991665602560)
- [Spec](https://streams.spec.whatwg.org/#byob-reader-read)

### Get Installed Related Apps API on desktop

#### What's New
Get Installed Related Apps API (`navigator.getInstalledRelatedApps`) 现在在桌面平台上可用，允许网站检测其对应的应用程序是否已安装在用户系统上。

#### Technical Details
该 API 最初在 Chrome 80 中面向移动平台推出，使网站能够查询已与 Web 来源建立关联的相关应用程序。该 API 维持严格的安全要求，只有当应用程序通过清单文件或特定平台机制正确声明其与网站的关系时才允许访问。

#### Use Cases
桌面支持为 Web 和原生应用程序之间的无缝用户体验开辟了新的可能性。网站现在可以提供上下文相关的应用下载提示、提供到已安装应用程序的深度链接，或根据可用的原生对应物调整其界面。这对于提供 Web 和桌面体验的生产力应用、通信工具和内容平台特别有用。

#### References
- [Tracking bug #895854](https://issues.chromium.org/issues/895854)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5695378309513216)
- [Spec](https://wicg.github.io/get-installed-related-apps/spec)

### Http cookie prefix

#### What's New
Chrome 140 引入了 HTTP cookie 前缀，允许服务器区分由服务器设置的 cookies 与由客户端代码设置的 cookies，从而增强对各种攻击向量的安全防护。

#### Technical Details
此安全功能实现了一种机制，用特定前缀标记 cookies 以指示其来源。该实现有助于防止恶意代码（如 XSS 漏洞利用、浏览器扩展或受损脚本）设置可能与合法服务器设置的 cookies 混淆的 cookies。这种区分对于维护身份验证和会话管理系统的完整性至关重要。

#### Use Cases
cookie 前缀功能对于具有严格安全要求的应用程序至关重要，特别是那些处理敏感数据或身份验证流程的应用程序。它有助于防止恶意脚本尝试伪造服务器 cookies 的攻击，并为服务器提供验证 cookie 真实性的可靠方法。这对于金融服务、企业应用程序以及任何 cookie 完整性对安全性至关重要的系统特别有价值。

#### References
- [Tracking bug #426096760](https://issues.chromium.org/issues/426096760)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5170139586363392)
- [Spec](https://github.com/httpwg/http-extensions/pull/3110)
