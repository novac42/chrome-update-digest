---
layout: default
title: chrome-138-zh
---

## 领域摘要

Chrome 138 (stable) 在 HTML-DOM 领域引入了一个针对错误建模的 DOM 级更改：QuotaExceededError 正从基于名称的 DOMException 条目转向一个从 DOMException 派生的接口。对开发者影响最大的是配额错误现在可以携带结构化的附加信息，而不再仅仅依赖 `name` 字符串。这推动了 Web 平台，使错误对象更丰富、可扩展，并便于更清晰的编程式处理。这些更新很重要，因为它们改善了诊断细节并为报告配额相关失败的 API 提供了向前兼容性。

## 详细更新

下面的单一更改直接来自摘要，并解释了面向开发者的影响。

### Update QuotaExceededError to a DOMException derived interface (将 QuotaExceededError 更新为从 DOMException 派生的接口)

#### 新增内容
之前，配额超限情况通过通用的 `DOMException` 报告，且 `name = "QuotaExceededError"`。该更改提议用一个从 `DOMException` 派生的 `QuotaExceededError` 接口来替代仅依赖名称的方法，以便错误可以携带附加信息。

#### 技术细节
- 该提案将 "QuotaExceededError" 从内置 `DOMException` 名称列表中移除，并引入一个从 `DOMException` 派生的专用接口。
- 此转变使得可以在错误对象上附加结构化数据或除 `name` 字符串之外的附加字段。

#### 适用场景
- 开发者可以从配额失败中获得更丰富的诊断信息（例如由实现提供的详细信息），以便于错误处理和遥测。
- 需要指示配额限制的 API 将获得可扩展的错误类型，从而实现更清晰且更易维护的错误处理代码路径。

#### 参考资料
- [ChromeStatus.com entry](https://chromestatus.com/feature/5647993867927552)
- [Link](https://whatpr.org/dom/1245.html)

File path to save this digest:
```text
digest_markdown/webplatform/HTML-DOM/chrome-138-stable-en.md
