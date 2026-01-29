---
layout: default
title: javascript-zh
---

## 领域摘要

Chrome 143（stable）在国际化、可编辑文本 API、输入事件数据和联合身份方面推进了与 JavaScript 相关的平台能力。该版本将 ICU 升级以支持 Unicode 16，修复并完善了 EditContext TextFormat 属性，在某些输入事件上公开剪贴板/拖动数据，并允许 FedCM 中的 IdP 返回结构化 JSON。这些更改减少了本地化、富文本编辑、粘贴/拖放处理和身份验证流程的开发者摩擦，并紧密对齐平台行为与 Web 规范。

## 详细更新

以下条目在上述摘要基础上提供了简洁的技术和以开发者为中心的详细信息。

### ICU 77 (supporting Unicode 16)

#### 新增内容
Chrome 的 ICU 库升级到 77.1，添加了 Unicode 16 支持和更新的区域设置数据。

#### 技术细节
此升级更新了与 Intl 相关的行为（区域设置数据、排序规则、格式化）。发布说明警告说，两个更改可能对假定 Intl JS API 特定输出格式的 Web 应用构成风险。

#### 适用场景
改进了国际化格式化、排序和区域设置敏感操作的正确性；依赖精确 Intl 字符串格式的应用应在升级后验证输出。

#### 参考资料
- [跟踪错误 #421834885](https://issues.chromium.org/issues/421834885)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5143313833000960)
- [规范](https://tc39.es/ecma402)

### EditContext: TextFormat underlineStyle and underlineThickness

#### 新增内容
Chrome 修复了 EditContext/TextFormat 行为，使 underlineStyle 和 underlineThickness 通过 textformatupdate 事件正确公开。

#### 技术细节
EditContext API 现在在 textformatupdate 回调中提供了更正的 TextFormat 对象，使实现与 W3C Edit Context 规范对富文本属性报告的要求保持一致。

#### 适用场景
支持在 Web 编辑器和 IME 集成中稳健处理下划线样式和粗细；对读取格式属性的协作编辑器和辅助功能工具有益。

#### 参考资料
- [EditContext API](https://developer.mozilla.org/docs/Web/API/EditContext)
- [`TextFormat`](https://developer.mozilla.org/docs/Web/API/TextFormat)
- [textformatupdate 事件](https://developer.mozilla.org/docs/Web/API/EditContext/textformatupdate_event)
- [跟踪错误 #354497121](https://issues.chromium.org/issues/354497121)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6229300214890496)
- [规范](https://w3c.github.io/edit-context/#textformatupdateevent)

### `DataTransfer` property for `insertFromPaste`, `insertFromDrop` and `insertReplacementText` input events

#### 新增内容
inputType 为 insertFromPaste、insertFromDrop 和 insertReplacementText 的输入事件现在包含已填充的 dataTransfer 属性。

#### 技术细节
InputEvent 接口在这些输入事件上公开 DataTransfer 对象，根据输入事件规范，使脚本能够访问粘贴/拖放操作期间可用的相同剪贴板和拖放负载。

#### 适用场景
允许编辑器和 contenteditable 处理程序在输入事件处理程序中同步检查和处理粘贴或拖放的内容，无需单独的剪贴板或拖动事件管道。

#### 参考资料
- [跟踪错误 #401593412](https://issues.chromium.org/issues/401593412)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6715253274181632)
- [规范](https://w3c.github.io/input-events/#dom-inputevent-datatransfer)

### FedCM: Support structured JSON responses from IdPs

#### 新增内容
FedCM 现在接受来自身份提供者在 id_assertion_endpoint 的结构化 JSON 对象，而不仅仅是纯字符串。

#### 技术细节
IdP 可以在由依赖方消费的断言中返回解析的 JSON；浏览器显示这些结构化响应，消除了 RP 代码中手动字符串序列化和解析的需要。

#### 适用场景
简化了 FedCM 集成，支持更丰富的断言负载（声明、元数据），并减少了联合登录流程中的编码/解码错误。

#### 参考资料
- [跟踪错误 #346567168](https://issues.chromium.org/issues/346567168)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5153509557272576)
- [规范](https://github.com/w3c-fedid/FedCM/pull/771)
