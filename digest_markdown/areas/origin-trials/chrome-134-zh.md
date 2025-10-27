---
layout: default
title: chrome-134-zh
---

## 领域摘要

Chrome 134 的 Origin Trials 专注于两个有针对性的试验：推出一个 Digital Credential API origin trial，以及运行一个弃用试验以恢复旧的 `<select>` 解析行为。Digital Credential API 试验允许网站使用 Android 的 IdentityCredential / CredMan 系统向移动钱包应用请求身份信息，从而支持 web 原生的凭证流程。针对 SelectParserRelaxation 的弃用试验为依赖旧解析行为的网站提供了一个临时的可选机制，以恢复旧解析。两个试验共同帮助开发者采用新兴的安全凭证集成，同时为与解析器相关的回归提供受控的迁移路径。

## 详细更新

以下条目扩展了上述摘要，并描述了参与这些 origin trials 的开发者的实际影响。

### Digital Credential API (数字凭证 API)

#### 新增内容
网站可以通过实现 Digital Credential API 的 origin trial 从移动钱包应用请求身份信息；该功能利用 Android 的 IdentityCredential / CredMan 系统并具有可扩展性。

#### 技术细节
该试验暴露了一个面向 Web 的 API，将网站与移动钱包凭证连接起来，而无需依赖临时机制（自定义 URL 处理器、二维码扫描）。试验中的实现说明参考了 Android 的 IdentityCredential 与 CredMan 集成，并指向 WICG 规范以了解 API 语义。

#### 适用场景
- 从用户钱包无缝检索凭证以用于登录或身份验证流程。
- 用标准化的 Web API 替换定制的钱包集成（二维码、URL 处理器）。
- 在更广泛发布前测试与 Android 钱包实现的互操作性。

#### 参考资料
- [跟踪错误 #40257092](https://issues.chromium.org/issues/40257092)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5166035265650688)  
- [规范](https://wicg.github.io/digital-credentials)

### Deprecation trial for `SelectParserRelaxation` (SelectParserRelaxation 弃用试验)

#### 新增内容
一个弃用 origin trial 重新启用了旧的 `<select>` 解析行为，即不受支持的内容会被静默丢弃且不会作为 `<select>` 的子项出现在 DOM 中。

#### 技术细节
该试验将 `<select>` 元素的解析行为切换回旧模式，以缓解因较新的解析语义引入的破坏性更改。此试验旨在作为受到近期 Chrome 版本行为更改影响的网站的临时兼容性措施。

#### 适用场景
- 对依赖旧的 `<select>` 解析语义的网站的短期缓解措施。
- 为将服务器端或作者端标记更新为符合新解析行为提供时间。
- 在完全弃用前用于测试和发布计划，以确定兼容性影响。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5145948356083712)
