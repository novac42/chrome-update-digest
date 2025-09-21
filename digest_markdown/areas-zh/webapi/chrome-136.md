---
layout: default
title: Chrome 136 稳定版发布 - Web API 分析
---

# Chrome 136 稳定版发布 - Web API 分析

## 区域摘要

Chrome 136 为 Web API 功能引入了重大增强，专注于开发者生产力、安全性改进和平台一致性。主要亮点包括用于更安全正则表达式处理的新 `RegExp.escape` 实用程序、用于更好触摸交互的指针事件改进，以及通过显式编译提示进行的 JavaScript 编译优化。此版本还通过 HTTP 缓存分区更新加强了安全性，并通过 ProgressEvent 改进增强了性能跟踪能力。这些更新通过为开发者提供对应用程序行为的更精确控制，同时保持向后兼容性，共同推进了 Web 平台的发展。

## 详细更新

此版本带来了几项重要的 Web API 增强，改善了开发者体验和应用程序安全性，涵盖从基础 JavaScript 实用程序到高级性能优化的各个方面。

### RegExp.escape

#### 新增功能
新的静态方法 `RegExp.escape`，可安全地转义字符串用作正则表达式模式，消除了手动转义的需要并减少了安全漏洞。

#### 技术细节
该方法接受任何字符串输入，返回所有特殊正则表达式字符都经过正确转义的版本。这确保用户输入或动态内容可以安全地合并到正则表达式中，而不会出现意外的模式匹配行为。

#### 使用场景
对于从用户输入构造正则表达式的应用程序、搜索功能和模板系统至关重要。对于防止正则表达式注入攻击和确保可预测的模式匹配行为特别有价值。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5074350768316416)
- [规范](https://tc39.es/proposal-regex-escaping/)

### Dispatch click events to captured pointer

#### 新增功能
当在 `pointerup` 事件期间指针捕获处于活动状态时，点击事件现在能正确分发到捕获的指针目标，使 Chrome 的行为与 UI 事件规范保持一致。

#### 技术细节
当在指针交互期间调用 `setPointerCapture()` 时，后续点击事件将发送到捕获的元素，而不是遵循默认的目标逻辑。这确保了不同交互模式下事件处理的一致性。

#### 使用场景
对于拖放界面、自定义 UI 控件和需要精确事件目标定位的基于触摸的应用程序至关重要。提高了复杂 Web 应用程序中基于指针交互的可靠性。

#### 参考资料
- [跟踪错误 #40851596](https://bugs.chromium.org/p/chromium/issues/detail?id=40851596)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5045063816396800)
- [规范](https://w3c.github.io/uievents/#event-type-click)

### Update ProgressEvent to use double type for loaded and total

#### 新增功能
ProgressEvent 的 `loaded` 和 `total` 属性现在使用 `double` 类型而不是 `unsigned long long`，提供更精确的进度报告能力。

#### 技术细节
此更改允许小数进度值，消除了仅限整数进度报告的限制。开发者现在可以以小数精度报告进度，实现更准确的进度指示器。

#### 使用场景
有利于文件上传/下载进度条、流式操作以及任何需要细粒度进度报告的场景。对于需要字节级精度的大文件传输特别有用。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5084700244254720)
- [规范](https://xhr.spec.whatwg.org/#interface-progressevent)

### Explicit compile hints with magic comments

#### 新增功能
JavaScript 文件现在可以包含魔术注释，为 V8 引擎提供关于哪些函数应该急切解析和编译的提示，优化初始加载性能。

#### 技术细节
开发者可以使用特殊注释来注解其 JavaScript 代码，指导编译过程。这允许在脚本解析期间进行更智能的资源分配，并可以减少关键代码路径的初始执行延迟。

#### 使用场景
对于选择性编译可以改善启动性能的大型 JavaScript 应用程序很有价值。对于具有复杂初始化序列的框架、库和应用程序特别有用。

#### 参考资料
- [跟踪错误 #13917](https://bugs.chromium.org/p/chromium/issues/detail?id=13917)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5047772830048256)
- [规范](https://github.com/v8/v8/wiki/Design-Elements#compile-hints)

### Incorporate navigation initiator into the HTTP cache partition key

#### 新增功能
Chrome 的 HTTP 缓存现在在其分区方案中包含导航发起者信息，以防止通过顶级导航缓存探测进行的跨站点时序攻击。

#### 技术细节
缓存键现在包含一个 `is-cross-site-main-frame-navigation` 布尔值，该值根据导航上下文隔离缓存条目。这防止攻击者使用缓存时序来推断用户在不同站点间的浏览历史信息。

#### 使用场景
通过防止复杂的基于时序的攻击，增强所有 Web 应用程序的隐私和安全性。对于处理敏感数据或在高安全环境中运行的应用程序特别重要。

#### 参考资料
- [跟踪错误 #398784714](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5108419906535424)
- [规范](https://httpwg.org/specs/rfc9110.html#caching)

### Speculation rules: tag field

#### 新增功能
推测规则现在可以包含可选的 `tag` 字段，允许开发者对不同的预加载提示来源进行分类和跟踪，标签通过 `Sec-Speculation-Tags` 头部发送。

#### 技术细节
标签字段通过允许开发者识别哪些规则被触发以及它们的性能表现，实现更好的推测规则性能分析和调试。标签会自动包含在相关的 HTTP 头部中以便服务器端处理。

#### 使用场景
对于跟踪不同预加载策略有效性的性能优化团队至关重要。用于 A/B 测试推测规则和了解复杂应用程序中的导航模式。

#### 参考资料
- [跟踪错误 #381687257](https://bugs.chromium.org/p/chromium/issues/detail?id=381687257)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5100969695576064)
- [规范](https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-tag)

### Protected audience: text conversion helpers

#### 新增功能
Protected Audience 竞价和评分脚本现在可以访问专门的辅助函数，用于在与 WebAssembly 模块接口时高效地在字符串和字节数组之间转换。

#### 技术细节
这些函数，`protectedAudience.textEncoder` 和相关实用程序，在隐私保护广告上下文中为数据转换提供优化路径。它们专门设计为与 WebAssembly 的内存模型高效配合工作。

#### 使用场景
对于使用 WebAssembly 组件实现 Privacy Sandbox API 的广告商和发布商至关重要。在保持隐私保证的同时实现更高效的广告拍卖处理。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5099738574602240)