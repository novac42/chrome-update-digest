---
layout: default
title: chrome-142-en
---

## Area Summary

Chrome 142's Navigation-Loading update focuses on preserving sticky user activation across same-origin renderer-initiated navigations. The most impactful change for developers is that user activation state is retained after navigating to another same-origin page, addressing blockers like virtual keyboards not appearing on auto-focus. This advances the web platform by reducing friction for post-navigation interactions that require prior user activation. The change matters because it restores developer expectations for seamless interactive behavior across same-origin navigations.

## Detailed Updates

Below are the detailed notes for the Navigation-Loading change in Chrome 142.

### Sticky user activation across same-origin renderer-initiated navigations

#### What's New
This feature preserves the sticky user activation state after a page navigates to another same-origin page.

#### Technical Details
Applies to renderer-initiated, same-origin navigations; the browser retains the sticky user activation flag into the post-navigation document so behaviors that depend on prior activation can proceed.

#### Use Cases
- Enables scenarios such as showing virtual keyboards on auto-focus in the navigated-to page.  
- Unblocks developer workflows that rely on preserved user activation across same-origin navigations.

#### References
- [Tracking bug #433729626](https://issues.chromium.org/issues/433729626)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5078337520926720)  
- [Spec](https://github.com/whatwg/html/pull/11454)
