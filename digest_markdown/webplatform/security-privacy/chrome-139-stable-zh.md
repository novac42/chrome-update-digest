````markdown
保存至: digest_markdown/webplatform/Security-Privacy/chrome-139-stable-zh.md

---

# Chrome 139 安全与隐私更新摘要

## 1. 执行摘要

Chrome 139 在安全与隐私领域带来了重要更新：当内容安全策略（CSP）阻止创建 Worker 或 SharedWorker 时，错误事件现在会异步触发。此更改使 Chrome 的行为与 CSP 规范保持一致，提高了开发者在受限安全策略下处理 worker 实例化时的一致性和可预测性。

## 2. 关键影响

### 技术影响

- **现有实现**：依赖于 CSP 阻止 worker 时同步异常的应用，必须更新错误处理逻辑，改为响应异步错误事件。
- **新能力**：开发者现在可以可靠地监听 CSP 阻止 worker 创建时的错误事件，从而实现更健壮的回退和日志记录策略。
- **技术债务**：依赖异常的旧代码可能会静默失败或表现异常。需重构以确保兼容新的事件驱动错误模型。

## 3. 风险评估

**关键风险**：
- **破坏性更改**：期望 CSP 阻止 worker 时同步异常的代码将不再按原方式工作，可能导致错误处理遗漏和用户体验下降。
- **安全考量**：此更改加强了对 CSP 标准的遵循，减少了 worker 实例化过程中的歧义和潜在安全漏洞。

**中等风险**：
- **弃用**：之前基于异常的错误处理方式已被事件驱动处理方式有效弃用。
- **性能影响**：异步错误事件可能导致错误检测出现轻微延迟，但整体应用性能不太可能受到影响。

## 4. 推荐措施

### 立即行动

- 检查所有 `new Worker(url)` 和 `new SharedWorker(url)` 在 CSP 阻止场景下的使用情况。
- 重构错误处理逻辑，改为监听错误事件而非捕获异常。

### 短期规划

- 更新文档和开发者指南，反映新的错误事件模型。
- 监控应用日志，查找遗漏的 worker 实例化错误，并根据需要调整错误报告。

### 长期策略

- 推动所有 Web API 实现一致的 CSP 错误处理。
- 跟踪未来 CSP 规范变更及浏览器实现，保持兼容性。

## 5. 功能分析

### Fire error event for Content Security Policy (CSP) blocked worker（CSP 阻止 worker 时触发错误事件）

**影响级别**：🔴 关键

**变更内容**：
Chrome 现在在获取阶段检查 CSP，当脚本尝试创建被 CSP 阻止的 Worker 或 SharedWorker 时，会异步触发错误事件。此前，Chrome 会在此类情况下抛出同步异常。

**重要意义**：
此更改使 Chrome 符合 CSP 规范，确保 worker 实例化时的错误处理一致且可预测。开发者可依赖错误事件机制，提高安全敏感应用的健壮性，降低静默失败风险。

**实施指南**：
- 用事件监听器替换围绕 `new Worker(url)` 和 `new SharedWorker(url)` 的 try/catch 逻辑，监听 `error` 事件。
- 在不同 CSP 配置下测试 worker 创建，确保错误检测和处理正常。
- 更新自动化测试，验证当 CSP 阻止 worker 创建时错误事件能如预期触发。

**参考资料**：
- [Tracking bug #41285169](https://issues.chromium.org/issues/41285169)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5177205656911872)
- [Spec](https://www.w3.org/TR/CSP3/#fetch-integration)

---
````