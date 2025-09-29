---
layout: default
title: chrome-139-en
---

## Area Summary

Chrome 139 (stable) introduces a privacy-focused Navigation-Loading change that clears the value of `window.name` when a navigation causes a browsing context group switch. This reduces a persistent cross-navigation tracking vector by preventing data leaking across distinct browsing-context groups. For developers, the most impactful change is that any reliance on `window.name` to persist data across cross-site navigations will break; alternatives like postMessage or origin-scoped storage should be used. The change aligns the browser with the HTML spec and strengthens web platform privacy guarantees while having minimal performance impact.

## Detailed Updates

Below are the details for the Navigation-Loading change and practical implications for developers.

### Clear window name for cross-site navigations that switches browsing context group

#### What's New
The browser now clears the `window.name` property when a navigation results in a browsing context group switch, preventing the value from surviving into the new group.

#### Technical Details
Per the HTML specification's resetBCName step, user agents reset the browsing context name when a navigation crosses browsing-context-group boundaries. The implementation in Chrome follows this behavior, causing `window.name` to become an empty string at the navigation boundary rather than carry previous values into a different browsing-context group.

#### Use Cases
- Prevents using `window.name` as a cross-site storage/tracking channel.
- Developers who used `window.name` to pass data across top-level navigations should migrate to alternatives (postMessage, same-origin storage, or ephemeral URL/state passing) for cross-origin scenarios.
- Single-origin navigation flows that do not trigger a browsing-context-group switch remain unaffected.

#### References
- Tracking bug #1090128: https://issues.chromium.org/issues/1090128
- ChromeStatus.com entry: https://chromestatus.com/feature/5962406356320256
- Spec: https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName

File saved to: digest_markdown/webplatform/Navigation-Loading/chrome-139-stable-en.md
