---
layout: default
title: chrome-133-zh
---

## 领域摘要

Chrome 133 带来一组聚焦的 CSS 平台改进，侧重于更丰富的样式表达、新的选择器与查询能力、更细粒度的文本布局控制，以及动画进度的可检视性。对开发者影响最大的更改包括 CSS Level 5 的 `attr()` 扩展（可在任何属性中使用的类型化属性值）、基于滚动状态的容器查询、`:open` 伪类，以及新的 text-box 对齐属性——这些都使得更声明式、组件友好的样式成为可能。上述特性通过减少基于 JavaScript 的变通方案、启用响应式的容器驱动样式，并为设计师提供更精细的布局与动画控制，从而推动 Web 平台演进。构建组件库、设计系统或以动画为主的 UI 的团队应评估这些 API 以便简化实现并提升性能。

## 详细更新

下面列出 Chrome 133 中与 CSS 领域相关的更改，包含简明的技术说明、实际用途以及指向参考资料的链接。

### CSS advanced `attr()` function

#### 新增内容
实现了 CSS Level 5 对 `attr()` 的扩展，允许除 `<string>` 之外的类型，并允许在所有 CSS 属性中使用 `attr()`（不再仅限于伪元素 `content`）。

#### 技术细节
`attr()` 现在支持 CSS Values 5 记法中的类型化值，并且可以在样式表的属性值中进行插值使用。

#### 适用场景
使用类型化的属性值来驱动组件的属性值，减少用于简单基于属性的样式的 JS，且在 Web 组件中启用属性到样式的数据流。

#### 参考资料
- https://developer.mozilla.org/en-US/docs/Web/CSS/attr
- https://issues.chromium.org/issues/246571
- https://chromestatus.com/feature/4680129030651904
- https://drafts.csswg.org/css-values-5/#attr-notation

### CSS `:open` pseudo-class

#### 新增内容
添加了 `:open` 伪类，用于匹配打开的 `<dialog>`、`<details>`，以及显示选择器或拾取器的 `<select>` / `<input>`。

#### 技术细节
按照 Selectors Level 4 的规范，实现了用于匹配打开/拾取器可见状态的选择器级别状态匹配。

#### 适用场景
在不使用脚本的情况下，直接为原生控件和可展开元素在打开或显示拾取器时设置样式。

#### 参考资料
- https://issues.chromium.org/issues/324293874
- https://chromestatus.com/feature/5085419215781888
- https://drafts.csswg.org/selectors-4/#open-state

### CSS scroll state container queries

#### 新增内容
容器查询现在可以基于容器的滚动状态来定位后代元素（例如，当容器是滚动容器或受滚动容器影响时）。

#### 技术细节
查询容器可为滚动容器或受滚动容器位置影响的元素；可查询的特定滚动相关状态（例如 `stuck`）遵循条件规则草案。

#### 适用场景
在不使用 JS 的情况下，根据滚动驱动的状态（粘性行为、滚动偏移）调整后代样式。

#### 参考资料
- https://issues.chromium.org/issues/40268059
- https://chromestatus.com/feature/5072263730167808
- https://www.w3.org/TR/css-conditional-5/#scroll-state-container

### CSS `text-box`, `text-box-trim`, and `text-box-edge`

#### 新增内容
引入了 `text-box-trim`、`text-box-edge` 以及 `text-box` 速记属性，以提供更细粒度的垂直文本对齐和修剪控制，从而实现更佳的文本平衡。

#### 技术细节
这些属性允许指定要修剪的侧（上方/下方）并定义文本框边缘行为，详见内联布局草案中的描述。

#### 适用场景
在以排版为重的布局中改进垂直节奏与对齐，微调基线/修剪行为以适应紧凑的 UI 文本流。

#### 参考资料
- https://issues.chromium.org/issues/1411581
- https://chromestatus.com/feature/5174589850648576
- https://drafts.csswg.org/css-inline-3/#text-edges

### `Animation.overallProgress`

#### 新增内容
新增 `overallProgress`，提供一个在各次迭代之间并不依赖时间线差异的一致动画进度表示。

#### 技术细节
`overallProgress` 把动画的累积进度暴露出来，使开发者无需手动计算相对于迭代的进度或处理时间线的特殊情况。

#### 适用场景
简化动画与 JS 逻辑之间的同步，基于单一规范化的进度度量驱动 UI 状态或效果。

#### 参考资料
- https://issues.chromium.org/issues/40914396
- https://chromestatus.com/feature/5083257285378048
- https://drafts.csswg.org/web-animations-2/#the-overall-progress-of-an-animation

### The `pause()` method of the `Atomics` object

#### 新增内容
新增 `Atomics.pause()`，用于向 CPU 提示当前代码在执行自旋锁。

#### 技术细节
在 Atomics 命名空间上提供的平台级提示，依照 microwait 提案的说明实现。

#### 适用场景
主要对低级并发模式有利；在多线程 JS 场景（如 WebWorkers）中的自旋等待期间可能降低 CPU 使用率。

#### 参考资料
- https://chromestatus.com/feature/5106098833719296
- https://tc39.es/proposal-atomics-microwait

### CSP hash reporting for scripts

#### 新增内容
新增用于上报脚本哈希的机制，帮助 Web 应用跟踪其下载并执行的子资源以满足安全/审计需求。

#### 技术细节
引入与 CSP 机制相关联的上报钩子（参见跟踪错误和 ChromeStatus 条目）。

#### 适用场景
用于合规与已加载脚本的清单跟踪，有助于安全审计以及像 PCI-DSS v4 这样的标准要求。

#### 参考资料
- https://issues.chromium.org/issues/377830102
- https://chromestatus.com/feature/6337535507431424

### DOM state-preserving move

#### 新增内容
引入 `Node.prototype.moveBefore`，用于在 DOM 中移动元素而不重置元素状态。

#### 技术细节
移动操作会保留元素状态，例如已加载的 `<iframe>` 内容和活动焦点，而不是执行移除并插入的流程。

#### 适用场景
在需要保留元素状态（如 iframe、媒体播放、焦点）且不希望导致重新加载或丢失状态的 UI 重排场景中使用。

#### 参考资料
- https://chromestatus.com/feature/5135990159835136

### Expose `attributionsrc` attribute on `<area>`

#### 新增内容
在 `<area>` 上公开 `attributionsrc` 属性，使 DOM 的暴露与现有处理行为保持一致。

#### 技术细节
该属性在 `<area>` 上可用，以符合浏览器的处理方式并将 `<area>` 视为导航面。

#### 适用场景
在图像映射区域上启用归因上报语义，并在导航元素间保持一致的属性访问。

#### 参考资料
- https://issues.chromium.org/issues/379275911
- https://chromestatus.com/feature/6547509428879360
- https://wicg.github.io/attribution-reporting-api/#html-monkeypatches

### The `FileSystemObserver` interface

#### 新增内容
新增 `FileSystemObserver` 接口，用于在用户授予权限的文件和目录发生变化时通知站点。

#### 技术细节
观察者可以监视本地设备文件系统或跟踪条目中提到的 Bucket File System / Origin Private File System 的更改。

#### 适用场景
为反映本地文件更改的应用提供响应式 UI，同步客户端或使用原点私有文件存储的编辑器。

#### 参考资料
- https://issues.chromium.org/issues/40105284
- https://chromestatus.com/feature/4622243656630272

### Multiple import maps

#### 新增内容
允许每个文档使用多个 import map，而不是在任何模块加载之前只使用单个 import map，从而解决脆弱性和排序问题。

#### 技术细节
支持模块化的 import map 使用，以避免单个大型阻塞性 import map，并在模块提前加载时提高健壮性。

#### 适用场景
大型模块化应用可以从多个来源组合 import map，改善弹性和加载顺序控制。

#### 参考资料
- https://chromestatus.com/feature/5121916248260608

### Storage Access Headers

#### 新增内容
新增头部以允许已认证的嵌入内容选择加入非分区 Cookie，并指示请求中是否包含（或可以包含）非分区 Cookie。

#### 技术细节
服务器可以通过这些头部根据隐私组草案来标示并激活先前授予的 `storage-access` 权限。

#### 适用场景
简化需要访问非分区 Cookie 的已认证第三方嵌入流程，同时与隐私约束保持一致。

#### 参考资料
- https://issues.chromium.org/issues/329698698
- https://chromestatus.com/feature/6146353156849664
- https://privacycg.github.io/storage-access-headers

### Support creating `ClipboardItem` with `Promise<DOMString>`

#### 新增内容
`ClipboardItem` 构造函数现在接受字符串值以及解析为 Blob 或字符串的 Promise 作为 `ClipboardItemData`。

#### 技术细节
异步剪贴板的 `write()` 输入现在可以由解析为字符串或 Blob 的 Promise 支持，符合 Clipboard APIs 规范。

#### 适用场景
在异步准备文本内容后写入剪贴板时，使剪贴板写入操作更灵活。

#### 参考资料
- https://issues.chromium.org/issues/40766145
- https://chromestatus.com/feature/4926138582040576
- https://www.w3.org/TR/clipboard-apis/#typedefdef-clipboarditemdata

### WebAssembly Memory64

#### 新增内容
支持 64 位索引的线性 WebAssembly 内存（大于 2^32 位的 Memory64 提案）。

#### 技术细节
扩展现有的内存/表指令以接受 64 位索引；未引入新指令。

#### 适用场景
使可能与图形或数据密集型应用互操作的大内存 WebAssembly 工作负载成为可能；与高性能的 Web 组件相关。

#### 参考资料
- https://chromestatus.com/feature/5070065734516736
- https://github.com/WebAssembly/memory64/blob/main/proposals/memory64/Overview.md

### Web Authentication API: `PublicKeyCredential` `getClientCapabilities()` method

#### 新增内容
为 `PublicKeyCredential` 添加 `getClientCapabilities()`，用于确定受支持的 WebAuthn 客户端功能。

#### 技术细节
该方法返回受支持的客户端能力列表，以便根据客户端功能定制认证流程。

#### 适用场景
在启动认证流程前检测客户端能力，从而改进认证体验的渐进增强。

#### 参考资料
- https://issues.chromium.org/issues/360327828
- https://chromestatus.com/feature/5128205875544064
- https://w3c.github.io/webauthn/#sctn-getClientCapabilities

### X25519 algorithm of the Web Cryptography API

#### 新增内容
在 SubtleCrypto 中实现了用于密钥协商操作（生成/导入/派生/导出）的 X25519 算法标识。

#### 技术细节
根据 WebCrypto 规范支持 X25519，用于 deriveKey 和 deriveBits 等密钥协商原语。

#### 适用场景
为可能与安全传输或密钥交换集成的安全应用密码学启用现代椭圆曲线密钥协商流程。

#### 参考资料
- https://issues.chromium.org/issues/378856322
- https://chromestatus.com/feature/6291245926973440
- https://w3c.github.io/webcrypto/#x25519

已保存到：digest_markdown/webplatform/CSS/chrome-133-stable-en.md
