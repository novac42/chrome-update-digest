---
layout: default
title: chrome-139-zh
---

## Area Summary

Chrome 139 (stable) 引入了一项以隐私为重点的 Navigation-Loading 更改，当导航导致浏览上下文组切换时，会清除 `window.name` 的值。通过防止数据在不同浏览上下文组之间泄露，该更改减少了持久的跨导航跟踪向量。对开发者来说，最重要的影响是任何依赖 `window.name` 在跨站导航中持久化数据的做法将会失效；应使用 postMessage 或 origin-scoped storage 等替代方案。该更改使浏览器与 HTML 规范保持一致，增强了 Web 平台的隐私保障，同时对性能影响最小。

## Detailed Updates

下面是关于该 Navigation-Loading 更改的详细信息以及对开发者的实际影响。

### Clear window name for cross-site navigations that switches browsing context group (在跨站导航导致浏览上下文组切换时清除 window.name)

#### What's New
The browser now clears the `window.name` property when a navigation results in a browsing context group switch, preventing the value from surviving into the new group.

#### Technical Details
Per the HTML specification's resetBCName step, user agents reset the browsing context name when a navigation crosses browsing-context-group boundaries. The implementation in Chrome follows this behavior, causing `window.name` to become an empty string at the navigation boundary rather than carry previous values into a different browsing-context group.

#### Use Cases
- 阻止将 `window.name` 用作跨站点存储/跟踪通道。
- 使用 `window.name` 在顶级导航之间传递数据的开发者，在跨源情形应迁移到替代方案（postMessage、same-origin storage 或临时 URL/状态传递）。
- 不会触发浏览上下文组切换的单源导航流程不受影响。

#### References
- Tracking bug #1090128: https://issues.chromium.org/issues/1090128
- ChromeStatus.com entry: https://chromestatus.com/feature/5962406356320256
- Spec: https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName

File saved to: digest_markdown/webplatform/Navigation-Loading/chrome-139-stable-en.md
