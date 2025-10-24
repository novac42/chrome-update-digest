---
layout: default
title: security-privacy-zh
---

## 领域摘要

Chrome 137 修复了用于支付凭证创建的 WebAuthn 错误类型不匹配问题，使运行时行为与 WebAuthn 规范一致。该更改将此前在跨源 iframe 中在没有用户激活的情况下创建支付凭证时抛出的 SecurityError 转为 NotAllowedError。此举提高了互操作性，并使跨框架实现支付和认证流程的开发者在错误处理上更可预测。开发者应审查跨源支付 WebAuthn 场景的错误处理和测试，以避免误判失败类型。

## 详细更新

### Align error type thrown for payment WebAuthn credential creation: SecurityError becomes NotAllowedError（在支付 WebAuthn 凭证创建中将 SecurityError 改为 NotAllowedError）

#### 新增内容
在跨源 iframe 中没有用户激活的情况下创建支付凭证现在会抛出 NotAllowedError，而不是 SecurityError，与 WebAuthn 规范一致。

#### 技术细节
此更改修正了历史上的规范不匹配：运行时现在报告规范为该场景要求的错误类型。该更改影响从跨源 iframe 调用且缺乏用户激活时的支付凭证的 WebAuthn 凭证创建路径。

#### 适用场景
- 在 iframe 中创建 WebAuthn 凭证的支付集成应更新错误处理，以在与用户激活相关的失败中预期 NotAllowedError。  
- 自动化测试和错误分类逻辑应作相应调整，以避免将这些情况视为更广泛的安全策略违规。

#### 参考资料
- 跟踪 bug #41484826: https://bugs.chromium.org/p/chromium/issues/detail?id=41484826  
- ChromeStatus.com 条目: https://chromestatus.com/feature/5096945194598400  
- 规范: https://w3c.github.io/webauthn/#sctn-creating-a-credential
