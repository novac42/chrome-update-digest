## 领域摘要

Chrome 141 的 Security-Privacy 更新收紧了跨源 cookie 处理，并为网页资源引入了基于来源的信任模型。Storage Access API 现严格遵循同源策略，默认将 cookie 附加限制在精确的 iframe 所属 origin，从而减少意外的第三方 cookie 暴露。Signature-based Integrity 增加了对依赖项的密码学验证，使站点可要求浏览器验证使用 Ed25519 密钥签名的响应。这些更改共同提升安全基线，降低供应链风险，并为安全嵌入与依赖管理提供更清晰、可预测的基元。

## 详细更新

这些更新聚焦于更强的存储同源边界及对子资源的密码学保证，引导开发者采用更安全的集成模式。

### Strict Same Origin Policy for Storage Access API（Storage Access API 严格同源策略）

#### 新增内容
Storage Access API 现严格遵循同源策略语义：在框架中使用 document.requestStorageAccess() 后，默认仅将 cookie 附加到指向该 iframe 所属 origin 的请求（而非更宽泛的整个站点）。

#### 技术细节
- 在调用 requestStorageAccess() 之后，cookie 附加对嵌入框架来说是 origin 作用域的。
- 该行为由站点级收窄至 origin 级，减少跨源 cookie 泄漏。
- 在嵌入框架内依赖 cookie 的跨源子资源，请求必须确保指向精确的 iframe 所属 origin，或按需调整策略。

#### 适用场景
- 需要 cookie 的嵌入式认证或账号小部件必须使子资源请求与该 iframe 的 origin 对齐。
- 第三方嵌入获得更严格的隔离，降低在相关但不同的 origin 之间意外暴露 cookie 的风险。
- 站点可审计 iframe 的资源图，确保依赖 cookie 的请求与 origin 匹配。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/379030052)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5169937372676096)
- [GitHub](https://github.com/privacycg/storage-access/pull/213)

### Signature-based Integrity（基于签名的完整性）

#### 新增内容
服务器可使用 Ed25519 密钥对对响应进行签名，开发者可要求用户代理对依赖资源验证这些签名，从而为站点依赖建立密码学来源证明。

#### 技术细节
- 响应用 Ed25519 签名；在页面要求时，浏览器会在接受资源前验证签名。
- 这提供了独立于传输渠道（例如 CDN 或缓存）的密码学信任锚。
- 它通过将资源绑定到授权签名者（而不仅仅是哈希）来补充现有的完整性检查。

#### 适用场景
- 防范针对第三方脚本、WASM 模块、样式等关键资产的供应链攻击。
- 通过验证其来自预期的签名者，安全地使用 CDN 托管的资产。
- 加强在资产穿越不受信中介时的部署流水线安全。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/375224898)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5032324620877824)
- [Spec](https://wicg.github.io/signature-based-sri)
