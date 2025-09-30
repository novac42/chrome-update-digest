---
layout: default
title: origin-trials-en
---

## Detailed Updates

Below are concise, developer-focused breakdowns of each Origin Trial introduced in Chrome 140 stable, tied to the summary above.

### Enable incoming call notifications

#### What's New
An extension to the Notifications API enabling installed PWAs to send incoming call notifications that include call-styled action buttons and a ringtone for more recognizable, answerable VoIP notifications.

#### Technical Details
- Implemented as a Notifications API extension surfaced via an Origin Trial token for sites that register.
- Targets installed PWAs to present richer notification UI and auditory feedback; integration relies on platform notification plumbing.
- Relevant areas: webapi, multimedia, devices, pwa-service-worker, security-privacy (user consent and notification permissions).

#### Use Cases
- VoIP and teleconferencing web apps presenting native-like incoming call prompts.
- Improving user engagement and reducing missed calls by surfacing ringtone and dedicated action buttons.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/2876111312029483009
- https://issues.chromium.org/issues/detail?id=1383570
- https://chromestatus.com/feature/5110990717321216
- https://notifications.spec.whatwg.org

### Crash Reporting key-value API

#### What's New
A tentative window.crashReport key-value API that exposes a per-document map for attaching key/value data to be included in CrashReportBody when renderer crashes occur.

#### Technical Details
- API surface: per-document map accessible from scripts; entries are serialized into CrashReportBody on renderer crash.
- Intended to aid post-crash diagnostics without server-side instrumentation; must be evaluated for privacy and data leak risks.
- Relevant areas: webapi, security-privacy, performance (debugging impact), deprecations (migration from custom logging patterns).

#### Use Cases
- Attaching contextual debug metadata (state identifiers, feature flags) to aid crash triage.
- Improving fidelity of crash analytics for complex single-page apps and PWAs.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/1304355042077179905
- https://issues.chromium.org/issues/400432195
- https://chromestatus.com/feature/6228675846209536
- https://github.com/WICG/crash-reporting/pull/37

### Add the `clipboardchange` event

#### What's New
A DOM event that fires when the system clipboard changes, enabling web apps to synchronize their internal clipboard state without polling.

#### Technical Details
- The event is dispatched to pages that opt in via the Origin Trial; it reflects system-level clipboard changes originating from any app.
- Designers must consider user privacy and permission models because clipboard contents can contain sensitive data.
- Relevant areas: webapi, security-privacy, performance, devices (input), multimedia (text/media clipboard).

#### Use Cases
- Remote desktop and collaboration apps keeping local and remote clipboards synchronized efficiently.
- Eliminating expensive periodic clipboard polling, reducing CPU and battery usage.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/137922738588221441
- https://issues.chromium.org/issues/41442253
- https://chromestatus.com/feature/5085102657503232
- https://github.com/w3c/clipboard-apis/pull/239

### Enable `SharedWorker` on Android

#### What's New
An Origin Trial enabling SharedWorker support on Android to allow multiple browsing contexts (tabs) to share a single worker instance.

#### Technical Details
- Enables SharedWorker API on Android builds behind an Origin Trial token so sites can test cross-tab shared scripts and connections.
- Addresses resource-sharing scenarios like a shared WebSocket or SSE connection to reduce redundant network and CPU work.
- Relevant areas: webapi, performance, pwa-service-worker, devices, security-privacy (origin isolation and lifetime).

#### Use Cases
- Sharing a single WebSocket/SSE across multiple tabs to reduce connections and memory footprint.
- Centralized coordination between tabs for caching, state sync, and background work on mobile.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/4101090410674257921
- https://chromestatus.com/feature/6265472244514816
- https://html.spec.whatwg.org/multipage/workers.html#shared-workers-and-the-sharedworker-interface

Saved file path: digest_markdown/webplatform/Origin trials/chrome-140-stable-en.md
