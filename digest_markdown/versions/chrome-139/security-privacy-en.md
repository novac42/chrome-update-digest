---
layout: default
title: security-privacy-en
---

## Area Summary

Chrome 139 aligns worker creation behavior with the CSP3 fetch integration spec by checking Content Security Policy during fetch and firing an asynchronous error event instead of throwing on "new Worker(url)" or "new SharedWorker(url)". This change reduces unexpected exceptions in page scripts and gives developers an event-driven failure mode to handle CSP-blocked worker loads. For web platform security, it improves consistency across user agents and makes CSP enforcement observable without breaking script flow. Developers should update error handling for worker creation to listen for error events rather than relying on catchable exceptions.

## Detailed Updates

The single Security-Privacy update below expands on how Chrome changes worker failure behavior under CSP and what developers should do to adjust.

### Fire error event for Content Security Policy (CSP) blocked worker

#### What's New
Chrome now checks Content Security Policy during the fetch used to create Worker and SharedWorker, and when CSP blocks the fetch it fires an asynchronous error event instead of throwing a synchronous exception from "new Worker(url)" or "new SharedWorker(url)".

#### Technical Details
- Behavior change implements the CSP3 fetch integration guidance: CSP is evaluated during the worker fetch and a blocked fetch results in an error event dispatched to the worker object.
- The error is emitted asynchronously, preserving script execution flow and avoiding synchronous exceptions thrown at the time of construction.
- This aligns Chrome with the spec and the tracked implementation effort referenced in the Chromium bug.

#### Use Cases
- Robust worker creation: Service authors can attach "error" handlers to Worker/SharedWorker instances to detect CSP rejections and implement fallback strategies (e.g., load alternative scripts, notify the user, or degrade functionality).
- Error telemetry: Observability improves because blocked fetches emit events that can be logged without try/catch wrapping worker construction.
- Progressive enhancement: Single-page apps and PWAs can avoid tearing down initialization flows due to unexpected exceptions and instead handle worker availability dynamically.

#### References
- https://issues.chromium.org/issues/41285169
- https://chromestatus.com/feature/5177205656911872
- https://www.w3.org/TR/CSP3/#fetch-integration

## Area-Specific Expertise and Developer Guidance (Security-Privacy focus)

- security-privacy: This change clarifies CSP enforcement semantics for worker fetches; audit code to attach "error" listeners on Workers and SharedWorkers and avoid relying on constructor exceptions.
- pwa-service-worker: For PWAs, ensure service worker registration and worker-based features handle asynchronous failure events and provide fallbacks offline.
- webapi & javascript: Update client-side patterns to use event-driven error handling for worker lifecycle instead of try/catch around constructors; this aligns with event-based DOM APIs.
- deprecations & performance: No deprecation here, but review initialization paths to prevent performance regressions when adding error listeners and fallback logic.
- Other areas (css, graphics-webgpu, multimedia, devices, webassembly): While not directly affected, cross-team awareness is useful where worker usage touches these domains (e.g., offloading heavy compute via workers for WebGPU or WASM).
