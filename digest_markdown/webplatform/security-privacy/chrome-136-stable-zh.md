# Chrome 136 安全-隐私更新

## 区域摘要

Chrome 136 引入了重要的隐私增强功能，专注于减少指纹识别和提高开发者对策略违规的可见性。最具影响力的更改是减少 Accept-Language 标头信息，通过限制 HTTP 请求中暴露的语言数据，大幅降低了指纹识别表面。此外，iframe 的新权限策略违规报告为开发者提供了更好的策略冲突调试能力。这些更新体现了 Chrome 持续致力于加强网络隐私，同时保持开发者工具质量，推动平台朝着更具隐私保护性的网络生态系统发展。

## 详细更新

这些安全和隐私改进建立在 Chrome 正在进行的工作基础上，旨在平衡用户保护与开发者体验，提供增强的隐私保护措施和更好的调试工具。

### Permissions Policy reports for iframes

#### 新增功能
当权限策略执行与通过 allow 属性传播给 iframe 的权限之间存在冲突时，Chrome 现在会生成"潜在权限策略违规"报告。

#### 技术细节
新的违规类型专门检查常规和仅报告的权限策略配置以及 iframe allow 属性，以检测不匹配情况。此报告机制有助于识别 iframe 权限可能与父文档策略意图不一致的情况，为以前未监控的潜在安全边界提供可见性。

#### 使用场景
开发者现在可以更有效地调试权限策略配置，识别 iframe allow 属性与父策略冲突的情况。这对于使用嵌入内容或第三方 iframe 的应用程序特别有价值，因为权限边界需要仔细管理。报告有助于确保安全策略在框架层次结构中正确实施。

#### 参考资料
- [跟踪问题 #40941424](https://bugs.chromium.org/p/chromium/issues/detail?id=40941424)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5061997434142720)
- [规范](https://w3c.github.io/webappsec-permissions-policy/#reporting)

### Reduce fingerprinting in Accept-Language header information

#### 新增功能
Chrome 现在将 Accept-Language 标头限制为仅包含用户最偏好的语言，相比之前的完整语言列表，显著减少了网站可获得的指纹识别信息。

#### 技术细节
Chrome 现在仅在 Accept-Language 标头中发送主要语言偏好，而不是在 HTTP 请求和 `navigator.languages` 中暴露用户语言偏好的完整有序列表。此更改减少了可用于浏览器指纹识别的熵值，同时保持了内容协商的核心国际化功能。

#### 使用场景
网站仍然可以使用主要语言偏好执行适当的内容本地化，但基于完整语言配置对用户进行指纹识别的能力显著降低。这对于注重隐私的应用程序特别重要，有助于符合反指纹识别要求，同时保持基本的国际化能力。

#### 参考资料
- [跟踪问题 #1306905](https://bugs.chromium.org/p/chromium/issues/detail?id=1306905)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5042348942655488)