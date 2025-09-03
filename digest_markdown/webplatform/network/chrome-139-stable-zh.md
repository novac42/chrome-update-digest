````markdown
digest_markdown/webplatform/network/chrome-139-stable-zh.md

---

# Chrome 139 稳定版 - 网络领域摘要

## 1. 执行摘要

Chrome 139 带来了两项重要的网络相关更改：在 Windows（2020 及以上版本）上随机分配 TCP 端口，以及通过 Accept-Language 头减少指纹信息。这些更新提升了安全性、隐私性和平台的健壮性，并直接影响网络栈行为及 Web 隐私模型。

## 2. 关键影响

### 技术影响

- **TCP Port Randomization**（TCP 端口随机化）：增强了针对端口预测攻击的安全性，降低了端口重用问题的风险，但可能影响依赖确定性端口分配的系统。
- **Accept-Language Header Reduction**（Accept-Language 头信息减少）：通过限制 HTTP 请求中发送的语言数据，减少了用户指纹信息，对依赖细粒度语言检测的本地化策略和分析产生影响。

#### 新能力

- 在 Windows 上增强了针对网络攻击的防护。
- 默认提升了 HTTP 请求中的用户隐私。

#### 技术债务考量

- 假设之前端口分配或语言头行为的遗留系统或测试可能需要更新。
- 可能需要审查依赖网络的功能以确保兼容性。

## 3. 风险评估

**关键风险：**

- **破坏性更改**：期望确定性 TCP 端口分配的应用或网络工具可能出现意外行为。
- **安全考量**：减少指纹信息有积极作用，但可能影响依赖语言头的安全分析或欺诈检测。

**中等风险：**

- **弃用**：隐式弃用完整 Accept-Language 头信息的暴露。
- **性能影响**：影响较小，但应监控网络栈更改是否带来意外延迟或连接问题。

## 4. 推荐措施

### 立即行动

- 审查与网络相关的代码，检查对 Windows 上 TCP 端口分配的假设。
- 检查本地化和分析系统是否依赖 Accept-Language 头的细粒度信息。

### 短期规划

- 更新文档和测试套件以反映新的网络行为。
- 向负责国际化和网络安全的团队传达相关更改。

### 长期策略

- 持续关注因端口随机化和语言头信息减少带来的反馈或问题。
- 规划进一步提升网络协议中的隐私保护。

## 5. 功能分析

---

### Randomize TCP port allocation on Windows（Windows 上随机分配 TCP 端口）

**影响级别**：🔴 关键

**变更内容**：
在 Windows 2020 及以上版本，TCP 端口分配现已随机化，从而缓解了可预测端口分配和生日问题相关的风险。此更改仅在快速端口重用不会引发问题的情况下启用。

**重要性说明**：
端口分配随机化增强了网络安全性，使攻击者更难预测端口使用，降低了特定类型攻击的风险。同时也解决了端口重用时序问题，提升整体可靠性。

**实施指南**：
- 检查任何依赖确定性端口分配的代码或基础设施。
- 更新网络监控和诊断工具以适应端口随机化行为。
- 测试与 Chrome 网络栈交互的第三方软件的兼容性。

**参考资料**：
- [Tracking bug #40744069](https://issues.chromium.org/issues/40744069)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

---

### Reduce fingerprinting in Accept-Language header information（减少 Accept-Language 头信息中的指纹）

**影响级别**：🟡 重要

**变更内容**：
Chrome 现仅在 Accept-Language HTTP 头中发送用户最偏好的语言，并在 `navigator.languages` 中暴露更少的细粒度数据，从而减少可用于指纹识别的信息量。

**重要性说明**：
限制请求中的语言数据提升了用户隐私，降低了通过语言指纹进行跨站跟踪的风险。但可能影响依赖详细语言偏好进行本地化或分析的服务。

**实施指南**：
- 检查本地化流程和分析是否依赖完整 Accept-Language 头信息。
- 更新服务器端逻辑，以适应减少的语言信息。
- 向相关方和终端用户传达隐私改进内容。

**参考资料**：
- [Tracking bug #1306905](https://issues.chromium.org/issues/1306905)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

---
````