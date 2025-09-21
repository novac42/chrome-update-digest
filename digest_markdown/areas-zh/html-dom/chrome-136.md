---
layout: default
title: Chrome 更新分析器 - 领域专业分析（中文）
---

# Chrome 更新分析器 - 领域专业分析（中文）

## 领域摘要

Chrome 136 的 **HTML-DOM** 更新专注于增强画布文本渲染能力并改进 SVG API 与 W3C 规范的一致性。最重要的新增功能是对 CanvasTextDrawingStyles 的语言支持，这使得在 OffscreenCanvas 上下文中能够正确进行特定区域设置的字体选择——解决了国际化支持中长期存在的缺口。此外，SVG 几何方法的更新通过采用 DOMPointInit 接口使 Chromium 与现代 W3C 标准保持一致。这些更改共同推进了 Web 平台在图形渲染和国际化内容处理方面的能力，为开发者提供了更强大的工具来创建可访问的本地化 Web 应用程序。

## 详细更新

这些更新通过改进国际化和标准合规性加强了 Chrome 的 DOM 实现，建立在平台对一致跨浏览器行为承诺的基础上。

### Language support for CanvasTextDrawingStyles

#### 新增功能
Chrome 136 为 OffscreenCanvas 文本渲染引入了语言属性支持，在之前缺乏国际化能力的画布上下文中启用特定区域设置的字体选择和字形处理。

#### 技术详情
`<canvas>` DOM 元素长期以来一直支持用于语言特定字体选择的 `lang` 属性，允许浏览器在字体中可用时选择适当的特定区域设置字形。然而，在创建 `OffscreenCanvas`（独立于 DOM 存在）时，没有机制来指定区域设置信息。此更新扩展了 CanvasTextDrawingStyles 接口以尊重语言设置，确保所有画布上下文中的一致国际化行为。

#### 使用案例
此增强功能对以下应用程序特别有价值：
- 使用 OffscreenCanvas 进行性能优化时渲染多种语言的文本
- 在 Web Worker 中生成具有特定区域设置排版的图形
- 创建国际化数据可视化或动态文本渲染
- 构建需要为不同语言进行适当字体选择的基于画布的游戏或应用程序

#### 参考链接
- [Tracking bug #385006131](https://bugs.chromium.org/p/chromium/issues/detail?id=385006131)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5101829618114560)
- [Spec](https://html.spec.whatwg.org/multipage/canvas.html#canvastextdrawingstyles)

### Use DOMPointInit for getCharNumAtPosition, isPointInFill, isPointInStroke

#### 新增功能
Chromium 现在对 SVG 几何元素中的 `getCharNumAtPosition`、`isPointInFill` 和 `isPointInStroke` 方法使用 `DOMPointInit` 而不是传统的 `SVGPoint` 接口，与最新的 W3C 规范保持一致。

#### 技术详情
此更改将 `SVGGeometryElement` 和 `SVGPathElement` 方法更新为接受 `DOMPointInit` 参数，这是在 Web API 中表示 2D 和 3D 点的现代标准化接口。与传统的 `SVGPoint` 接口相比，`DOMPointInit` 接口在不同 Web API 之间提供了更好的类型安全性和一致性，代表了更广泛的 Web 平台现代化努力的一部分。

#### 使用案例
使用 SVG 的开发者将受益于：
- 在 SVG 中进行基于点的计算时具有更一致的 API 模式
- 为 SVG 几何操作提供更好的 TypeScript 支持和类型检查
- 与已经使用 DOMPointInit 的其他现代 Web API 一起使用这些方法时简化代码
- 与当前 Web 标准保持一致的面向未来的代码

#### 参考链接
- [Tracking bug #40572887](https://bugs.chromium.org/p/chromium/issues/detail?id=40572887)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5084627093929984)
- [Spec](https://www.w3.org/TR/SVG2/types.html#InterfaceDOMPointInit)