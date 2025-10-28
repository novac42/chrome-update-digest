---
layout: default
title: chrome-139-en
---

## Area Summary

Chrome 139 (stable) tightens background resource controls on Android by shortening the time before background pages and their associated workers are frozen from five minutes to one minute. This change is the main Performance theme in this release and most impactful for developers who rely on prolonged background execution. It advances the web platform by reducing idle CPU and battery usage on mobile devices. Teams should treat longer-running background tasks as fragile and adapt to more aggressive freezing behavior.

## Detailed Updates

Below are the Performance-focused updates connected to the summary above.

### Faster background freezing on Android

#### What's New
Shortens the time to freezing background pages (and associated workers) from five minutes to one minute on Android.

#### Technical Details
Chrome now reduces the threshold for freezing inactive background contexts on Android to one minute, enforcing earlier suspension of background pages and any workers tied to them. Tracking and status information is available via the provided links.

#### Use Cases
- Mobile sites and apps that perform background processing should assume a shorter window for continued execution and move work to foreground interactions or server-side processing.
- Background timers, long-running WebWorkers, or any background polling logic may be frozen earlier; use foreground triggers, push messages, or other platform mechanisms to resume work when needed.
- Overall benefit is reduced CPU and battery consumption on Android devices, improving perceived performance and device longevity.

#### References
- [Tracking bug](https://issues.chromium.org/issues/435623337)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

Save path: `digest_markdown/webplatform/Performance/chrome-139-stable-en.md`
