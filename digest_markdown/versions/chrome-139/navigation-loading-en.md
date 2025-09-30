---
layout: default
title: navigation-loading-en
---

## Area Summary

Chrome 139 (stable) introduces a privacy-focused Navigation-Loading change that clears window.name when a navigation causes a browsing context group switch. This primarily mitigates a cross-site tracking vector by preventing information leakage through window.name. For developers, the most impactful change is that window.name can no longer be relied on to persist data across navigations that cross browsing context groups. The update tightens privacy guarantees in the navigation model and aligns behavior with the HTML spec.

## Detailed Updates

The single Navigation-Loading change in this release strengthens privacy during cross-site navigations. Details follow.

### Clear window name for cross-site navigations that switches browsing context group

#### What's New
Clears the value of the `window.name` property when navigation switches browsing context groups, to avoid leaking information that could be used as a tracking vector.

#### Technical Details
This behavior enforces a reset of `window.name` on navigations that change the browsing context group, consistent with the HTML specification's resetBCName step. The change is implemented to prevent cross-site carryover of `window.name` state.

#### Use Cases
- Prevents using `window.name` as a cross-site tracking channel.
- Developers should not rely on `window.name` to persist data across navigations that may switch browsing context groups; use explicit storage or messaging patterns instead.

#### References
- https://issues.chromium.org/issues/1090128
- https://chromestatus.com/feature/5962406356320256
- https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName
