# Chrome 140 - Origin Trials Analysis

## Area Summary

Chrome 140 brings four significant origin trials that expand web platform capabilities in communication, debugging, clipboard integration, and multi-threading. The most impactful changes include incoming call notifications for PWAs, crash reporting diagnostics, real-time clipboard synchronization, and SharedWorker support on Android. These features collectively enhance user experience through better VoIP integration, improved debugging workflows, seamless clipboard operations, and resource-efficient background processing across tabs on mobile platforms.

## Detailed Updates

This release focuses on empowering developers with advanced APIs for communication, diagnostics, and system integration while expanding platform consistency across devices.

### Enable incoming call notifications

#### What's New
This feature extends the Notifications API to allow installed PWAs to send incoming call notifications with call-styled buttons and ringtone support, creating more engaging VoIP experiences.

#### Technical Details
The enhancement builds upon the existing Notifications API by adding specialized call notification types that include native call interface elements and audio capabilities. This allows PWAs to integrate more deeply with the operating system's calling interface.

#### Use Cases
VoIP applications can now provide native-like calling experiences, making it easier for users to recognize and respond to incoming calls. This is particularly valuable for business communication tools, video conferencing platforms, and messaging applications with voice calling features.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009)
- [Tracking bug #detail?id=1383570](https://issues.chromium.org/issues/detail?id=1383570)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5110990717321216)
- [Spec](https://notifications.spec.whatwg.org)

### Crash Reporting key-value API

#### What's New
This feature introduces a new key-value API, tentatively `window.crashReport`, that allows developers to attach custom debugging data to crash reports for better error analysis.

#### Technical Details
The API maintains a per-document map that holds developer-defined data, which gets automatically included in the `CrashReportBody` when renderer process crashes occur. This provides contextual information that can help diagnose the circumstances leading to crashes.

#### Use Cases
Developers can track user actions, application state, feature flags, or custom metrics that provide crucial context for debugging crashes. This is especially valuable for complex web applications where understanding the user's journey before a crash is essential for root cause analysis.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905)
- [Tracking bug #400432195](https://issues.chromium.org/issues/400432195)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6228675846209536)
- [Spec](https://github.com/WICG/crash-reporting/pull/37)

### Add the `clipboardchange` event

#### What's New
The `clipboardchange` event fires whenever the system clipboard contents change, whether from the current web app or any other system application, enabling real-time clipboard synchronization.

#### Technical Details
This event provides an efficient alternative to polling the clipboard by automatically notifying applications of changes. It works across the entire system, not just within the browser context, allowing for comprehensive clipboard monitoring.

#### Use Cases
Remote desktop clients can maintain synchronized clipboards between local and remote systems. Clipboard managers, productivity tools, and collaborative applications can provide seamless copy-paste experiences across different contexts and applications.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/137922738588221441)
- [Tracking bug #41442253](https://issues.chromium.org/issues/41442253)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5085102657503232)
- [Spec](https://github.com/w3c/clipboard-apis/pull/239)

### Enable `SharedWorker` on Android

#### What's New
SharedWorker support is now available on Android through origin trials, addressing long-standing developer requests for cross-tab resource sharing and background processing capabilities on mobile platforms.

#### Technical Details
SharedWorkers enable multiple browser contexts (tabs, windows) to share a single background thread, allowing for efficient resource utilization and state management across multiple instances of the same web application.

#### Use Cases
Developers can now share WebSocket connections or Server-Sent Events across multiple tabs on Android, conserving bandwidth and battery life. This enables better resource management for chat applications, real-time collaboration tools, and any web app that benefits from persistent background connections.

#### References
- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6265472244514816)
- [Spec](https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface)