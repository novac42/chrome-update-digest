---
layout: default
title: chrome-140-zh
---

## 领域摘要

Chrome 140 的 Web API 更新侧重于提高健壮性、本地集成和服务器端完整性。关键更改允许开发者控制流读取保证、从网页检测相关桌面应用，以及区分由服务器设置的 cookie 以用于安全敏感的工作流。这些更新通过收紧 I/O 语义、扩展桌面上的网页到原生发现以及强化 cookie 归属来推进平台，以缓解客户端篡改。它们共同减少数据处理中的歧义，使安装感知体验更丰富，并强化服务器端的信任边界。

## 详细更新

下面的条目扩展了上述摘要，并描述了 Chrome 140 中每个 Web API 功能对开发者的影响和技术说明。

### `ReadableStreamBYOBReader` `min` option（添加 min 选项）

#### 新增内容
向 `ReadableStreamBYOBReader.read(view)` 添加了一个 `min` 选项，使调用者可以在读取解析之前请求在提供的 `ArrayBufferView` 中写入至少指定数量的元素。

#### 技术细节
此更改扩展了 Streams 规范中定义的 BYOB 读取语义，以在现有的 view 缓冲区之外接受一个 `min` 约束。读取的 promise 现在仅在至少有 `min` 个元素可用时才会解析（受流结束/错误条件约束），从而减少部分读取的不确定性。权威行为见 WHATWG streams 规范。

#### 适用场景
- 在确定性的二进制协议解析中，要求在处理之前获得最小帧大小。  
- 通过确保更大、可用的读取来减少应用层的缓冲和重试。  
- 对偏好完整记录而非增量片段的流式解析器提高性能。

#### 参考资料
- [跟踪 bug #40942083](https://issues.chromium.org/issues/40942083)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6396991665602560)
- [规范](https://streams.spec.whatwg.org/#byob-reader-read)

### Get Installed Related Apps API on desktop（桌面端可用）

#### 新增内容
Get Installed Related Apps API（`navigator.getInstalledRelatedApps`）在桌面端可用，允许站点检查与该来源关联的本机应用是否已安装。

#### 技术细节
该 API 仅在本机应用与 Web 来源之间已建立关联（链接必须经过验证）时返回信息。此桌面端推出扩展了现有能力（之前主要面向移动端），并保持关联检查作为隐私保护发现的门槛。历史背景：该 API 最初在 Chrome 80 推出。

#### 适用场景
- 仅在匹配的桌面应用存在时提供深度链接或“在应用中打开”提示。  
- 通过在检测到配套应用时定制 UI 来改进安装参与流程。  
- 为 PWAs 和跨桌面平台的可安装体验提供渐进式增强。

#### 参考资料
- [跟踪 bug #895854](https://issues.chromium.org/issues/895854)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5695378309513216)
- [规范](https://wicg.github.io/get-installed-related-apps/spec)

### Http cookie prefix（服务器端 cookie 归属语义）

#### 新增内容
引入了服务器端 cookie 归属语义，以区分由服务器设置的 cookie 与客户端设置的 cookie，解决某些 cookie 应仅由服务器产生的场景。

#### 技术细节
该功能提供了一种标记或识别应视为服务器来源的 cookie 的机制，帮助服务器识别意外的客户端设置的 cookie（可能源自 XSS、恶意扩展或开发者错误）。该更改在所链接的 HTTP extensions PR 和跟踪 bug 中进行了跟踪和规范化。

#### 适用场景
- 强制执行仅服务器可写的 cookie 不变量并检测客户端篡改。  
- 在认证、会话管理等安全敏感流程中通过确保某些 cookie 仅可由服务器写入来强化安全。  
- 通过使意外的客户端设置 cookie 更易标记和修复，帮助事件响应。

#### 参考资料
- [跟踪 bug #426096760](https://issues.chromium.org/issues/426096760)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5170139586363392)
- [规范](https://github.com/httpwg/http-extensions/pull/3110)
