---
layout: default
title: Chrome 144 Stable - JavaScript 更新
---

# Chrome 144 Stable - JavaScript 更新

## 领域摘要

Chrome 144 带来了重要的 JavaScript 增强功能，专注于现代化日期/时间处理、改进 SVG/HTML API 一致性，以及扩展剪贴板交互能力。最突出的新增功能是 Temporal API，这是对 JavaScript 长期存在问题的 Date 对象的全面替代方案，为开发者提供了强大、现代的时间操作基础。其他更新通过改进的 SVG 元素支持增强了跨平台兼容性，加强了 RTL 语言的 MathML 渲染，并引入了剪贴板监控能力，为远程桌面客户端等 Web 应用程序实现高级同步场景。

## 详细更新

Chrome 144 的 JavaScript 改进涵盖基础语言特性、DOM API 一致性和专业渲染能力，反映了平台在功能完整性和跨规范对齐方面的持续演进。

### Temporal in ECMA262

#### 新增内容

Temporal API 为 JavaScript 中的日期和时间处理引入了现代化的综合解决方案，解决了传统 Date 对象长期存在的痛点。Temporal 提供了一个新的全局命名空间（类似于 Math），包含专为精确、时区感知的时间操作设计的标准对象和函数。

#### 技术细节

Temporal 用一套针对不同时间概念的专用类型替代了有问题的 Date API：Instant（时间上的固定点）、ZonedDateTime（带时区）、PlainDate、PlainTime、PlainDateTime、Duration 和 Calendar。该 API 在设计上是不可变的，避免了 Date 的修改陷阱，并提供对时区、日历和时间运算的显式处理。所有操作都根据 ECMA262 规范精确定义。

#### 适用场景

开发者现在可以自信地处理复杂的日期/时间场景：跨时区调度、日历感知的日期运算（考虑夏令时转换）、精确的持续时间计算以及特定于区域的日期格式化。不可变的设计防止了与意外日期修改相关的常见错误。需要可靠时间逻辑的应用程序（如预订系统、日历应用或国际调度工具）可以从 Temporal 的强大基础中受益。

#### 参考资料

- [跟踪错误 #detail?id=11544](https://issues.chromium.org/issues/detail?id=11544)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5668291307634688)
- [规范](https://tc39.es/proposal-temporal/)

### Support `ping`, `hreflang`, `type`, and `referrerPolicy` for `SVGAElement`

#### 新增内容

Chrome 144 为 `SVGAElement` 添加了对 `ping`、`hreflang`、`type` 和 `referrerPolicy` 属性的支持，使 SVG 锚元素与其 HTML 对应元素保持一致，在两种标记语言中实现一致的链接行为。

#### 技术细节

以前，`SVGAElement` 缺少 `HTMLAnchorElement` 上可用的几个属性，在 SVG 上下文中使用链接时会产生不一致性。此更新实现了 `ping` 属性（用于链接跟踪端点）、`hreflang`（指示链接资源的语言）、`type`（MIME 类型提示）和 `referrerPolicy`（控制请求发送的 referrer 信息）。这些添加确保 SVG 链接在导航元数据和隐私控制方面与 HTML 链接的行为完全相同。

#### 适用场景

构建基于 SVG 的交互式图形、数据可视化或混合 HTML/SVG 界面的开发者现在可以应用统一的链接处理模式。使用 `ping` 属性的分析实现可以在 HTML 和 SVG 链接中保持一致。国际化应用程序可以正确地为 SVG 链接添加语言信息注释，隐私意识强的网站可以在所有链接类型中统一执行 referrer 策略。

#### 参考资料

- [跟踪错误 #40589293](https://issues.chromium.org/issues/40589293)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5140707648077824)
- [规范](https://svgwg.org/svg2-draft/linking.html#InterfaceSVGAElement)

### Mirroring of RTL MathML operators

#### 新增内容

Chrome 144 在右到左（RTL）模式下渲染时，为 MathML 运算符实现了字符级和字形级镜像，确保在 RTL 语言上下文中正确显示数学符号。

#### 技术细节

该实现处理两种镜像策略：字符级镜像使用 Unicode 的 `Bidi_Mirrored` 属性将运算符与其方向等价物交换（例如，右括号在 RTL 中变成左括号）。对于没有适当镜像字符的运算符，字形级镜像应用 `rtlm` OpenType 字体特性，允许字体提供镜像字形。这种方法保留了不对称运算符（如顺时针轮廓积分）的语义正确性，在这些情况下简单的水平翻转会改变数学含义。

#### 适用场景

用阿拉伯语、希伯来语或其他 RTL 语言创建数学文档的内容作者现在可以依赖正确的运算符渲染，无需手动干预。为国际受众服务的教育平台、科学出版物和数学符号工具可以从正确的双向数学支持中受益。该实现尊重数学语义，同时适应方向上下文，确保视觉正确性和意义保留。

#### 参考资料

- [跟踪错误 #40120782](https://issues.chromium.org/issues/40120782)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6317308531965952)
- [规范](https://w3c.github.io/mathml-core/#layout-of-operators)

### The `clipboardchange` event

#### 新增内容

`clipboardchange` 事件在任何应用程序修改系统剪贴板内容时提供通知，使 Web 应用程序能够响应剪贴板更改而无需轮询。

#### 技术细节

此事件在剪贴板内容更改时触发，无论来源是什么——无论是来自 Web 应用程序本身、本机系统应用程序还是其他程序。该事件消除了反复检查剪贴板内容的低效 JavaScript 轮询循环的需求。应用程序可以在适当的作用域上注册事件监听器，并在剪贴板状态更改时立即收到通知，从而实现高效的同步模式。

#### 适用场景

远程桌面客户端可以实时保持本地和远程剪贴板同步，立即响应任一端的剪贴板更改。协作编辑工具可以检测用户何时从外部源复制内容，触发适当的格式化或安全检查。剪贴板管理器扩展可以维护历史记录而无需持续轮询开销。密码管理器可以检测复制操作，并在超时后提供清除敏感剪贴板内容的功能。

#### 参考资料

- [跟踪错误 #41442253](https://issues.chromium.org/issues/41442253)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5085102657503232)
- [规范](https://github.com/w3c/clipboard-apis/pull/239)
