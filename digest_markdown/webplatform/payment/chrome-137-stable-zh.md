## 领域摘要

Chrome 137 通过将 WebAuthn 支付凭证创建过程中抛出的错误类型与规范对齐，修复了 Payment 领域中的规范不匹配。最重要的变化是：在跨源 iframe 中尝试创建支付凭证且没有用户激活时，现在会抛出 NotAllowedError 而不是 SecurityError。这使 Chromium 的行为符合 WebAuthn 规范，改善了互操作性并简化了开发者的错误处理。此更改对依赖可预测 WebAuthn 错误语义、测试和安全用户激活流程的支付集成很重要。

## 详细更新

下面的条目扩展了摘要并描述了面向开发者的影响。

### Align error type thrown for payment WebAuthn credential creation: SecurityError becomes NotAllowedError（SecurityError 变为 NotAllowedError）

#### 新增内容
在跨源 iframe 中创建支付 WebAuthn 凭证且没有用户激活的尝试，现在按 WebAuthn 规范抛出 NotAllowedError，而不是 SecurityError。

#### 技术细节
历史上的规范不匹配导致 Chromium 在这种场景下发出 SecurityError。Chromium 137 修正了该行为，使创建凭证的路径遵循 WebAuthn 规范文本：在某些跨源上下文中缺少所需的用户激活会导致 NotAllowedError。依赖先前 SecurityError 的开发者需要相应更新错误处理和测试。

#### 适用场景
- 在嵌入的 iframe 中使用 WebAuthn 创建凭证的支付集成，应在缺少用户激活时捕获 NotAllowedError。
- 支付流程的自动化测试和错误报告应将对 SecurityError 的预期更新为 NotAllowedError。
- 将凭证创建以用户手势为前提的安全敏感流程，现可在各浏览器间看到一致且符合规范的异常，有助于跨浏览器互操作性。

#### 参考资料
- 跟踪问题 #41484826: https://bugs.chromium.org/p/chromium/issues/detail?id=41484826
- ChromeStatus.com 条目: https://chromestatus.com/feature/5096945194598400
- 规范: https://w3c.github.io/webauthn/#sctn-creating-a-credential

```text
digest_markdown/webplatform/Payment/chrome-137-stable-en.md
```