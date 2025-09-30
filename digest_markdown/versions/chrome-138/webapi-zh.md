---
layout: default
title: webapi-zh
---

## 领域摘要

Chrome 138 在 Web API 领域强调内置的语言和 AI 辅助能力（Translator、Language Detector、Summarizer），以及对平台的强化和对 service worker 与报告机制的生命周期改进。最具影响力的更改允许开发者利用浏览器提供的翻译/检测/摘要模型，避免随附大型 ML 工件；同时，安全与可靠性改进（属性序列化转义、更丰富的崩溃报告、以及推送订阅生命周期事件）减少了攻击面并改善了诊断能力。总体而言，这些更新通过暴露原生语言模型服务、收紧序列化行为以缓解 mutation XSS，并使推送与崩溃报告语义对开发者更具可操作性，从而推动了 Web 平台的进展。这些更新重要，因为它们改善了开发者体验、用户隐私/性能的权衡，以及整体平台的弹性。

## 详细更新

以下条目在上文摘要基础上提供简明、面向开发者的细节。

### Translator API（翻译器 API）

#### 新增内容
一个 JavaScript API，为网页提供语言翻译能力，将浏览器级的翻译功能暴露给开发者。

#### 技术细节
通过 Web API 暴露翻译功能，使页面在不打包模型的情况下请求翻译。相关于 webapi 和 javascript 领域；链接指向 MDN、跟踪 bug、ChromeStatus 和 WICG 规范。

#### 适用场景
在内置浏览器翻译不足或站点需要可控的翻译工作流时，对用户生成内容或 UI 文本进行按需翻译。

#### 参考资料
- https://developer.mozilla.org/docs/Web/API/Translator
- https://bugs.chromium.org/p/chromium/issues/detail?id=322229993
- https://chromestatus.com/feature/5652970345332736
- https://wicg.github.io/translation-api/

### Language Detector API（语言检测器 API）

#### 新增内容
一个用于检测文本语言的 JavaScript API，返回置信度以辅助后续操作。

#### 技术细节
提供独立于翻译的语言检测功能，旨在与翻译或其他流程结合使用。相关于 webapi 与 javascript 的集成点；提供规范和状态链接。

#### 适用场景
自动确定输入语言以用于自动翻译、路由或分析；在调用 Translator API 之前作为预检步骤。

#### 参考资料
- https://developer.mozilla.org/docs/Web/API/LanguageDetector
- https://chromestatus.com/feature/5134901000871936
- https://wicg.github.io/language-detection-api/

### Summarizer API（摘要器 API）

#### 新增内容
一个由浏览器支持的 AI 语言模型提供支持的 JavaScript API，可生成输入文本的摘要。

#### 技术细节
浏览器通过 Summarizer API 暴露设备/操作系统提供的语言模型，使站点可以在无需各自下载大型模型的情况下对内容进行摘要。设计细节见规范和跟踪条目。

#### 适用场景
在客户端对文章、消息或用户生成内容进行摘要，用于预览、无障碍或类似助手的功能，同时降低网络/模型加载成本。

#### 参考资料
- https://developer.mozilla.org/docs/Web/API/Summarizer
- https://bugs.chromium.org/p/chromium/issues/detail?id=351744634
- https://chromestatus.com/feature/5134971702001664
- https://wicg.github.io/summarization-api/

### Escape < and > in attributes on serialization（在序列化时转义属性中的 < 和 >）

#### 新增内容
在 HTML 序列化过程中转义属性值中的 `<` 和 `>`，以缓解 mutation XSS 风险。

#### 技术细节
序列化现在确保属性值中的 `<` 和 `>` 字符被转义，以防在序列化并重新解析后被误解为起始标签标记。此更改与 HTML 规范中对片段序列化的规定一致，是一项与安全相关的安全强化措施，影响安全-隐私和解析行为。

#### 适用场景
在应用序列化 DOM 片段或设置可能被重新解析或注入的属性时，减少一类 mutation XSS 问题。

#### 参考资料
- https://chromestatus.com/feature/5125509031477248
- https://html.spec.whatwg.org/multipage/parsing.html#serializing-html-fragments

### Crash Reporting API: is_top_level and visibility_state（崩溃报告 API：is_top_level 与 visibility_state）

#### 新增内容
在发送到默认报告端点的崩溃报告负载中添加字符串字段 `is_top_level` 和 `visibility_state`。

#### 技术细节
崩溃报告正文现在包含这些额外的上下文字段，以便更好地理解崩溃情境。此更改影响报告语义和后端诊断；有关预期字段的详情见 reporting 规范和 ChromeStatus 条目。

#### 适用场景
通过提供可见性上下文和顶层帧状态，改善服务器端崩溃分析和客户端分拣，有助于调试和优先级排序。

#### 参考资料
- https://chromestatus.com/feature/5112885175918592
- https://w3c.github.io/reporting/#crash-report

### Fire the pushsubscriptionchange event upon resubscription（在重新订阅时触发 pushsubscriptionchange 事件）

#### 新增内容
当先前有订阅的源再次被授予通知权限时，service worker 将触发 `pushsubscriptionchange` 事件；在这种情况下，该事件会以空的 `oldSubscription` 派发。

#### 技术细节
此行为更改使在权限发生转换（granted → denied/default → granted）时推送订阅的生命周期更加明确。它遵循 Push API 规范中 `pushsubscriptionchange` 事件的语义，并影响 pwa-service-worker 与权限处理流程。

#### 适用场景
当权限被重新授予时，允许 service worker 重新订阅或对齐推送状态，从而实现可靠的推送恢复并改进开发者对权限波动的处理。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=407523313
- https://chromestatus.com/feature/5115983529336832
- https://w3c.github.io/push-api/#the-pushsubscriptionchange-event
