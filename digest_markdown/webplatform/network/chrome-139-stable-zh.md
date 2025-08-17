---
layout: default
title: Chrome 139 稳定版 – 网络领域更新摘要
---

````markdown
digest_markdown/webplatform/network/chrome-139-stable-zh.md

---

# Chrome 139 稳定版 – 网络领域更新摘要

## 1. 执行摘要

Chrome 139 带来了两项重要的网络相关更新：通过 `Accept-Language` 头减少指纹识别，以及在 Windows 上随机分配 TCP 端口。这些更改提升了用户隐私和网络安全，符合现代 Web 标准和最佳实践。

## 2. 主要影响

### 技术影响

- **现有实现**：依赖详细 `Accept-Language` 头或假设 TCP 端口分配可预测的应用可能需要更新。
- **新能力**：为用户带来更好的隐私保护，并增强对某些网络攻击的安全性。
- **技术债务**：解析或依赖完整语言列表或静态端口行为的遗留代码应进行审查和重构。

## 3. 风险评估

**关键风险**：
- **破坏性更改**：`Accept-Language` 头的粒度降低可能影响本地化或内容协商逻辑。
- **安全考量**：TCP 端口随机化可能影响依赖可预测端口分配的系统。

**中等风险**：
- **弃用**：通过头部进行详细语言协商的方式被隐式弃用。
- **性能影响**：影响极小，但在 Windows 网络栈行为中可能存在边缘情况。

## 4. 推荐措施

### 立即行动

- 审查服务器端解析 `Accept-Language` 头的逻辑，检查对语言列表长度或顺序的假设。
- 检查网络诊断和工具，确保兼容随机化的 TCP 端口分配。

### 短期规划

- 更新本地化和内容协商策略，减少对细粒度 `Accept-Language` 数据的依赖。
- 在 Windows 部署环境中监控网络错误日志，关注端口分配异常问题。

### 长期策略

- 推动所有面向网络的功能采用保护隐私的默认设置。
- 规划进一步减少被动指纹识别面，并持续强化网络栈行为。

## 5. 功能分析

### Reduce fingerprinting in Accept-Language header information（减少 Accept-Language 头信息中的指纹识别）

**影响级别**：🔴 关键

**变更内容**：
减少了 `Accept-Language` 头值字符串在 HTTP 请求和 `navigator.languages` 中暴露的信息量。Chrome 不再在每个 HTTP 请求的 `Accept-Language` 头中发送用户的完整首选语言列表，而只发送用户的首选语言。

**重要意义**：
此更改显著减少了浏览器的指纹识别面，使追踪者更难仅通过语言偏好唯一识别用户。同时也符合隐私最佳实践和监管要求。

**实施建议**：
- 审查任何依赖 `Accept-Language` 头完整语言列表的服务器端逻辑。
- 更新本地化和内容协商机制，以便能够优雅地处理仅接收主语言的情况。
- 向本地化团队传达变更，并相应更新文档。

**参考资料**：
- [Tracking bug #1306905](https://issues.chromium.org/issues/1306905)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

---

### Randomize TCP port allocation on Windows（在 Windows 上随机分配 TCP 端口）

**影响级别**：🟡 重要

**变更内容**：
在 Windows（2020 年及以后版本）上启用 TCP 端口随机化，在不期望频繁端口重用的情况下生效。此举可缓解端口冲突风险，以及与可预测端口分配相关的某些网络攻击。

**重要意义**：
随机分配 TCP 端口提升了安全性，使攻击者更难预测将使用哪些端口，从而降低端口劫持及相关攻击的风险。

**实施建议**：
- 在 Windows 2020 及以上版本上测试网络应用，确保兼容随机端口分配。
- 更新任何假设端口分配可预测的脚本或监控工具。
- 监控与端口分配相关的意外连接失败或超时问题。

**参考资料**：
- [Tracking bug #40744069](https://issues.chromium.org/issues/40744069)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

---
````