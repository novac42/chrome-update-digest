---
layout: default
title: Chrome 139 Web API 更新摘要（稳定版）
---

````markdown
Save to: digest_markdown/webplatform/Web API/chrome-139-stable-zh.md

---

# Chrome 139 Web API 更新摘要（稳定版）

## 1. 执行摘要

Chrome 139 在 Web API 领域带来了多项重要更新，包括增强的多源应用 Web 应用清单能力、对 JSON MIME 类型检测的标准兼容性提升、扩展的 WebGPU 功能支持，以及更细粒度的崩溃报告端点。这些更改共同提升了互操作性、开发者控制力和平台健壮性。

## 2. 主要影响

### 技术影响

- **现有实现**：依赖旧版 JSON MIME 类型检测或崩溃报告端点的应用可能需要做小幅调整。
- **新能力**： 
  - Web 应用现在可通过 `scope_extensions` 跨多个源。
  - WebGPU 获得对核心功能和限制的显式支持。
  - 开发者可将崩溃报告定向到专用端点。
- **技术债务**： 
  - 可淘汰针对 JSON MIME 嗅探和崩溃报告过滤的旧有变通方案。
  - 多源应用架构可进一步简化。

## 3. 风险评估

**关键风险**：
- 未发现破坏性更改，但错误使用新的清单字段或崩溃报告端点可能导致配置错误。
- 安全性：扩展应用作用域至多个源时，需要更强的源关联和校验。

**中等风险**：
- 弃用非标准 JSON MIME 处理可能影响部分边缘集成场景。
- 性能影响较小，但多源应用可能增加资源管理复杂性。

## 4. 推荐措施

### 立即行动

- 检查并更新 Web 应用清单，在需要多源支持时使用 `scope_extensions`。
- 审核 API 中的 JSON MIME 类型处理，确保符合更新后的检测逻辑。
- 如仅需崩溃报告，请指定 `crash-reporting` 端点。

### 短期规划

- 重构依赖非标准 JSON MIME 类型或广义崩溃报告端点的旧代码。
- 评估 WebGPU 使用情况，更新功能检测逻辑以利用 `core-features-and-limits`。

### 长期策略

- 持续关注多源 Web 应用模式的采用和反馈。
- 跟踪 WebGPU 及崩溃报告 API 的后续演进，做好未来适配。
- 持续对齐 MIME 类型处理和清单规范等不断演进的 Web 标准。

## 5. 功能分析

---

### Web app scope extensions（Web 应用作用域扩展）

**影响级别**：🟡 重要

**变更内容**：
在 Web 应用清单中新增 `scope_extensions` 字段，允许 Web 应用将作用域扩展到其他源。这使得控制多个子域或顶级域的站点可以作为单一 Web 应用呈现。需要通过 `.well-known` 文件进行关联确认。

**意义**：
该变更简化了多源 Web 应用的用户体验和开发流程，使组织能够在不同域间实现无缝导航和统一应用身份。

**实施建议**：
- 如应用跨多个源，请在 Web 应用清单中添加 `scope_extensions`。
- 确保所有列出的源均部署了所需的 `.well-known` 关联文件。
- 测试所有目标源的导航和安装流程。

**参考资料**：
- [Tracking bug #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5746537956114432)
- [Spec](https://github.com/WICG/manifest-incubations/pull/113)

---

### Specification-compliant JSON MIME type detection（规范兼容的 JSON MIME 类型检测）

**影响级别**：🟡 重要

**变更内容**：
Chrome 现已根据 WHATWG mimesniff 规范识别所有有效的 JSON MIME 类型，包括以 `+json` 结尾的任意子类型，以及 `application/json` 和 `text/json`。这确保了依赖 JSON 检测的 Web API 行为一致。

**意义**：
此更新提升了互操作性和标准兼容性，降低了处理非标准 MIME 类型 JSON 负载时出现隐性 bug 的风险。

**实施建议**：
- 审查 API 端点和客户端代码，查找对旧版或非标准 JSON MIME 类型的依赖。
- 必要时将服务器响应更新为规范 MIME 类型。
- 测试与第三方 API 的集成兼容性。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528)
- [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

---

### WebGPU `core-features-and-limits`

**影响级别**：🟢 可选优化

**变更内容**：
引入 `core-features-and-limits` 功能，表明 WebGPU 适配器和设备支持规范中定义的核心功能和限制。

**意义**：
为开发者提供了可靠的方式检测和利用 WebGPU 的基础能力，提升跨平台一致性，并支持更健壮的功能检测。

**实施建议**：
- 更新 WebGPU 功能检测逻辑，检查 `core-features-and-limits`。
- 根据功能支持情况调整降级或渐进增强策略。

**参考资料**：
- [Tracking bug #418025721](https://issues.chromium.org/issues/418025721)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496)
- [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

---

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports（崩溃报告 API：指定 `crash-reporting` 仅接收崩溃报告）

**影响级别**：🟡 重要

**变更内容**：
开发者现在可以指定 `crash-reporting` 端点，仅接收崩溃报告，而非默认端点聚合的多种报告类型。可为此目的向 well-known 端点提供单独的 URL。

**意义**：
该变更使崩溃报告的监控和处理更加精确，减少无关数据干扰，提升事件响应效率。

**实施建议**：
- 如仅需崩溃数据，请将崩溃报告配置为使用 `crash-reporting` 端点。
- 确保后端已准备好处理来自新端点的报告。
- 关注报告数量或内容的变化。

**参考资料**：
- [Tracking bug #414723480](https://issues.chromium.org/issues/414723480)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5129218731802624)
- [Spec](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)

---
````