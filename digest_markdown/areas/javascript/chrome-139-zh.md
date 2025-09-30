---
layout: default
title: chrome-139-zh
---

## 领域摘要

Chrome 139 (stable) 更新了与 JavaScript 相关的 MIME 类型处理，以完全遵循 WHATWG mimesniff 规范中对 JSON 的要求。浏览器现在除了识别 `application/json` 和 `text/json` 外，还会识别任何以 `+json` 结尾的 MIME 子类型，这会影响通过 Content-Type 检测 JSON 的 API。此更改提升了 web APIs、service workers、fetch/XHR 处理器以及开发者自行实现的 MIME 检查的互操作性与正确性。开发者应检查服务器的 Content-Type 头，并避免仅匹配 `application/json` 的脆弱字符串检查。

## 详细更新

Below are the specific changes that implement the summary above and what they mean for JavaScript developers.

### Specification-compliant JSON MIME type detection（符合规范的 JSON MIME 类型检测）

#### 新增内容
Chrome 现在识别 WHATWG mimesniff 规范定义的所有有效 JSON MIME 类型，包括任何以 `+json` 结尾的 MIME 子类型，以及 `application/json` 和 `text/json`。

#### 技术细节
Chromium 的 networking/content-sniffing 层中的检测逻辑已与 WHATWG mimesniff 规范对齐。对执行基于 MIME 启发式判断的 API 来说，任何子类型以 `+json` 结尾的 Content-Type 都会被视为 JSON。

#### 适用场景
- 服务器 API 可以使用类似 `application/vnd.api+json` 的厂商或自定义类型，fetch()、XHR 以及其他浏览器 API 仍会将其视为 JSON。
- 在 Content-Type 上分支的 service workers 和中间件可以无需自定义列表就可靠地处理 `+json` 子类型。
- 此前对 `application/json` 进行手动匹配的库应更新以接受 `+json`，或依赖于 response.json() 的行为。

#### 参考资料
- https://chromestatus.com/feature/5470594816278528
- https://mimesniff.spec.whatwg.org/#json-mime-type

保存此摘要的文件：
```text
digest_markdown/webplatform/JavaScript/chrome-139-stable-en.md
