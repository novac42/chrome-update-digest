---
layout: default
title: chrome-140-en
---

## Area Summary

Chrome 140's Web API updates focus on improving robustness, native-integration, and server-side integrity. Key changes let developers control stream read guarantees, detect related desktop apps from the web, and distinguish server-set cookies for security-sensitive workflows. These updates advance the platform by tightening I/O semantics, expanding web-to-native discovery on desktops, and strengthening cookie attribution to mitigate client-side tampering. Together they reduce ambiguity in data handling, enable richer install-aware experiences, and harden server-side trust boundaries.

## Detailed Updates

The items below expand on the summary above and describe developer-facing impacts and technical notes for each Web API feature in Chrome 140.

### `ReadableStreamBYOBReader` `min` option

#### What's New
Adds a `min` option to ReadableStreamBYOBReader.read(view) so callers can request a minimum number of elements be written into the provided ArrayBufferView before the read resolves.

#### Technical Details
The change extends the BYOB read semantics defined in the Streams spec to accept a `min` constraint alongside the existing view buffer. The read promise will now resolve only when at least `min` elements are available (subject to stream end/errored conditions), reducing partial-read indeterminacy. See the WHATWG streams spec for authoritative behavior.

#### Use Cases
- Deterministic binary protocol parsing where a minimum frame size is required before processing.
- Reducing application-level buffering and retries by ensuring larger, useful reads.
- Improved performance for streaming parsers that prefer full records over incremental fragments.

#### References
- https://issues.chromium.org/issues/40942083 (Tracking bug #40942083)
- https://chromestatus.com/feature/6396991665602560 (ChromeStatus.com entry)
- https://streams.spec.whatwg.org/#byob-reader-read (Spec)

### Get Installed Related Apps API on desktop

#### What's New
The Get Installed Related Apps API (navigator.getInstalledRelatedApps) is available on desktop, allowing sites to check whether associated native applications are installed for the origin.

#### Technical Details
The API returns information only when the native application has an established association with the web origin (linking must be verified). This desktop rollout extends the existing capability (previously focused on mobile) and keeps association checks as the gate for privacy-preserving discovery. Historical context: the API was initially launched in Chrome 80.

#### Use Cases
- Offer deep-linking or "open in app" prompts only when the matching desktop app is present.
- Improve install engagement flows by tailoring UI when a companion app is detected.
- Progressive enhancement for PWAs and installable experiences across desktop platforms.

#### References
- https://issues.chromium.org/issues/895854 (Tracking bug #895854)
- https://chromestatus.com/feature/5695378309513216 (ChromeStatus.com entry)
- https://wicg.github.io/get-installed-related-apps/spec (Spec)

### Http cookie prefix

#### What's New
Introduces server-side cookie attribution semantics to distinguish cookies set by the server from those set client-side, addressing cases where certain cookies are expected to originate only from the server.

#### Technical Details
This feature provides a mechanism to mark or recognize cookies that should be treated as server-originated, helping servers identify unexpected client-set cookies (which could stem from XSS, malicious extensions, or developer mistakes). The change is tracked and specified in the linked HTTP extensions PR and tracking bug.

#### Use Cases
- Enforce server-only cookie invariants and detect client-side tampering.
- Strengthen security-sensitive flows (authentication, session management) by ensuring certain cookies are only writable by the server.
- Aid incident response by making unexpected client-set cookies easier to flag and remediate.

#### References
- https://issues.chromium.org/issues/426096760 (Tracking bug #426096760)
- https://chromestatus.com/feature/5170139586363392 (ChromeStatus.com entry)
- https://github.com/httpwg/http-extensions/pull/3110 (Spec)
