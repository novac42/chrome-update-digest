## 领域摘要

Chrome 143（stable）引入了 WebTransport Application Protocol Negotiation，作为主要的 Network 领域更新。 这使 Web 应用能够在 WebTransport 握手期间提供一组应用协议，由服务器在握手时选择合适的协议。该更改让开发者对 WebTransport 连接的应用协议选择具有明确的握手级别控制。它通过规范在 WebTransport 上协商应用层协议的方式，提升互操作性和可部署性，从而推进 Web 平台发展。

## 详细更新

Below are the Network-area details that follow from the summary above.

### WebTransport Application Protocol Negotiation（WebTransport 应用协议协商）

#### 新增内容
WebTransport Application Protocol Negotiation 允许在 WebTransport 握手中协商由 Web 应用使用的协议。Web 应用在构造 `WebTransport` 对象时可以指定一组所提供的应用协议，这些协议会在握手期间传送给服务器。

#### 技术细节
- 该特性在构造 `WebTransport` 时暴露一个选项，用于提供客户端向服务器宣告的应用协议标识符。
- 这些所提供的协议作为 WebTransport 握手的一部分传输到服务器，以便服务器选择合适的应用协议。
- 实现和规范细节在所链接的规范和 Chromium 跟踪错误中跟踪。

#### 适用场景
- 允许客户端宣告支持的应用协议，使服务器在建立连接时选择最佳匹配。
- 使基于 WebTransport 构建的服务能够进行显式的应用协议协商，改善兼容性和部署选择。
- 支持需要不同应用层协议且无需额外连接建立逻辑的场景。

#### 参考资料
- [跟踪错误 #416080492](https://issues.chromium.org/issues/416080492)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6521719678042112)  
- [规范](https://w3c.github.io/webtransport/#dom-webtransportoptions-protocols)

已保存到：digest_markdown/webplatform/Network/chrome-143-stable-en.md