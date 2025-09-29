---
layout: default
title: chrome-139-zh
---

## Area Summary

Chrome 139 (stable) 提供了两个与 HTML-DOM 相关的更新：一项是在现代 Windows 上对 TCP 临时端口分配进行随机化的网络更改，另一项是放宽 JavaScript DOM 创建 API 的字符验证，使其与 HTML 解析器更一致。端口随机化减少了快速端口重用带来的风险，而 DOM 验证放宽则消除了从脚本创建元素/属性时的一类开发摩擦。这些更改共同提升了平台稳健性和互操作性，减少了网络和 DOM 构建工作流中的细微故障。

## Detailed Updates

The following entries expand on each change, emphasizing developer impact and technical pointers.

### Randomize TCP port allocation on Windows (在 Windows 上随机化 TCP 端口分配)

#### What's New
Enables TCP port randomization on Windows versions (2020 or later) where rapid reuse of prior ports is not expected to cause rejection due to timeouts.

#### Technical Details
The change adjusts ephemeral TCP port allocation behavior on supported Windows builds to introduce randomness and reduce collisions that stem from rapid port reuse (a manifestation of the Birthday problem). This is a platform-level networking mitigation that Chrome enables where safe.

#### Use Cases
- Reduces intermittent connection failures for browser network clients and WebRTC flows caused by port reuse timing.
- Improves reliability of parallel connections and automated test runs that open many short-lived sockets.
- Developers should be aware of slightly different ephemeral port distributions when diagnosing connection-level issues.

#### References
- https://issues.chromium.org/issues/40744069
- https://chromestatus.com/feature/5106900286570496

### Allow more characters in JavaScript DOM APIs (在 JavaScript DOM API 中允许更多字符)

#### What's New
Relaxes validation in JavaScript DOM creation APIs so element and attribute names accepted by the HTML parser are also accepted when created via DOM APIs.

#### Technical Details
Historically the HTML parser permitted a wide variety of valid characters in element/attribute names while JS DOM APIs enforced stricter validation. This change aligns the JavaScript-facing validation with the parser’s rules and the relevant namespace handling per the spec.

#### Use Cases
- Scripts can create elements and attributes that previously failed validation, improving parity with server-generated markup and authoring tools.
- Facilitates interoperability when working with nonstandard or internationalized names and when migrating markup-generation code to client-side APIs.
- Developers should consult namespace rules in the spec when creating names across XML/HTML namespaces.

#### References
- https://issues.chromium.org/issues/40228234
- https://chromestatus.com/feature/6278918763708416
- https://dom.spec.whatwg.org/#namespaces

保存路径:
digest_markdown/webplatform/HTML-DOM/chrome-139-stable-en.md
