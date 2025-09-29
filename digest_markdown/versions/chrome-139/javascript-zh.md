---
layout: default
title: javascript-zh
---

## Area Summary

Chrome 139 使 JSON MIME 类型检测符合规范：按照 WHATWG mimesniff 规范识别所有有效的 JSON MIME 类型。对开发者最重要的变化是对 JSON 有载荷（包括以 `+json` 结尾的厂商和自定义类型）的更广泛且一致的检测，从而减少基于 Content-Type 分支的 API 的互操作性意外。这一对齐通过在解析或处理 JSON 的功能间强制采用统一的基于标准的检测模型，推动了 Web 平台的进步。对 JavaScript 开发者而言，这提高了依赖 Content-Type 分类的 fetch/XHR 处理、service workers 和其他运行时行为的可靠性。

## Detailed Updates

上述简要更改影响浏览器如何对 JSON 有载荷进行分类，进而影响 JavaScript 代码和 Web API 如何处理响应和请求体。

### Specification-compliant JSON MIME type detection（符合规范的 JSON MIME 类型检测）

#### What's New
Chrome 现在会识别 WHATWG mimesniff 规范定义的所有有效 JSON MIME 类型。这包括任何子类型以 `+json` 结尾的 MIME 类型，以及 `application/json` 和 `text/json`。

#### Technical Details
检测遵循 WHATWG mimesniff 关于 JSON MIME 类型的规则（子类型以 `+json` 结尾，或为 `application/json`/`text/json`），使 Chrome 的行为与规范保持一致。

#### Use Cases
- Fetch/XHR 响应处理：在根据 Content-Type 分支进行 JSON 解析的场景。
- Service workers 和其他依赖准确 JSON 分类的请求/响应过滤器。
- 使用厂商特定或自定义 `+json` 子类型（例如 `application/vnd.company+json`）的服务器和客户端集成将被正确视为 JSON。

#### References
- https://chromestatus.com/feature/5470594816278528
- https://mimesniff.spec.whatwg.org/#json-mime-type
