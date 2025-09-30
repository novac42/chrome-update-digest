## 区域摘要

Chrome 138 (stable) 通过将内置的语言和 AI 辅助文本能力（Translator、Language Detector、Summarizer）标准化，同时收紧序列化安全性并改进运行时诊断和推送订阅行为，扩展了 Web API 面。对开发者影响最大的变更是原生语言处理 API，减少了站点端大型模型的需求，以及改进的平台级别安全和可观测性。这些更新将更多常见任务（翻译、检测、摘要、安全序列化、崩溃上下文、推送重新订阅）的责任推向浏览器，简化了 Web 应用的实现并提升了终端用户的隐私与可靠性。

## 详细更新

以下条目扩展了上文摘要，并概述了此发行版中每个 Web API 特性对开发者的影响。

### Translator API（翻译能力）

#### 新增内容
一个 JavaScript API，向网页公开语言翻译能力，使页面能够请求来自浏览器提供的翻译能力。

#### 技术细节
浏览器提供的翻译通过 Web API 暴露，使开发者能够在不捆绑模型或仅依赖浏览器 UI 的情况下集成翻译流程。（有关实现细节，请参阅规范和跟踪链接。）

#### 适用场景
对页面上的用户内容进行翻译、本地化输入处理，或在内置浏览器翻译不可用时增强 UI。

#### 参考资料
- MDN 文档: https://developer.mozilla.org/docs/Web/API/Translator
- “跟踪 bug #322229993”: https://bugs.chromium.org/p/chromium/issues/detail?id=322229993
- ChromeStatus.com 条目: https://chromestatus.com/feature/5652970345332736
- 规范: https://wicg.github.io/translation-api/

### Language Detector API（语言检测能力）

#### 新增内容
一个 JavaScript API，用于检测输入文本的语言并返回置信度，旨在补充翻译工作流。

#### 技术细节
语言检测作为浏览器 API 暴露，页面可以以编程方式确定输入语言，并将检测与翻译或路由逻辑结合使用。

#### 适用场景
自动检测用户输入语言以选择翻译目标、用于分析，或在语言未知时调整 UI。

#### 参考资料
- MDN 文档: https://developer.mozilla.org/docs/Web/API/LanguageDetector
- ChromeStatus.com 条目: https://chromestatus.com/feature/5134901000871936
- 规范: https://wicg.github.io/language-detection-api/

### Summarizer API（摘要能力）

#### 新增内容
一个 JavaScript API，用于生成输入文本的摘要，由浏览器内或操作系统提供的语言模型支持，减少站点需要部署大型模型的需求。

#### 技术细节
该 API 通过浏览器暴露摘要能力，使站点可以请求简明摘要而无需嵌入大型模型工件；有关行为和安全考量，请参阅规范和跟踪链接。

#### 适用场景
为长篇文章生成摘要、为用户提供内容预览，或将摘要工作从服务器端下放到客户端/浏览器。

#### 参考资料
- MDN 文档: https://developer.mozilla.org/docs/Web/API/Summarizer
- “跟踪 bug #351744634”: https://bugs.chromium.org/p/chromium/issues/detail?id=351744634
- ChromeStatus.com 条目: https://chromestatus.com/feature/5134971702001664
- 规范: https://wicg.github.io/summarization-api/

### Escape < and > in attributes on serialization（在序列化时在属性中转义 < 和 >）

#### 新增内容
属性值在序列化时将把 `<` 和 `>` 转义，以缓解在序列化的属性可能被重新解析为 start-tag 标记时的变异型 XSS 风险。

#### 技术细节
序列化算法现在根据 HTML 解析/序列化规范，在属性值内部转义 `<` 和 `>`，以降低当内容被重新序列化并重新解析时由属性驱动的注入风险。

#### 适用场景
通过防止某些变异型 XSS 向量，提升 DOM 序列化操作（例如类似 innerHTML 的流程、HTML 片段生成）的安全性。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5125509031477248
- 规范: https://html.spec.whatwg.org/multipage/parsing.html#serializing-html-fragments

### Crash Reporting API: is_top_level and visibility_state（崩溃报告 API：is_top_level 与 visibility_state）

#### 新增内容
向发送到默认崩溃报告端点的崩溃报告主体添加字符串字段 `is_top_level` 和 `visibility_state`。

#### 技术细节
这些字段提供在生成崩溃报告时关于页面的额外运行时上下文，遵循崩溃报告的 reporting 规范扩展。

#### 适用场景
为诊断和分流提供更丰富的崩溃上下文（例如崩溃是否发生在顶级页面以及文档的可见性状态），有助于可靠性工程和调试。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5112885175918592
- 规范: https://w3c.github.io/reporting/#crash-report

### Fire the pushsubscriptionchange event upon resubscription（在重新订阅时触发 pushsubscriptionchange 事件）

#### 新增内容
当先前具有推送订阅的来源在被撤销后再次授予通知权限时，service worker 将收到一个 `pushsubscriptionchange` 事件，事件中 `oldSubscription` 为空，当前订阅作为 `newSubscription` 提供。

#### 技术细节
此行为确保 service worker 在由于权限转换导致的订阅生命周期更改时得到通知，与 Push API 规范保持一致。

#### 适用场景
帮助具备推送功能的应用在权限更改后检测重新订阅情形并更新服务器端订阅记录或重新向推送服务注册。

#### 参考资料
- “跟踪 bug #407523313”: https://bugs.chromium.org/p/chromium/issues/detail?id=407523313
- ChromeStatus.com 条目: https://chromestatus.com/feature/5115983529336832
- 规范: https://w3c.github.io/push-api/#the-pushsubscriptionchange-event

Saved to digest_markdown/webplatform/Web API/chrome-138-stable-en.md