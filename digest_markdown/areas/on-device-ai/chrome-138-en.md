---
layout: default
title: Area Summary
---

# Area Summary

The Chrome 138 On-device AI update centers on the new Summarizer API, a JavaScript interface that exposes a built-in language model for producing text summaries. This reduces the need for sites to bundle or fetch multi-gigabyte models, improving performance, bandwidth, and privacy by enabling locally-available summaries. For developers, the most impactful change is a standardized web API for summarization that can be integrated into web apps without external model hosting. These capabilities advance the web platform by bringing AI-native text processing into the browser runtime, enabling richer client-side features.

## Detailed Updates

Below are the explicit changes in this release relevant to On-device AI and how developers can use them.

### Summarizer API

#### What's New
The Summarizer API is a JavaScript API that produces summaries of input text using a built-in AI language model available to the browser/OS. By exposing this model via a standard API, sites can use summarization without downloading their own large models.

#### Technical Details
The API surfaces model-backed summarization functionality to web pages via JavaScript. The underlying design assumes browsers or the host OS will provide access to a local language model implementation, allowing the API to run without per-site model downloads. See the specification for surface details and the Chromium tracking entry for status.

#### Use Cases
- Inline article or transcript summarization in the browser to improve reading workflows.
- Client-side summarization for privacy-sensitive content (keeps text local).
- Reduced latency and bandwidth vs. fetching remote summarization services or shipping large models.
- Enabling progressive enhancement: sites can call the API when available, falling back otherwise.

#### References
- https://developer.mozilla.org/docs/Web/API/Summarizer
- https://bugs.chromium.org/p/chromium/issues/detail?id=351744634
- https://chromestatus.com/feature/5134971702001664
- https://wicg.github.io/summarization-api/

## Area-Specific Expertise Notes

- css: Summarization outputs typically integrate into UI flows; consider responsive layout for variable-length summaries and ARIA for accessible readouts.
- webapi: The Summarizer API fits the progressive enhancement model — feature-detect and provide fallbacks.
- graphics-webgpu: On-device AI may share GPU resources; coordinate heavy compute with rendering budgets to avoid jank.
- javascript: Use async patterns (Promises/async-await) to call the API without blocking the main thread; offload work to Web Workers if post-processing is heavy.
- security-privacy: Favor local summarization to minimize data exfiltration; review CSP and permissions models when integrating.
- performance: Leverage the on-device model to reduce network latency; benchmark memory/CPU on target devices.
- multimedia: Summaries of transcripts or captions can be generated client-side to enhance media UX.
- devices: Device capability detection is important—fallback for low-resource devices.
- pwa-service-worker: Consider caching summarized results and offline strategies via service workers.
- webassembly: If polyfills or local model runtimes are needed, WASM can be an implementation path.
- deprecations: Adopt the standardized API to avoid bespoke client-side models that increase bundle size.

Save path:
```text
digest_markdown/webplatform/On-device AI/chrome-138-stable-en.md
