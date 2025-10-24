---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 135 带来了多项 Web API 增强，重点提升互操作性、开发者体验、隐私和性能。主要主题包括改进的 service worker 集成、扩展的 DOM 和 JavaScript 能力，以及用于异步编程和用户交互的新 API。值得关注的变化有新增的 `Float16Array`、Observable API，以及导航和高亮检测的更新，这些都让开发者能够构建更具响应性和功能丰富的应用。通过 HSTS 跟踪防护和更精细的 CORS 重定向处理，隐私和安全性也得到了加强。这些更新共同推动了 Web 平台与不断发展的标准接轨，弥合兼容性差距，并为现代 Web 开发启用新的适用场景。

## 详细更新

以下是 Chrome 135 Web API 的详细更新，突出技术细节及对开发者的实际益处。

### Create service worker client and inherit service worker controller for srcdoc iframe

#### 新增内容
Srcdoc iframe 现在作为 service worker 客户端，并继承其父级的 service worker controller，确保资源请求拦截行为一致。

#### 技术细节
此前，srcdoc 文档不受 service worker 控制，导致资源处理不一致。此更新确保 srcdoc iframe 的资源请求由父级的 service worker 拦截，使行为与其他 iframe 类型一致。

#### 适用场景
- 使动态 iframe 的离线和缓存策略保持一致。
- 提高嵌入内容的调试和资源计时准确性。

#### 参考资料
- [跟踪问题 #41411856](https://issues.chromium.org/issues/41411856)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5128675425779712)
- [规范](https://github.com/w3c/ServiceWorker/issues/765)

---

### Element reflection

#### 新增内容
ARIA 关系属性现在在 IDL 中以元素引用的形式反映，而不再是 DOMString。

#### 技术细节
实现了 ARIAMixin 接口，将属性暴露为 `Element` 或 `FrozenArray<Element>`，提升类型安全性和开发体验。

#### 适用场景
- 简化 JavaScript 中 ARIA 属性的操作。
- 增强辅助功能工具和动态 ARIA 更新。

#### 参考资料
- [ARIAMixin](https://w3c.github.io/aria/#ARIAMixin)
- [跟踪问题 #981423](https://issues.chromium.org/issues/981423)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6244885579431936)
- [规范](https://html.spec.whatwg.org/multipage/common-dom-interfaces.html#reflecting-content-attributes-in-idl-attributes:element)

---

### Fenced frames: Automatic beacon cross-origin data support

#### 新增内容
通过特定 API 加载的 fenced frame 现在可自动发送包含跨域数据的报告 beacon。

#### 技术细节
支持 fenced frame 中跨域文档的自动 beacon 报告，超越了仅限顶级导航 beacon 的范围。

#### 适用场景
- 支持隐私保护的广告测量与报告。
- 满足以隐私为中心环境下的高级分析需求。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5121048142675968)
- [规范](https://github.com/WICG/fenced-frame/pull/203)

---

### `Float16Array`

#### 新增内容
引入了 `Float16Array` 类型数组，支持 16 位浮点数。

#### 技术细节
写入时数值会舍入为 IEEE fp16。该功能与最新 ECMAScript 提案保持一致，并提升了图形和机器学习等工作负载的兼容性。

#### 适用场景
- 图形、机器学习和科学数据的高效存储与计算。
- 降低大规模数值数据集的内存占用。

#### 参考资料
- [跟踪问题 #42203953](https://issues.chromium.org/issues/42203953)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5164400693215232)
- [规范](https://tc39.es/proposal-float16array)

---

### HSTS tracking prevention

#### 新增内容
通过仅允许顶级导航升级 HSTS，防止第三方利用 HSTS 缓存进行跟踪。

#### 技术细节
阻止子资源请求的 HSTS 升级，缓解跨站点跟踪风险。

#### 适用场景
- 通过减少指纹识别和跟踪风险提升用户隐私。
- 符合现代 Web 安全最佳实践。

#### 参考资料
- [跟踪问题 #40725781](https://issues.chromium.org/issues/40725781)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5072685886078976)

---

### NavigateEvent sourceElement

#### 新增内容
为 `NavigateEvent` 新增 `sourceElement` 属性，暴露发起导航的元素。

#### 技术细节
当导航由某个元素（如链接或表单）触发时，`sourceElement` 引用该 DOM 元素。

#### 适用场景
- 支持高级导航分析和自定义路由逻辑。
- 便于 SPA 的调试和事件追踪。

#### 参考资料
- [跟踪问题 #40281924](https://issues.chromium.org/issues/40281924)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5134353390895104)
- [规范](https://html.spec.whatwg.org/multipage/nav-history-apis.html#dom-navigateevent-sourceelement)

---

### NotRestoredReasons API reason name change

#### 新增内容
统一 NotRestoredReasons API 的原因文本，与最新规范保持一致。

#### 技术细节
更新页面未从前进/后退缓存恢复的原因名称，使其与 HTML 规范一致。

#### 适用场景
- 简化导航与缓存问题的监控和调试。
- 保证跨浏览器诊断的兼容性。

#### 参考资料
- [跟踪问题 #331754704](https://issues.chromium.org/issues/331754704)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6444139556896768)
- [规范](https://github.com/whatwg/html/pull/10154)

---

### Observable API

#### 新增内容
引入 Observable API，用于处理异步事件流。

#### 技术细节
提供原生 Observable 接口，便于处理多个异步事件，类似于 Promise，但适用于流。

#### 适用场景
- Web 应用中的响应式编程模式。
- 简化事件驱动架构和数据流处理。

#### 参考资料
- [跟踪问题 #1485981](https://issues.chromium.org/issues/1485981)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5154593776599040)
- [规范](https://wicg.github.io/observable)

---

### Remove clamping of `setInterval(...)` to >= 1ms

#### 新增内容
移除了 `setInterval` 最小 1ms 延迟限制，允许零延迟间隔。

#### 技术细节
`setInterval(..., 0)` 现在会产生 0ms 延迟，嵌套调用仍限制为 4ms。

#### 适用场景
- 支持高性能应用的更精细定时。
- 适用于动画循环和实时更新。

#### 参考资料
- [跟踪问题 #41380458](https://issues.chromium.org/issues/41380458)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5072451480059904)

---

### Service Worker client URL ignore `history.pushState()` changes

#### 新增内容
Service worker 的 `Client.url` 属性现在会忽略通过 `history.pushState()` 产生的 URL 变化。

#### 技术细节
`Client.url` 反映文档创建时的 URL，不受后续 history API 变更影响，与 service worker 规范保持一致。

#### 适用场景
- 保证 SPA 中 service worker 行为一致。
- 防止客户端标识和缓存逻辑混淆。

#### 参考资料
- [跟踪问题 #41337436](https://issues.chromium.org/issues/41337436)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4996996949344256)
- [规范](https://www.w3.org/TR/service-workers/#client-url)

---

### Support `rel` and `relList` attributes for `SVGAElement`

#### 新增内容
为 SVG `<a>` 元素添加 `rel` 和 `relList` 属性，对齐 HTML 锚点行为。

#### 技术细节
实现 SVG 2.0 的链接关系特性，增强安全性和隐私控制。

#### 适用场景
- 实现 HTML 与 SVG 间一致的链接管理。
- 支持高级 SVG 导航和安全策略。

#### 参考资料
- [跟踪问题 #40589293](https://issues.chromium.org/issues/40589293)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5066982694846464)
- [规范](https://svgwg.org/svg2-draft/linking.html#__svg__SVGAElement__rel)

---

### Timestamps for RTC Encoded Frames

#### 新增内容
为 WebRTC 编码帧公开捕获和接收时间戳。

#### 技术细节
为通过 RTCPeerConnection 传输的帧提供元数据，包括帧的捕获和接收时间。

#### 适用场景
- 支持精确的媒体同步与诊断。
- 满足实时通信的高级分析需求。

#### 参考资料
- [跟踪问题 #391114797](https://issues.chromium.org/issues/391114797)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6294486420029440)
- [规范](https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-receivetime)

---

### Update HTTP request headers, body, and referrer policy on CORS redirect

#### 新增内容
CORS 重定向行为与 Fetch 规范保持一致，按需更新请求头、请求体和 referrer policy。

#### 技术细节
当重定向导致 HTTP 方法变化时，移除请求体和相关头部，并更新 referrer policy，以提升与其他浏览器的兼容性。

#### 适用场景
- 提升 CORS 请求的跨浏览器兼容性。
- 减少复杂 fetch 场景中的隐性 bug。

#### 参考资料
- [跟踪问题 #40686262](https://issues.chromium.org/issues/40686262)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5129859522887680)
- [规范](https://fetch.spec.whatwg.org/#http-redirect-fetch)

---

### fetchLater API

#### 新增内容
引入 `fetchLater()`，允许开发者调度延迟的 fetch 请求。

#### 技术细节
延迟请求会被排队，并在文档销毁或指定时间后执行，兼顾隐私考量。

#### 适用场景
- 支持后台数据预取和延迟分析。
- 提升资源加载的性能与隐私。

#### 参考资料
- [跟踪问题 #1465781](https://issues.chromium.org/issues/1465781)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4654499737632768)
- [规范](https://whatpr.org/fetch/1647/07662d3...139351f.html)

---

### highlightsFromPoint API

#### 新增内容
新增 `highlightsFromPoint` API，可检测文档指定点的自定义高亮。

#### 技术细节
支持查询高亮覆盖层，包括 shadow DOM 内的高亮，实现精确的用户交互。

#### 适用场景
- 支持高级文本选择、注释和辅助功能。
- 适用于编辑器、阅读器和协作工具。

#### 参考资料
- [跟踪问题 #365046212](https://issues.chromium.org/issues/365046212)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4552801607483392)
- [规范](https://drafts.csswg.org/css-highlight-api-1/#interactions)
