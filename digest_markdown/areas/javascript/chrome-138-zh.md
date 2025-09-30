---
layout: default
title: chrome-138-zh
---

### 1. Area Summary （区域摘要）

Chrome 138 引入了一个关于配额超出错误表示方法的更改：将 QuotaExceededError 从基于名称的 DOMException 条目迁移为派生自 DOMException 的接口。这样可以让配额错误携带结构化的额外信息，提升可诊断性和在 JavaScript 中的程序化处理能力。该更改使异常对象更可扩展并与 WebIDL 派生接口保持一致。开发者应为更稳健的错误处理做准备，并优先使用能力检查而非脆弱的字符串比较。

## 详细更新

下面是 Chrome 138 中与 JavaScript 领域相关的更新及其对开发者的影响。

### Update QuotaExceededError to a DOMException derived interface （将 QuotaExceededError 更新为派生自 DOMException 的接口）

#### 新增内容
提出不再将 "QuotaExceededError" 仅视为 DOMException 的 name 值，而是将其定义为派生自 DOMException 的接口，能够携带额外信息。

#### 技术细节
该更改会将 "QuotaExceededError" 从内置 DOMException name 字符串列表中移除，并用一个真正的派生自 DOMException 的接口替代。这样异常可以暴露除旧有 `name` 属性之外的额外属性，从而允许将更丰富的结构化数据附加到配额错误上。

#### 适用场景
- 与存储和配额相关的 API 可以返回带有上下文数据的配额错误，以便更好地诊断。  
- 客户端代码可以对配额情况进行更精确的程序化处理（而不是仅依赖字符串匹配）。

#### 开发者指导
审查检查 `error.name === "QuotaExceededError"` 的代码，并准备在该接口落地后采用特性检测或 instanceof 风格的检查。可用时优先处理更丰富的异常属性。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5647993867927552  
- 规范: https://whatpr.org/dom/1245.html
