区域摘要

Chrome 140 的 Web API 更新聚焦于提升 Web 应用的可靠性与平台集成。主要主题包括更确定性的流式读取、在桌面上扩展的原生应用关联检查，以及更强的服务器端 cookie 溯源控制。这些更改使开发者对二进制流有更严格的控制，提供更好的方式检测相关的本地安装，并在服务器与客户端 Cookie 之间提供更明确的区分——推动 Web 平台的健壮性和安全性。总体上，它们减少了先前需要变通或启发式处理的边缘情况。

## 详细更新

以下内容在上文摘要基础上展开，并列出 Chrome 140 中每项 Web API 更改的简要技术说明、开发者适用场景和参考资料。

### `ReadableStreamBYOBReader` `min` option（新增 `min` 选项）

#### 新增内容
该功能为已有的 `ReadableStreamBYOBReader.read(view)` 方法引入了一个 `min` 选项，允许调用者要求读取在写入到提供的 `ArrayBufferView` 的元素达到最小数量后才 resolve。

#### 技术细节
`read(view)` 调用已接受一个用于接收数据的 `ArrayBufferView`；新增 `min` 提供了一个约定，即返回的 promise 在至少写入 `min` 个元素之前不应 resolve。有关权威行为和语义，请参阅 Streams 规范。

#### 适用场景
适用于消费端在处理前需要保证最小二进制数据量的场景（例如帧/二进制协议或大批量缓冲处理），以避免反复的短读取并简化缓冲管理。

#### 参考资料
- https://issues.chromium.org/issues/40942083
- https://chromestatus.com/feature/6396991665602560
- https://streams.spec.whatwg.org/#byob-reader-read

### Get Installed Related Apps API on desktop（在桌面上可用）

#### 新增内容
Get Installed Related Apps API（`navigator.getInstalledRelatedApps`）现已在桌面端可用，允许站点在 web 源与应用之间存在已建立关联时，获取对应相关应用是否已安装。

#### 技术细节
仅当应用与 web 源之间存在已建立的关联时，站点才可以调用 `navigator.getInstalledRelatedApps`。该 API 最初在早期 Chrome 版本中推出，现在扩展到了桌面环境。

#### 适用场景
支持渐进式增强流程，站点可以检测用户已安装的本地应用，以在存在相关应用时提供深度链接、安装提示或替代的用户体验路径。

#### 参考资料
- https://issues.chromium.org/issues/895854
- https://chromestatus.com/feature/5695378309513216
- https://wicg.github.io/get-installed-related-apps/spec

### Http cookie prefix（HTTP cookie 前缀）

#### 新增内容
引入了一种 HTTP cookie 前缀机制，帮助区分由服务器设置的 cookie 与由客户端代码设置的 cookie。这有助于防御通过 XSS、扩展或其他客户端行为者引入的意外或恶意 cookie。

#### 技术细节
通过采用 cookie 前缀约定，服务器可以标记预期由服务器设置的 cookie，从而在 cookie 溯源重要时，使服务器端处理和策略决策更可靠。

#### 适用场景
适用于必须防止被客户端脚本伪造的服务器驱动型 cookie，例如需要服务器确定来源以提升安全性的认证或完整性 cookie。

#### 参考资料
- https://issues.chromium.org/issues/426096760
- https://chromestatus.com/feature/5170139586363392
- https://github.com/httpwg/http-extensions/pull/3110

已保存至：digest_markdown/webplatform/Web API/chrome-140-stable-en.md