---
layout: default
title: chrome-138-zh
---

## 领域摘要

Chrome 138 改变了配额超出错误的表示方式：从使用一个 name 为 "QuotaExceededError" 的通用 DOMException，转为使用专门的、派生自 DOMException 的接口。此更改使配额错误能够携带结构化的附加信息，而不仅仅依赖旧有的名称字符串。对于开发者来说，最直接的影响是当触及存储或配额限制时，程序化的错误处理得到改善且诊断信息更为丰富。总体而言，此更新规范化了错误语义并使平台 API 更具表达力。

## 详细更新

下面是基于上述摘要的面向 JavaScript 的详细信息。

### Update QuotaExceededError to a DOMException derived interface（将 QuotaExceededError 更新为派生自 DOMException 的接口）

#### 新增内容
以前平台通过抛出一个其 name 属性被设置为 "QuotaExceededError" 的 DOMException 来表示配额错误。此次更改引入了一个专门用于配额超出情况的、派生自 DOMException 的接口，以便错误可以携带额外的信息。

#### 技术细节
该提案用定义一个扩展自 DOMException 的独立接口来替代以 name="QuotaExceededError" 即兴使用 DOMException 的做法。这样实现可以将结构化数据（字段或属性）附加到错误对象上，而不再仅依赖名称字符串。

#### 适用场景
- 在与存储相关的 API 中更可靠地检测配额条件。  
- 抛出的错误上可获得更丰富的诊断数据，从而支持更好的恢复或遥测。  
- 为需要报告配额问题的 Web API 提供更整洁、由规范驱动的错误表面。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5647993867927552  
- 规范： https://whatpr.org/dom/1245.html
