---
layout: default
title: performance-zh
---

### 1. 领域摘要

Chrome 136（stable）引入了一项由 origin trial 驱动的能力，帮助 Web 应用检测并理解双峰页面加载性能分布（例如冷启动与热启动）。对开发者影响最大的是能够按是否受昂贵的、平台级启动影响对遥测和指标进行分段。这样可以更准确地报告百分位、改进性能回退的检测，并进行有针对性的优化（在温路径上延后/安排更重的工作），且不改变最终用户行为。这些更新通过暴露可减少真实世界性能测量噪声的信号推进了 Web 平台，并使团队能够更有效地优先分配工程资源。

## 详细更新

Below are the relevant details and developer implications connected to the summary above.

### Enable web applications to understand bimodal performance timings（识别双峰性能时序）

#### 新增内容
Chrome 136 的一个 origin trial 提供了一种方法，允许 Web 应用检测页面加载时序何时受双峰因素（例如浏览器冷启动）影响，从而使开发者能够在遥测和分析中将这些情况与正常导航分离。

#### 技术细节
该能力通过 origin trial 暴露（参见 Origin Trial 链接）。概念上，它让页面能够区分受系统级初始化或其他应用外因素影响的导航与典型导航——从而减少聚合时序分布的偏斜。集成将与现有的 timing 接口并存（例如 Navigation Timing），以便检测和分析管道可以筛选或标记受影响的事件。将其用于避免将平台级抖动误归因于应用回归。

#### 适用场景
- 在计算 p50/p90/p99 时对性能遥测进行分段，排除冷启动异常值。
- 通过过滤受平台初始化影响的导航，使 A/B 测试组更可靠。
- 在热路径上延后非关键的 JS/CSS/worker 初始化，同时确保对冷启动具有弹性。
- 通过将平台引起的方差与应用回归分离来改进 CI/性能仪表板。

#### 参考资料
- https://developer.chrome.com/origintrials/#/trials/active
- https://bugs.chromium.org/p/chromium/issues/detail?id=1413848
- https://chromestatus.com/feature/5037395062800384
- https://w3c.github.io/navigation-timing/

Output file: digest_markdown/webplatform/Performance/chrome-136-stable-en.md
