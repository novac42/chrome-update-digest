## Area Summary

Chrome 139 (stable) advances Network-area privacy and robustness by limiting identifier surface in client headers and hardening TCP ephemeral port allocation on Windows. The most impactful changes for developers are reduced exposure of full Accept-Language lists (affecting server-side locale detection and fingerprinting) and randomized ephemeral TCP ports (affecting connection reuse characteristics and ephemeral-port predictability). Together these updates push the platform toward privacy-first defaults while improving resilience of the network stack. These changes matter because they alter what information servers can infer from requests and can affect network diagnostics and connection behavior on affected Windows versions.

## Detailed Updates

Below are the Network-area changes in Chrome 139 that follow from the summary above.

### Reduce fingerprinting in Accept-Language header information

#### What's New
Chrome reduces how much information the Accept-Language header and navigator.languages expose: instead of sending the full list of a user's preferred languages on every HTTP request, Chrome sends only the user's most-preferred language.

#### Technical Details
This change restricts the Accept-Language header value string and navigator.languages to limit the surface used for passive fingerprinting. The behavior applies to HTTP request headers and the navigator.languages API.

#### Use Cases
- Server-side localization and content negotiation will see only the top-preference language per request; developers should ensure fallback logic and explicit language negotiation remain robust.
- Reduces passive fingerprinting vectors used by analytics or anti-fraud heuristics.

#### References
- [Tracking bug](https://issues.chromium.org/issues/1306905)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

### Randomize TCP port allocation on Windows

#### What's New
Chrome enables randomized TCP port allocation on Windows versions from around 2020 onward where rapid port re-use is not expected to cause reuse-timeout failures.

#### Technical Details
The rollout randomizes ephemeral TCP ports to avoid collision patterns that can arise from predictable allocation (the release notes cite the Birthday problem as a source of rapid port re-use collisions). The change targets Windows releases where port reuse timings are safe for randomized allocation.

#### Use Cases
- Hardens the network stack against predictability of ephemeral ports, improving privacy and making certain fingerprinting or probing techniques less reliable.
- May alter connection reuse characteristics observed during diagnostics; network tooling and tests that assume deterministic port sequences should be reviewed.

#### References
- [Tracking bug](https://issues.chromium.org/issues/40744069)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

Area-specific notes (Network perspective)
- security-privacy: Both features reduce fingerprinting surface and increase unpredictability in network identifiers.
- performance: Port randomization can affect ephemeral port reuse patterns and timing-sensitive connection behavior; test load and connection-retry logic.
- pwa-service-worker / webapi: Reduced Accept-Language exposure applies to requests originating from service workers and affects client-side language detection APIs.
- deprecations: Server-side localization that relied on full Accept-Language lists should provide explicit preference mechanisms or fallbacks.