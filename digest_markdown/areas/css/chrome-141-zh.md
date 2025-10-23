---
layout: default
title: chrome-141-zh
---

## 领域摘要

Chrome 141 的 CSS 更新聚焦于 CSSOM 的正确性与互操作性。主要更改修复了 `getComputedStyle()` 中自定义属性的枚举问题，确保在遍历计算样式时以及其长度计数能按预期反映自定义属性。这提升了规范一致性与跨浏览器一致性，减少依赖计算样式检查的工具与测试中的边缘情况缺陷。结果是在现代开发流程中更可靠的 CSS 检查、诊断与自动化。

## 详细更新

本次版本使 CSSOM 行为更贴近开发者预期与规范，提升样式自省与相关工具的可靠性。

### Custom property enumeration in `getComputedStyle()`（在 `getComputedStyle()` 中枚举自定义属性）

#### 新增内容
Chrome 141 修复了一个问题：迭代 `window.getComputedStyle(element)` 时不包含自定义属性，且返回对象的长度未将其计入。

#### 技术细节
- 现在对 `getComputedStyle(element)` 返回的 `CSSStyleDeclaration` 进行迭代时，会包含元素上定义的自定义属性。
- 返回对象的 `length` 属性会反映这些自定义属性的存在。
- 行为与 CSSOM 规范对计算样式枚举的要求保持一致。

#### 适用场景
- 枚举计算样式的样式检查与诊断工具无需变通即可获取自定义属性。
- 依赖 `CSSStyleDeclaration.length` 的测试套件与代码规范检查工具可获得准确计数，减少误报/漏报。
- 遍历计算样式的遥测、序列化或调试流程可生成完整的数据集。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5070655645155328
- 规范: https://drafts.csswg.org/cssom/#dom-window-getcomputedstyle
