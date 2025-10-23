---
layout: default
title: chrome-141-zh
---

## 领域摘要

Chrome 141 的 HTML-DOM 更新聚焦于无障碍可靠性与与标准对齐的 DOM 显露行为。新的 ARIA Notify API 为开发者提供对屏幕阅读器播报的直接编程控制，相比 ARIA live regions 更可靠，并将播报与 DOM 变更解耦。与此同时，针对 hidden=until-found 与 details 元素的算法更新可在祖先显露时防止出现无限循环，提升健壮性。总体而言，这些更改以最小的编写复杂度推动无障碍体验与平台正确性。

## 详细更新

这些更新提升无障碍易用性，并确保符合规范且健壮的 DOM 显露行为。

### ARIA Notify API

#### 新增内容
提供一个 JavaScript API，ariaNotify，使内容作者可指示屏幕阅读器播报的内容；相较 ARIA live regions 提升可靠性，并支持不依赖 DOM 更新的播报。

#### 技术细节
- 独立于 DOM 变更的编程式播报机制，输出更一致。
- 相比 live regions 提供更好的控制与可靠性。
- 跟进下方所引的 W3C ARIA 规范工作。

#### 适用场景
- 在不修改 DOM 的情况下播报异步事件（例如网络结果）。
- 提供超越 live regions 限制的清晰、即时的警报或确认。
- 在动态 UI 流程中确保无障碍播报的一致性。

#### 参考资料
- Tracking bug #326277796: https://issues.chromium.org/issues/326277796
- ChromeStatus.com 条目: https://chromestatus.com/feature/5745430754230272
- 规范: https://github.com/w3c/aria/pull/2577

### Update `hidden=until-found` and details ancestor revealing algorithm

#### 新增内容
实现针对 hidden=until-found 与 details 元素显露算法的规范变更，防止浏览器进入无限循环。

#### 技术细节
- 调整祖先显露过程，避免在显露逻辑中出现无限循环。
- 使 Chrome 行为与 WHATWG HTML 规范的最新更新保持一致。

#### 适用场景
- 在搜索/UA 显露流程中，对 hidden=until-found 内容实现更可靠的显露行为。
- 使 details 元素的展开更可预测，避免挂起或循环风险。
- 改善依赖内建显露语义的应用的健壮性。

#### 参考资料
- Tracking bug #433545121: https://issues.chromium.org/issues/433545121
- ChromeStatus.com 条目: https://chromestatus.com/feature/5179013869993984
- 规范: https://github.com/whatwg/html/pull/11457
