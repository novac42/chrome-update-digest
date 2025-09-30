---
layout: default
title: chrome-136-zh
---

### 1. 领域摘要

Chrome 136 Stable 在 Security-Privacy 领域引入了针对性的隐私和报告改进：为 iframes 添加了一种新的 Permissions Policy 报告类型，并减少了来自 Accept-Language header 的指纹识别信息。对开发者影响最大的更改是更细粒度地检测 iframe 权限传播问题，以及语言偏好向服务器传达和通过 `navigator.languages` 暴露方式的改变。这些更新通过改进策略违规的可观测性和限制被动指纹识别向量来推进 Web 平台发展。其重要性在于在减少例行请求中可识别用户的信息的同时，能够提供更准确的安全诊断。

## 详细更新

以下条目扩展上述摘要，重点说明面向开发者的技术和实际影响。

### Permissions Policy reports for iframes（针对 iframes 的 Permissions Policy 报告）

#### 新增内容
引入了一种名为 "Potential Permissions Policy violation" 的新违规类型，该类型检查 Permissions Policy（包括 report-only policy）以及在 iframes 上设置的 allow attribute，以检测被强制执行的 Permissions Policy 与传播到 iframes 的权限之间的冲突。

#### 技术细节
该新违规类型会评估生效的 Permissions Policy 和 iframe 的 allow attribute，以标记那些传播的权限与顶层策略强制的内容冲突的情况。报告遵循下方规范中描述的 Permissions Policy 报告模型。

#### 适用场景
- 在开发和生产中检测并报告 iframe 权限传播的错误配置。
- 通过揭示可能导致意外权限授予的策略不匹配来改进安全监控。
- 在部署 report-only policies 以测试策略更改时，帮助合规和调试。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40941424
- https://chromestatus.com/feature/5061997434142720
- https://w3c.github.io/webappsec-permissions-policy/#reporting

### Reduce fingerprinting in Accept-Language header information（减少 Accept-Language 头的信息指纹识别）

#### 新增内容
减少 Accept-Language header 值字符串在 HTTP 请求和 `navigator.languages` 中暴露的信息量。Chrome 不再在每个 HTTP 请求中发送用户的完整首选语言列表，而是在 Accept-Language header 中仅发送用户最偏好的语言。

#### 技术细节
Chrome 在发出 HTTP 请求时将 Accept-Language header 限制为单一的首选语言，并降低 `navigator.languages` 暴露的粒度，以缓解被动指纹识别。此更改减少了跨请求泄露用户完整语言偏好列表的情况。

#### 适用场景
- 通过减少一种常见的跨请求指纹识别向量来提升终端用户隐私。
- 可能会影响依赖完整 Accept-Language 列表的服务器端区域设置检测和分析；开发者应验证区域回退逻辑。
- 对注重隐私的功能和威胁模型有用，在这些场景需要尽量减少每次请求的信息熵。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1306905
- https://chromestatus.com/feature/5042348942655488
