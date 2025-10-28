---
layout: default
title: webapi-zh
---

## 详细更新

以下细节将上述高层主题与开发者应跟踪并采用的具体更改联系起来。

### Dispatch click events to captured pointer（将 click 事件派发到被捕获的指针目标）

#### 新增内容
当在派发 `pointerup` 期间指针被捕获时，产生的 `click` 事件现在派发到捕获目标，而不是 `pointerdown` 和 `pointerup` 目标的最近公共祖先。

#### 技术细节
行为已更改为在指针捕获生效时遵循 UI Events spec 关于 click 目标解析的语义；未捕获的指针保留先前的 click 目标行为。

#### 适用场景
对使用指针捕获的组件（自定义拖放、绘图工具）提供更可预测的交互处理，避免在捕获期间出现令人惊讶的 click 路由。

#### 参考资料
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=40851596)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5045063816396800)
- [Link](https://w3c.github.io/uievents/#event-type-click)

### Explicit compile hints with magic comments（通过魔法注释提供显式编译提示）

#### 新增内容
JavaScript 文件可以包含编码了应当被 eager-parse 或 eager-compile 的函数的魔法注释。

#### 技术细节
该功能提供了一种随源文件内联附加编译提示的方式，使引擎（V8）能在解析/编译阶段使用这些提示，以减少预热或解析开销。

#### 适用场景
大型 JS 代码库和库可以在不更改运行时代码的情况下引导对性能关键函数进行 eager 编译；有助于启动性能调优。

#### 参考资料
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=13917)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5047772830048256)
- [GitHub](https://github.com/v8/v8/wiki/Design-Elements#compile-hints)

### Incorporate navigation initiator into the HTTP cache partition key（将导航发起者并入 HTTP 缓存分区键）

#### 新增内容
Chrome 的 HTTP 缓存键现在在分区键中包含一个 `is-cross-site-main-frame-navigation` 布尔值。

#### 技术细节
缓存键的更改根据导航是否为跨站点顶级发起者区分响应，从而关闭通过缓存探测进行跨站点信息泄露的一个向量。

#### 适用场景
改进依赖缓存语义的网站的隐私和安全；开发者应注意缓存行为可能根据导航发起者而变化，并据此规划缓存预期。

#### 参考资料
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5108419906535424)
- [Link](https://httpwg.org/specs/rfc9110.html#caching)

### Protected audience: text conversion helpers（受保护受众：文本转换辅助函数）

#### 新增内容
添加了专用辅助函数，用于在 Protected Audience 的出价/评分场景中高效地在字符串与字节数组之间相互转换，以便与 WebAssembly 内存交互。

#### 技术细节
这些独立函数旨在避免临时性转换并为 JS 字符串数据与 Protected Audience 脚本使用的 WASM 线性内存缓冲区之间提供高效互操作性。

#### 适用场景
在 WebAssembly 中运行并必须与 JS 交换字符串类型数据的广告与隐私保护出价/评分流程，可避免昂贵的手动编码/解码。

#### 参考资料
- [ChromeStatus.com entry](https://chromestatus.com/feature/5099738574602240)

### RegExp.escape

#### 新增内容
引入了 `RegExp.escape`，一个静态方法，返回对字符串进行转义后的版本，可安全用作正则表达式模式。

#### 技术细节
该方法对正则元字符进行转义，以便不受信任或用户提供的字符串可以嵌入到 `RegExp` 构造函数中而不改变模式语义。

#### 适用场景
从用户输入（搜索框、模式构建器）安全构建动态正则表达式而无需手动转义；降低意外的正则语法注入风险。

#### 参考资料
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074350768316416)
- [Link](https://tc39.es/proposal-regex-escaping/)

### Speculation rules: tag field（Speculation rules：tag 字段）

#### 新增内容
Speculation rules 现在可以包含可选的 `tag` 字段，用以标记推测规则的来源或目的。

#### 技术细节
附加到 speculation rules 的标签通过 `Sec-Speculation-Tags` 头传输，允许中间件或服务器基于来源对推测请求进行不同处理。

#### 适用场景
更好地观测和路由 prerender/prefetch 推测流量，允许中间件和服务器按标签应用策略或日志记录。

#### 参考资料
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=381687257)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5100969695576064)
- [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-tag)

### Update ProgressEvent to use double type for loaded and total（将 ProgressEvent 的 loaded 与 total 更新为 double 类型）

#### 新增内容
`loaded` 和 `total` 属性的类型从 `unsigned long long` 更改为 `double`。

#### 技术细节
使用 `double` 允许以浮点语义表示小数和非常大的值，符合 Web 开发者对进度报告的预期表示方式。

#### 适用场景
在 XHR/Fetch 进度处理器中支持更精确的进度报告（小数、部分单位），并使实现能够适应长时间传输或聚合进度计算。

#### 参考资料
- [ChromeStatus.com entry](https://chromestatus.com/feature/5084700244254720)
- [Spec](https://xhr.spec.whatwg.org/#interface-progressevent)

文件保存位置（按规范）： digest_markdown/webplatform/Web API/chrome-136-stable-en.md
