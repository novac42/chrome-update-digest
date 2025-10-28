---
layout: default
title: Area Summary
---

# Area Summary

Chrome 136 introduces a privacy-oriented change in Navigation-Loading: the HTTP cache key now includes an `is-cross-site-main-frame-navigation` boolean. This change targets cross-site leak attacks that exploit top-level navigations to infer cache state. For developers, the most impactful effect is that cache keying and thus cache hits/misses can differ based on navigation initiator, which may affect caching assumptions and testing. Overall, the update strengthens cache partitioning to advance web privacy without changing cache semantics defined by HTTP caching specs.

## Detailed Updates

Below are the details for the Navigation-Loading change in Chrome 136 and what developers should know.

### Incorporate navigation initiator into the HTTP cache partition key

#### What's New
Chrome's HTTP cache keying scheme is updated to include an `is-cross-site-main-frame-navigation` boolean to mitigate cross-site leak attacks involving top-level navigation.

#### Technical Details
- The cache partition key now encodes whether a request was initiated by a cross-site top-level navigation (`is-cross-site-main-frame-navigation`).
- This boolean differentiates cache entries so that resources fetched as part of such navigations are keyed separately, reducing the risk that an attacker can infer cache state by triggering navigations.
- The change builds on standard HTTP caching behavior while adding an origin-navigation context to keying.

#### Use Cases
- Improves privacy for sites vulnerable to cross-site probing via top-level navigations.
- Relevant for developers relying on deterministic cache hit behavior during navigation-driven flows—test and validate caching logic where navigation initiator matters.
- Impacts cache analysis, automated tests, and security reviews for navigation-heavy apps (including PWAs and sites with cross-origin redirects).

#### References
- [Tracking bug #398784714](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5108419906535424)
- [Spec](https://httpwg.org/specs/rfc9110.html#caching)

## Area-Specific Expertise (Navigation-Loading focused)

- css: Layout and painting are unaffected by cache keying; however, resource timing and cache status can change rendering performance on navigations.
- webapi: Fetch and caching behavior may return different cache hits for navigation-initiated requests; verify Fetch API and navigation preload interactions.
- graphics-webgpu: No direct effect on GPU pipelines, but altered cache hits can change resource fetch timing that impacts GPU upload latency.
- javascript: V8 and script-driven navigations should be tested for cache-dependent logic (e.g., navigation-driven module fetching).
- security-privacy: This change closes a class of cross-site cache-probing attacks by scoping cache entries based on navigation context.
- performance: Expect potential cache hit-rate shifts; measure end-to-end navigation latency after the change.
- multimedia: Media resource caching for top-level navigations may be partitioned differently; validate streaming startup behavior.
- devices: Hardware-initiated navigations are unlikely to be affected, but caching semantics remain important for sensor-driven UX.
- pwa-service-worker: Service worker cache usage and expectations should be audited—service worker-controlled responses still follow HTTP caching rules but navigation context may alter keying.
- webassembly: WASM module fetches during navigations may see different cache results; prefetching strategies should be revalidated.
- deprecations: No deprecations announced; treat this as an interoperability/behavioral change and update tests accordingly.

Save to: digest_markdown/webplatform/Navigation-Loading/chrome-136-stable-en.md
