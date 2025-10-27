---
layout: default
title: chrome-134-en
---

## Area Summary

Chrome 134's Performance updates focus on giving developers finer control over resource lifetimes, reducing unnecessary speculative work during page load, and improving high-performance instrumentation for accurate measurements. The most impactful changes are explicit resource management (both async and sync variants), a Document Policy hook to opt out of speculative linked-resource processing, and an expanded console.timeStamp API for richer timing data in DevTools. Together these features advance the platform by enabling deterministic cleanup, fewer wasted fetches/CPU during load, and higher-fidelity runtime diagnostics—important for optimizing memory, startup, and runtime performance.

## Detailed Updates

Below are concise, developer-focused descriptions of each Performance-area feature from Chrome 134, with implementation context and practical use cases.

### Document-Policy: `expect-no-linked-resources`

#### What's New
The `expect-no-linked-resources` configuration point in Document Policy lets a document hint to the user agent to optimize its loading sequence, for example by avoiding the default speculative parsing behavior for linked resources.

#### Technical Details
This hint informs the UA's HTML parsing/fetching heuristics so it may skip speculative parsing and speculative fetches of linked resources that would otherwise be triggered by standard parsing optimizations.

#### Use Cases
- Pages or embedded documents that intentionally have no linked resources (stylesheets, scripts, preloads) can reduce wasted network requests and CPU by opting out of speculative parsing.
- Single-page apps or isolated widgets that control their resource fetching can avoid redundant speculative fetches during startup.

#### References
- Tracking bug #365632977: https://issues.chromium.org/issues/365632977
- ChromeStatus.com entry: https://chromestatus.com/feature/5202800863346688
- Spec: https://github.com/whatwg/html/pull/10718

### Explicit resource management (async)

#### What's New
Adds language-level features to address a common pattern of allocating and explicitly releasing resources in asynchronous contexts, improving deterministic cleanup for memory and I/O.

#### Technical Details
These features expose APIs and semantics that let asynchronous code explicitly release critical resources when no longer needed, aligning allocation and release patterns in async flows.

#### Use Cases
- Async APIs that manage file handles, streams, or network connections can expose deterministic release operations to reduce resource retention and GC pressure.
- Long-running web apps and PWAs can reduce memory and handle leaks by explicitly releasing resources when logical tasks complete.

#### References
- Tracking bug #42203814: https://issues.chromium.org/issues/42203814
- ChromeStatus.com entry: https://chromestatus.com/feature/5087324181102592
- Spec: https://tc39.es/proposal-explicit-resource-management

### Explicit resource management (sync)

#### What's New
Provides synchronous counterparts for explicit resource management, enabling deterministic release of resources in non-async code paths.

#### Technical Details
These sync features follow the same allocation/release pattern but are designed for synchronous usage patterns where immediate cleanup semantics are required.

#### Use Cases
- Low-level APIs and libraries that need immediate resource reclamation (e.g., graphics or device handles) can provide synchronous release mechanisms to avoid deferred cleanup.
- Developers porting native-like resource management patterns to JS can model predictable lifetimes without relying solely on GC.

#### References
- Tracking bug #42203506: https://issues.chromium.org/issues/42203506
- ChromeStatus.com entry: https://chromestatus.com/feature/5071680358842368
- Spec: https://tc39.es/proposal-explicit-resource-management

### Extend the `console.timeStamp` API to support measurements and presentation options

#### What's New
Extends console.timeStamp() in a backwards-compatible way to provide a high-performance method for instrumentation and for surfacing timing data to the Performance panel in DevTools. New entries can include custom timestamps, durations, and presentation options.

#### Technical Details
The API extension produces Performance-panel-compatible timing entries with optional metadata (timestamp, duration, presentation flags) while preserving existing console.timeStamp behavior for older uses.

#### Use Cases
- Low-overhead instrumentation for measuring sub-task durations without the heavier performance.mark/measure workflow.
- Annotating timeline data in DevTools with custom presentation to make performance traces more actionable for optimization.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5133241999425536
- Spec: https://docs.google.com/document/d/1juT7esZ62ydio-SQwEVsY7pdidKhjAphvUghWrlw0II/edit?tab=t.0#heading=h.ekp1q3o1v7v3
