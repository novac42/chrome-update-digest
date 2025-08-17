```markdown
保存至: digest_markdown/webplatform/Multimedia/chrome-139-stable-zh.md

---

# Chrome 139 多媒体更新摘要

## 1. 执行摘要

Chrome 139 在多媒体领域带来了重要更新，新增了 “Web Authentication immediate mediation” 功能。此对 Web Authentication API 的增强，使认证流程更加简化和用户友好：当凭据可用时，浏览器会立即显示登录界面，否则会迅速拒绝请求。该变更影响了利用 passkey 或密码的 Web 应用的安全性和用户体验。

## 2. 主要影响

### 技术影响

- **对现有实现的影响**：使用 `navigator.credentials.get()` 的应用现在可以选择启用 immediate mediation，从而改变认证流程。不指定该模式的现有实现不受影响，但采用该模式的实现需处理新的拒绝行为。
- **新能力**：开发者可提供更确定且响应迅速的认证体验，减少不必要的界面提示，并提升感知性能。
- **技术债务考量**：依赖传统认证流程的团队应评估迁移路径，以利用 immediate mediation 提升用户体验和安全性。

## 3. 风险评估

**关键风险**：
- **破坏性更改**：除非明确采用 immediate mediation，否则现有代码无破坏性更改。
- **安全考量**：该功能加强了对凭据中介的控制，通过减少不必要的凭据提示，有助于降低网络钓鱼风险。

**中等风险**：
- **弃用**：暂无直接弃用，但团队应关注未来旧中介模式的弃用动态。
- **性能影响**：预计将带来积极影响，因为减少了界面调用次数，并在无凭据时更快拒绝。

## 4. 推荐行动

### 立即行动

- 审查使用 `navigator.credentials.get()` 的认证流程，评估 immediate mediation 的适用性。
- 更新用户界面逻辑，在无凭据时优雅处理 `NotAllowedError` 拒绝。

### 短期规划

- 规划用户测试，评估 immediate mediation 对认证成功率和用户满意度的影响。
- 关注 Chromium 和 W3C 相关讨论，获取该中介模式的进一步优化或最佳实践。

### 长期策略

- 跟踪采纳指标和反馈，为更广泛迁移到现代 Web Authentication 流程提供依据。
- 为可能弃用传统中介模式做好准备，确保代码库与标准演进保持一致。

## 5. 功能分析

### Web Authentication immediate mediation（Web 身份验证即时中介）

**影响级别**：🟡 重要

**变更内容**：
为 `navigator.credentials.get()` 引入了一种新的中介模式。启用后，若站点有可用的 passkey 或密码，浏览器会立即显示登录界面；若无可用凭据，则 promise 会以 `NotAllowedError` 拒绝且不显示界面。

**意义说明**：
该功能带来更可预测、高效的认证体验。仅在有凭据时才提示用户，减少混淆和不必要的界面打断。同时，通过限制凭据提示的暴露，提升了安全性。

**实现建议**：
- 评估当前对 `navigator.credentials.get()` 的使用情况，适时采用 immediate mediation。
- 确保错误处理逻辑已更新，能正确处理 `NotAllowedError` 拒绝。
- 测试认证流程，确保用户体验得到提升，并覆盖边缘场景。

**参考资料**：
- [Tracking bug #408002783](https://issues.chromium.org/issues/408002783)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704)
- [Spec](https://github.com/w3c/webauthn/pull/2291)

---
```