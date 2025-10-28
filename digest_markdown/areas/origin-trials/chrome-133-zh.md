---
layout: default
title: chrome-133-zh
---

## 领域摘要

Chrome 133 的 Origin Trials 侧重于通过可选注册为开发者提供对生命周期和可访问性行为的有针对性控制。这两个试验允许网站选择在省电模式下不被冻结，以及在 shadow DOM 边界之间引用元素以建立 ARIA 关系。这些更改很重要，因为它们在不削弱封装性的前提下保留了交互性并改善了可访问组件的组合。开发者应评估是否为这些试验注册，以在受影响的场景中维护用户体验和可访问性。

## 详细更新

下面列出 Chrome 133 中的 origin-trial 功能，包含简要的技术说明、现实场景示例以及权威参考链接。

### Opt out of freezing on Energy Saver（在省电模式下取消冻结）

#### 新增内容
此取消冻结试验允许网站选择不受 Chrome 133 中随省电模式启用的冻结行为影响。

#### 技术细节
- 支持 origin-trial 的行为，修改在省电模式下的页面生命周期冻结行为。
- 关联规范：Page Lifecycle。
- 发布元数据中的主要标签：webgpu, origin-trials。

#### 适用场景
- 需要持续活动的站点（例如长时间运行的计算、实时交互或图形工作负载）可以注册以避免在浏览器进入省电模式时被冻结。
- 对需要在低功耗模式下保持执行的 PWA 和 WebGPU 驱动应用有用。

#### 参考资料
- [跟踪缺陷 #325954772](https://issues.chromium.org/issues/325954772)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5158599457767424)
- [规范](https://wicg.github.io/page-lifecycle)

### Reference Target for Cross-root ARIA（跨根 ARIA 的引用目标）

#### 新增内容
Reference Target 是一项功能，允许使用诸如 `for` 和 `aria-labelledby` 的 IDREF 属性引用组件的 shadow DOM 内的元素，同时保持 shadow DOM 内部细节的封装。该功能的主要目标是使 ARIA 能跨越 shadow ro...

#### 技术细节
- 使 `for` 和 `aria-labelledby` 等属性的跨根 IDREF 解析成为可能，以改善涉及 shadow DOM 组件的 ARIA 关系。
- 旨在在允许外部可访问性引用的同时保持 shadow DOM 封装。
- 发布元数据中的主要标签：webgpu, origin-trials。

#### 适用场景
- 组件作者可以构建可访问的 web 组件，使标签或 describedby 关系跨越 light DOM 与 shadow DOM，而无需暴露内部实现细节。
- 改善复杂组件层级中 ARIA 语义的互操作性，并促进更健壮的屏幕阅读器行为。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5188237101891584)
