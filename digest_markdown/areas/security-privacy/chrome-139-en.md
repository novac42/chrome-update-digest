---
layout: default
title: chrome-139-en
---

## Area Summary

Chrome 139 tightens CSP integration for worker creation by conforming to the CSP3 spec: CSP is checked during fetch and a worker-blocking CSP now triggers an asynchronous error event instead of a thrown exception. This change affects how developers detect and handle worker load failures and improves predictable, spec-compliant failure semantics. It advances the web platform by aligning Chrome with the W3C CSP fetch-integration behavior, enabling more consistent cross-browser error handling. Teams should update logic that relied on synchronous exceptions around new Worker/new SharedWorker and add robust error-event handling and telemetry.

## Detailed Updates

The single Security-Privacy change in this release refines worker failure semantics under Content Security Policy and is directly relevant to error handling, CSP reporting, and secure script loading patterns.

### Fire error event for Content Security Policy (CSP) blocked worker

#### What's New
Chrome now checks CSP during fetch and, when a worker script is blocked by CSP, fires an asynchronous error event instead of throwing an exception during the call to new Worker(url) or new SharedWorker(url).

#### Technical Details
- CSP evaluation occurs during the fetch for worker scripts per the CSP3 fetch-integration spec.
- When CSP blocks the fetch, the browser does not throw synchronously; it emits an error event on the Worker/SharedWorker object asynchronously.
- This behavior aligns Chrome with the W3C spec and changes observable control flow for worker creation failures.

#### Use Cases
- Update code that wraps new Worker(...) in try/catch to instead attach error listeners (worker.addEventListener('error', ...)) to reliably detect CSP blocks.
- Improve telemetry and CSP reporting by listening for worker error events and logging or reporting CSP-related failures.
- Libraries and frameworks that spawn workers should ensure they register error handlers before or immediately after worker creation to avoid missed failures.

#### References
- Tracking bug #41285169: https://issues.chromium.org/issues/41285169
- ChromeStatus.com entry: https://chromestatus.com/feature/5177205656911872
- Spec: https://www.w3.org/TR/CSP3/#fetch-integration

## Area-Specific Expertise (Security-Privacy focused guidance)

- css: Minimal direct impact; CSP policies that affect inline styles or script-src remain relevant—ensure style/script CSPs are consistent with worker script sources.
- webapi: Worker/SharedWorker creation semantics changed — rely on event-based failure signals rather than synchronous exceptions.
- graphics-webgpu: Worker-hosted GPU work that loads modules should handle asynchronous worker error events for CSP blocks.
- javascript: Do not rely on try/catch around new Worker/new SharedWorker for CSP failures; attach 'error' handlers and propagate errors through Promise-based APIs if needed.
- security-privacy: Aligns runtime enforcement with CSP3; improves observability and consistent enforcement of cross-origin/script-source restrictions.
- performance: Slight timing difference (asynchronous vs synchronous failure) — ensure startup flows tolerate deferred failure callbacks.
- multimedia: Worker-based media processing must handle worker load errors via events for graceful degradation.
- devices: Hardware-accessing code in workers should validate worker availability via error events before assuming capabilities.
- pwa-service-worker: ServiceWorker APIs are not changed by this feature; however, other worker types used by PWAs must handle CSP-block events.
- webassembly: Loading Wasm modules via workers will surface CSP blocks through the error event; add handlers to surface module load failures.
- deprecations: No deprecations here, but code relying on synchronous exceptions should be migrated to the new event-driven error handling.

Save to: digest_markdown/webplatform/Security-Privacy/chrome-139-stable-en.md
