---
layout: default
title: chrome-139-zh
---

### 1. 领域摘要

Chrome 139 对 Secure Payment Confirmation (SPC) 进行了有针对性的改进，简化了功能检测并加强了用于支付的加密设备绑定。对开发者影响最大的是一个新的 JavaScript 可用性 API，它避免了为了检查 SPC 支持而构造完整的 PaymentRequest，以及绑定于浏览器的密钥，它为 SPC 断言添加了一个不跨设备同步的加密签名。两者共同推进了 Web 支付平台，通过改善能力检测的开发者体验并提升设备绑定支付凭证的安全态势。这些更新重要因为它们降低了集成摩擦，并帮助网站满足更严格的设备绑定和防欺诈要求。

## 详细更新

下面是基于上述摘要的 Chrome 139 在 Payment 领域的具体更新。

### The `securePaymentConfirmationAvailability` API（可用性检查 API）

#### 新增内容
- 一个小型的 JavaScript API，用于在不创建 PaymentRequest 的情况下检查 Secure Payment Confirmation (SPC) 是否可用。

#### 技术细节
- 提供对 SPC 的显式可用性检查，使调用方无需仅为检测支持而构造 `PaymentRequest` 对象和参数。
- 减少了之前那个笨拙的流程，该流程需要构建并查询 `PaymentRequest` 来进行功能检测。

#### 适用场景
- 渐进增强：仅在可用时有条件地启用 SPC 用户体验。
- 性能与用户体验：避免仅为能力检查而创建与销毁 `PaymentRequest` 实例。
- 在支付流程和集成中实现更干净的功能检测逻辑。

#### 参考资料
- https://issues.chromium.org/issues/40258712
- https://chromestatus.com/feature/5165040614768640
- https://github.com/w3c/secure-payment-confirmation/pull/285

### Secure Payment Confirmation: Browser Bound Keys（浏览器绑定密钥）

#### 新增内容
- 在 SPC 断言和凭证创建上增加了额外的加密签名，所用的相应私钥绑定于浏览器并不会跨设备同步。

#### 技术细节
- 引入一个本地存储（不同步）的浏览器绑定密钥，用于对 SPC 断言/凭证创建进行签名，提供额外的设备绑定层。
- 有助于使 SPC 凭证符合要求，即证明交易绑定于特定设备，而不仅仅是一个已同步的凭证。

#### 适用场景
- 为需要设备绑定证明的高价值或合规敏感支付提供更强的防欺诈能力。
- 在需要将签名密钥来源限制在单一设备的合规场景中使用。
- 开发者可以依赖浏览器提供的增强证明语义，而无需实现自定义的设备绑定逻辑。

#### 参考资料
- https://issues.chromium.org/issues/377278827
- https://chromestatus.com/feature/5106102997614592
- https://w3c.github.io/secure-payment-confirmation/#sctn-browser-bound-key-store

输出文件：digest_markdown/webplatform/Payment/chrome-139-stable-en.md
