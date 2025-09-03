````markdown
digest_markdown/webplatform/javascript/chrome-139-stable-zh.md

---

# Chrome 139 稳定版发布摘要 – JavaScript 领域

## 1. 执行摘要

Chrome 139 在 JavaScript 领域带来了两项重要更新：放宽了 JavaScript DOM API 的字符校验，以及实现了符合规范的 JSON MIME 类型检测。这些更改提升了互操作性、开发者体验，并加强了基于 JavaScript 的 Web 应用的标准兼容性。

## 2. 主要影响

### 技术影响

- **现有实现**：通过 JavaScript 创建 DOM 元素和属性时，现在支持更广泛的有效名称，减少了与 HTML 解析的差异。
- **新能力**：开发者可以创建此前受限于 JavaScript API 的元素和属性名称，与 HTML 解析器行为保持一致。
- **技术债务**：依赖严格校验的旧代码可能需要审查，以确保兼容放宽后的规则。JSON MIME 类型检测现已完全符合规范，减少了边缘情况处理。

## 3. 风险评估

**关键风险**：
- 未发现破坏性更改；两项功能均向后兼容。
- 安全考虑：放宽 DOM API 校验可能增加 DOM 型 XSS 攻击面，若输入未正确净化。

**中等风险**：
- 可能弃用自定义 MIME 类型检测逻辑，转而使用原生支持。
- 若应用依赖大量使用此前无效名称的 DOM 操作，可能出现轻微性能回退。

## 4. 推荐措施

### 立即行动

- 检查 DOM 创建逻辑，确认对有效元素/属性名称的假设。
- 审查 JSON MIME 类型处理，利用原生检测能力。

### 短期规划

- 更新文档和开发者指南，反映新的 DOM API 能力。
- 重构自定义 MIME 嗅探代码，依赖浏览器原生行为。

### 长期策略

- 关注与放宽 DOM 校验相关的安全公告。
- 推动所有支持的浏览器一致采用标准。

## 5. 功能分析

---

### Allow more characters in JavaScript DOM APIs（JavaScript DOM API 支持更多字符）

**影响级别**：🟡 重要

**变更内容**：
JavaScript DOM API 中元素和属性名称的校验已放宽，与 HTML 解析器保持一致，允许更多有效字符和名称。

**意义**：
此更改消除了 HTML 解析与 JavaScript DOM 操作之间的不一致，使开发者能够创建此前仅在 HTML 中有效的元素和属性名称。提升了互操作性，并减少了动态生成 DOM 结构时的意外错误。

**实施建议**：
- 检查任何通过代码创建 DOM 元素或属性的逻辑，确认对有效名称的假设。
- 测试元素/属性名称包含非常规字符的边界情况。
- 确保输入净化，以防安全漏洞。

**参考资料**：
- [Tracking bug #40228234](https://issues.chromium.org/issues/40228234)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416)
- [Spec](https://dom.spec.whatwg.org/#namespaces)

---

### Specification-compliant JSON MIME type detection（规范兼容的 JSON MIME 类型检测）

**影响级别**：🟡 重要

**变更内容**：
Chrome 现已识别所有 WHATWG mimesniff 规范定义的有效 JSON MIME 类型，包括所有以 `+json` 结尾的子类型，以及 `application/json` 和 `text/json`。

**意义**：
此更新确保依赖 JSON 检测的 Web API 和功能与规范保持一致，减少了自定义 MIME 类型处理需求，并提升了与其他平台和工具的互操作性。

**实施建议**：
- 重构任何自定义的 JSON MIME 类型检测逻辑，改为依赖浏览器原生支持。
- 验证消费 JSON 数据的 API 能够正确处理所有规范兼容的 MIME 类型。
- 更新服务器端响应，确保 JSON 数据使用合适的 MIME 类型。

**参考资料**：
- [ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528)
- [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

---
````