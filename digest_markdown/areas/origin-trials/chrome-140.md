---
layout: default
title: chrome-140
---

## Origin trials

### Enable incoming call notifications

This feature extends the Notifications API to allow installed PWAs to send incoming call notifications—notifications with call-styled buttons and a ringtone. This extension helps VoIP web apps create more engaging experiences by making it easier for users to recognize and answer calling notifications. Additionally, this feature helps bridge the gap between native and web implementations of apps that have them both.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009) | [Tracking bug #detail?id=1383570](https://issues.chromium.org/issues/detail?id=1383570) | [ChromeStatus.com entry](https://chromestatus.com/feature/5110990717321216) | [Spec](https://notifications.spec.whatwg.org)

### Crash Reporting key-value API

This feature introduces a new key-value API, tentatively `window.crashReport`, backed by a per-document map that holds data appended to crash reports.

The data placed in this API's backing map is sent in the `CrashReportBody` if any renderer process crashes occur on the site. This lets developers debug what specific state in their application might be causing a given crash.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905) | [Tracking bug #400432195](https://issues.chromium.org/issues/400432195) | [ChromeStatus.com entry](https://chromestatus.com/feature/6228675846209536) | [Spec](https://github.com/WICG/crash-reporting/pull/37)

### Add the `clipboardchange` event

The `clipboardchange` event fires whenever a web app or any other system application changes the system clipboard contents. This allows web apps like remote desktop clients to keep their clipboards synchronized with the system clipboard. It provides an efficient alternative to polling the clipboard with JavaScript for changes.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/137922738588221441) | [Tracking bug #41442253](https://issues.chromium.org/issues/41442253) | [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232) | [Spec](https://github.com/w3c/clipboard-apis/pull/239)

### Enable `SharedWorker` on Android

The long-standing demand for SharedWorker support on Android stems from several needs expressed by web developers:

  * **Resource sharing and efficiency** : Developers aim to share a single WebSocket or Server-Sent Events (SSE) connection across multiple tabs, thereby conserving resources.
  * **Persistent resource management** : A requirement to share and persist resources across tabs, particularly for technologies like WASM-based SQLite.
  * **Closing a feature gap** : Other major mobile browsers, including Safari on iOS and Firefox on Android, already support SharedWorker, making Chrome on Android the last major browser to address this gap.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921) | [ChromeStatus.com entry](https://chromestatus.com/feature/6265472244514816) | [Spec](https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface)
