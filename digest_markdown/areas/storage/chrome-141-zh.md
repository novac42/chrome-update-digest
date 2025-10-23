---
layout: default
title: chrome-141-zh
---

## 领域摘要

Chrome 141（stable）通过在 Storage Access API 中执行严格的同源策略（Same Origin Policy）语义来提升存储隐私。关键变化是：通过 `document.requestStorageAccess()` 授予的 Cookie 附加范围限定为精确的 iframe 源（origin），而非更广义的站点（site）。这强化了跨源隔离，减少了非预期的 Cookie 共享，使嵌入式存储行为更可预测。嵌入第三方内容的开发者应验证对 Cookie 的假设，并调整集成模式，以符合按源限定的访问。

## 详细更新

此版本聚焦于收紧存储访问的源级边界，以改进嵌入式上下文的隐私与可预测性。

### Strict Same Origin Policy for Storage Access API（Storage Access API 严格同源策略）

#### 新增内容
调整 Storage Access API 的语义，使其在安全方面严格遵循同源策略。默认情况下，在框架（frame）中使用 `document.requestStorageAccess()` 只会将 Cookie 附加到指向该 iframe 源的请求（而非站点）。

#### 技术细节
- 存储访问授权现作用于源级别，与同源策略保持一致。
- 在嵌入的框架中，由 `document.requestStorageAccess()` 导致的 Cookie 附加被限定为指向该 iframe 精确源的请求。
- 这减少了跨站 Cookie 暴露，并规范了第三方框架的行为。

#### 适用场景
- 在嵌入需要 Cookie 的第三方内容时，尽量减少跨站泄露。
- 需要在 iframe 中获得可预测、以源为作用域的 Cookie 行为的实现。
- 审计先前依赖站点级 Cookie 附加的集成，以确保与仅限源级作用域的兼容性。

#### 参考资料
- 跟踪问题 #379030052: https://issues.chromium.org/issues/379030052
- ChromeStatus.com 条目: https://chromestatus.com/feature/5169937372676096
- 规范: https://github.com/privacycg/storage-access/pull/213
