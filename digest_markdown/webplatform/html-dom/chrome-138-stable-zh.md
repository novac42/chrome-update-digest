## 区域摘要

Chrome 138 在 HTML-DOM 中引入了一项聚焦更改：QuotaExceededError 将从以名称字符串表示的 DOMException 情形，转换为一个派生自 DOMException 的接口。这样与配额相关的错误可以携带超出名称字符串的结构化、可扩展信息。对开发者而言，此更改改进了对报告配额超出情况的 API 的错误处理和诊断。总体上，这通过使异常对象更具表达性和互操作性推进了 Web 平台。

## 详细更新

下面的单项更新扩展了摘要并说明了对开发者的影响与参考资料。

### Update QuotaExceededError to a DOMException derived interface（将 QuotaExceededError 更新为派生自 DOMException 的接口）

#### 新增内容
QuotaExceededError 不再仅以带有特定名称字符串的 DOMException 表示；而是将以派生自 DOMException 的接口表示，从而允许错误携带附加的结构化信息。

#### 技术细节
该提案将把 "QuotaExceededError" 从内置的仅以名称标识的 DOMException 列表中移除，并为配额超出情况定义一个专用的派生自 DOMException 的接口。这样实现者可以在异常对象上暴露属性或结构化字段，而不是仅依赖 name property。

#### 适用场景
- 需要指示配额超出的 API 可以提供更丰富的错误细节，以便程序化处理和诊断。  
- 开发者可以基于新异常接口暴露的结构化字段实现更细粒度的恢复或上报逻辑。

#### 参考资料
- https://chromestatus.com/feature/5647993867927552
- https://whatpr.org/dom/1245.html