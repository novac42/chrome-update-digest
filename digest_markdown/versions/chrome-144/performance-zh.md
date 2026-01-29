---
layout: default
title: Chrome 144 Stable - Performance 更新
---

# Chrome 144 Stable - Performance 更新

## 领域摘要

Chrome 144 通过新的 `performance.interactionCount` 属性对 Event Timing API 进行了重大增强，使 Chromium 与其他主流浏览器和 Interop 2025 倡议保持一致。此功能解决了衡量用户交互性能方面的关键缺口，为开发者提供了页面上总交互次数的准确计数，这对于计算 Interaction to Next Paint (INP) 指标至关重要。作为 Performance Timeline 规范的一部分，此更新实现了更精确的性能监控，并帮助开发者通过识别交互瓶颈来优化用户体验。这一长期指定功能的增加展示了 Chrome 致力于在 Web 平台上标准化性能测量工具的承诺。

## 详细更新

Chrome 144 的性能改进专注于增强 Event Timing API 的用户交互测量能力，为开发者提供更好的工具来监控和优化页面响应性。

### Performance and Event Timing: `interactionCount`

#### 新增内容

Chrome 144 引入了 `performance.interactionCount` 属性，该属性跟踪页面上发生的用户交互总数。此属性与现有的 Event Timing API 协同工作，提供全面的交互性能数据。

#### 技术细节

Event Timing API 是 Performance Timeline 的一部分，用于测量用户交互的性能。某些事件被分配了 `interactionId` 值，该值根据常见的物理用户输入或手势将相关交互分组。新的 `performance.interactionCount` 属性通过维护页面上所有交互的运行计数来补充这一功能。

此功能已被指定很长时间，并且之前在 Chromium 中进行过原型设计，但从未发布。它现在是 Interop 2025 倡议的一部分，并且已在其他主流浏览器中可用，确保跨浏览器兼容性。

**注意：** 虽然存在更强大的 `performance.eventCounts` 映射用于跟踪特定事件，但它无法准确地将事件计数映射到交互计数，这使得 `interactionCount` 对于交互特定指标至关重要。

#### 适用场景

此功能的主要用例是计算 Interaction to Next Paint (INP) 指标值，这是衡量页面响应性的关键 Core Web Vital。INP 需要知道总交互次数才能计算高百分位数分数（对于总交互次数超过 50 次的页面为 p98）。使用 `performance.interactionCount`，开发者可以：

- 准确计算用于性能监控的 INP 指标
- 识别可能需要优化的高交互量页面
- 构建更复杂的用户体验分析
- 确保不同浏览器之间性能测量的一致性

#### 参考资料

- [ChromeStatus.com 条目](https://chromestatus.com/feature/5153386492198912)
- [规范](https://www.w3.org/TR/event-timing/#dom-performance-interactioncount)
