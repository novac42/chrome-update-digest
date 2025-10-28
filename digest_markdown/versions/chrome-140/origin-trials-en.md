---
layout: default
title: origin-trials-en
---

## Detailed Updates

Below are concise, developer-focused explanations of each origin trial in this release and what they mean for implementation, security, and common use cases.

### Enable incoming call notifications

#### What's New
Extends the Notifications API for installed PWAs to send incoming-call style notifications with call-styled actions and a ringtone to surface VoIP calls more prominently.

#### Technical Details
This is an Origin Trial exposing call-like notification affordances via the Notifications API for installed PWAs. Expect integration points with PWA installation state, notification action buttons, and playing a ringtone. Pay attention to permission and UX constraints imposed by the Notifications spec and platform notification behavior.

#### Use Cases
VoIP and video-call web apps can present recognizable incoming-call UIs, improving user responsiveness and parity with native call notifications.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009)
- [Tracking bug](https://issues.chromium.org/issues/detail?id=1383570)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5110990717321216)
- [Spec](https://notifications.spec.whatwg.org)

### Crash Reporting key-value API

#### What's New
Introduces a per-document key-value API (tentatively window.crashReport) whose map contents are appended to crash reports when renderer crashes occur.

#### Technical Details
The API provides a document-scoped backing map whose entries are serialized into the CrashReportBody on renderer process failure. This origin trial gives developers a controlled channel to attach diagnostic metadata to crash reports, improving post-mortem analysis while requiring careful handling of sensitive data.

#### Use Cases
Improve crash triage by annotating renderer crashes with contextual state (feature flags, last actions). Useful for complex single-page apps, PWAs, and debugging production stability regressions.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905)
- [Tracking bug](https://issues.chromium.org/issues/400432195)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6228675846209536)
- [GitHub](https://github.com/WICG/crash-reporting/pull/37)

### Add the `clipboardchange` event

#### What's New
Adds a clipboardchange event that fires when the system clipboard content changes, enabling efficient synchronization without polling.

#### Technical Details
This Origin Trial surfaces a DOM event signifying system clipboard mutations. Implementations will need to reconcile platform clipboard privacy/security models and may gate event delivery by focus, permissions, or user gesture policy to mitigate exfiltration risks.

#### Use Cases
Remote desktop clients and productivity web apps can keep in-page clipboard state synchronized with the system clipboard, improving user experience for copy/paste workflows.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/137922738588221441)
- [Tracking bug](https://issues.chromium.org/issues/41442253)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232)
- [GitHub](https://github.com/w3c/clipboard-apis/pull/239)

### Enable `SharedWorker` on Android

#### What's New
Runs SharedWorker support on Android to allow multiple tabs/contexts to share a single worker, enabling shared connections and resource-efficient coordination.

#### Technical Details
This Origin Trial enables the SharedWorker interface on Android platforms. SharedWorkers allow multiple browsing contexts from the same origin to communicate with a shared script context, useful for sharing WebSocket/SSE connections and centralized state. Expect developer attention on lifecycle semantics, cross-document messaging, and consistency with the HTML spec.

#### Use Cases
Conserve resources by sharing a single WebSocket or SSE across tabs; coordinate background tasks or centralized caching across multiple tabs of the same origin on Android.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6265472244514816)
- [Spec](https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface)

Saved file: digest_markdown/webplatform/Origin trials/chrome-140-stable-en.md
