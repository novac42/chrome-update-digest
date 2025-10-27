---
layout: default
title: pwa-service-worker-zh
---

## 详细更新

以下条目对上面的摘要展开说明，描述了更改内容、工作原理及实际的开发者使用场景。

### Document subtitle (Fix PWA app titles)（文档副标题）

#### 新增内容
为已安装并运行的 PWA 提供页面副标题，用于在窗口标题栏中显示补充信息，在该窗口中替代 HTML 标题元素显示的文本。

#### 技术细节
该功能对已安装 PWA 的当前窗口暴露了一个独立的副标题值；当存在该值时，会在窗口标题区域显示，而不是显示文档的 HTML <title>。有关实现和互操作性说明，请参阅链接的规范和跟踪 bug。

#### 适用场景
- 在 PWA 窗口标题中显示上下文状态或视图名称（例如，“Inbox — Work”），而无需修改用于标签页的文档标题。
- 提高清晰度以支持多窗口 PWA，其中每个窗口代表不同内容或用户上下文。

#### 参考资料
- 跟踪 bug #1351682: https://issues.chromium.org/issues/1351682
- ChromeStatus.com 条目: https://chromestatus.com/feature/5168096826884096
- 规范: https://github.com/whatwg/html/compare/main...diekus:html:main

### User link capturing on PWAs（PWA 上的用户链接捕获）

#### 新增内容
可以由已安装 Web 应用处理的链接将自动定向到该应用，从而简化浏览器与已安装体验之间的导航，更贴合用户预期。

#### 技术细节
当用户点击一个可由已安装 Web 应用处理的导航链接时，Chrome 会在已安装的应用中打开该链接，而不是将导航限制在浏览器中。有关资格标准和行为详细信息，请参阅开发者文档和 ChromeStatus 条目。

#### 适用场景
- 确保来自网页的深度链接在已安装的应用中打开，以实现更紧密的集成用户流。
- 在浏览器上下文与应用上下文之间移动时减少用户摩擦，提高 PWA 的保留和参与度。

#### 参考资料
- 开发者文档: https://docs.google.com/document/d/e/2PACX-1vSqYzAmiLr-58OgSWBITtAAu6_2XUpjjNEdMvc6IdZn9DjQCeVrE0SKViumyly0cpryxAONMq62zwHw/pub
- ChromeStatus.com 条目: https://chromestatus.com/feature/5194343954776064
