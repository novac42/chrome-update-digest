## 领域摘要

Chrome 136 为 Chromium 的滚动条引入了视觉刷新，以匹配 Windows 11 Fluent 设计语言，影响 Windows 和 Linux 上的覆盖（overlay）和非覆盖滚动条。对开发者影响最大的可见变化是非覆盖 Fluent 滚动条在这些平台上默认启用，这可能会改变页面外观以及自定义滚动条样式与系统提供的 chrome 的交互。此更新通过统一各平台的滚动条视觉并减少原生 UI 期望与网页内容之间的摩擦，推动了 Web 平台的发展。团队应为潜在的布局和样式差异做好计划，并验证可访问性和视觉回归。

## 详细更新

下文列出基于上述摘要的具体浏览器更改。

### Fluent scrollbars (Fluent 滚动条)

#### 新增内容
Chromium 的滚动条（覆盖和非覆盖）在 Windows 和 Linux 上已现代化以符合 Windows 11 Fluent 设计语言。非覆盖的 Fluent 滚动条将在 Linux 和 Windows 上默认启用。（源内容在输入中被截断。）

#### 技术细节
- 适用于 Windows 和 Linux 上的覆盖和非覆盖滚动条模式。
- 根据发行说明，非覆盖的 Fluent 滚动条在这些平台上默认启用。
- 源数据未包含超出提供摘要的实现细节。

#### 适用场景
- UI 一致性：Web 应用和网站将在 Windows 和 Linux 上呈现与更新后的 Fluent 外观一致的滚动条，减少与原生控件的视觉不匹配。
- 开发者样式：使用自定义滚动条 CSS（例如 `::-webkit-scrollbar`）的团队应测试视觉回归，并确保自定义样式在新默认样式下仍然可读。
- 测试与可访问性：在刷新后验证键盘和辅助技术的交互以及视觉对比；当滚动条视觉影响快照时，也请重新运行视觉回归测试。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1292117 (跟踪 bug #1292117)  
- https://chromestatus.com/feature/5023688844812288 (ChromeStatus.com 条目)

已保存到： digest_markdown/webplatform/Browser changes/chrome-136-stable-en.md