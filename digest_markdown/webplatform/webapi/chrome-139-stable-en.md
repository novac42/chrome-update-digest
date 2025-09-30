## Area Summary

Chrome 139's Web API updates focus on standardization, cross-origin app boundaries, predictable feature detection, and clearer telemetry routing. Key changes let web apps extend scopes across origins, make JSON MIME detection fully WHATWG-compliant, signal WebGPU adapters/devices that meet core spec features and limits, and allow delivery of only crash reports to a dedicated endpoint. These advances improve interoperability, developer predictability, and operational clarity for platform-integrated features. Developers should evaluate manifest, content-type handling, GPU capability assumptions, and crash-reporting configuration in light of these changes.

## Detailed Updates

The following entries expand on the summary above and present what changed, how it works, practical developer use cases, and links to tracking/spec resources.

### Web app scope extensions

#### What's New
Adds a `scope_extensions` web app manifest field that enables web apps to extend their scope to other origins, allowing sites that control multiple subdomains and top level domains to be presented as a single web app. Listed origins must confirm association with the web app using a `.well-known` association.

#### Technical Details
This is a manifest-level extension that requires origin verification via the indicated association mechanism. Implementation and tracking are coordinated via the Chromium tracking bug and a spec PR.

#### Use Cases
Unify multi-origin properties (subdomains, related top-level domains) into a single PWA install/launch experience; simplify navigation, sharing, and service worker expectations across related origins.

#### References
- https://issues.chromium.org/issues/detail?id=1250011 (Tracking bug #detail?id=1250011)  
- https://chromestatus.com/feature/5746537956114432 (ChromeStatus.com entry)  
- https://github.com/WICG/manifest-incubations/pull/113 (Spec)

### Specification-compliant JSON MIME type detection

#### What's New
Chrome now recognizes all valid JSON MIME types per the WHATWG mimesniff specification, including any subtype ending with `+json`, in addition to `application/json` and `text/json`. This makes JSON detection consistent with the spec.

#### Technical Details
MIME type recognition logic was updated to follow the WHATWG mimesniff rules for JSON. This affects any feature or API path that branches behavior based on detected JSON content types.

#### Use Cases
APIs and client-side code that rely on content-type checks will see more consistent parsing/handling of JSON payloads when servers use `+json` vendor or vendor-tree subtypes; reduces surprises when interoperating with APIs using custom JSON-like MIME types.

#### References
- https://chromestatus.com/feature/5470594816278528 (ChromeStatus.com entry)  
- https://mimesniff.spec.whatwg.org/#json-mime-type (Spec)

### WebGPU `core-features-and-limits`

#### What's New
Introduces the `core-features-and-limits` feature flag/status to signify that a WebGPU adapter and device support the core features and limits defined by the GPUWeb spec.

#### Technical Details
Adapters/devices that advertise this feature meet the spec's baseline features and limits. Tracking and specification alignment are documented in the referenced tracking bug and spec section.

#### Use Cases
Graphics and compute applications can query for and rely on a well-defined baseline of WebGPU capabilities, simplifying capability negotiation and fallback strategies in high-performance rendering and GPU compute scenarios.

#### References
- https://issues.chromium.org/issues/418025721 (Tracking bug #418025721)  
- https://chromestatus.com/feature/4744775089258496 (ChromeStatus.com entry)  
- https://gpuweb.github.io/gpuweb/#core-features-and-limits (Spec)

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports

#### What's New
Developers can specify an endpoint named `crash-reporting` so that only crash reports are delivered to that endpoint. By default, the `default` endpoint receives many report types; this feature separates crash delivery for focused telemetry.

#### Technical Details
The crash-reporting endpoint is configured via the well-known endpoint name in the Crash Reporting API. This allows a different URL to be used solely for crash reports, distinct from broader report delivery endpoints.

#### Use Cases
Teams that want crash-only telemetry to go to a dedicated ingestion pipeline (for storage, alerting, or privacy separation) can configure the `crash-reporting` endpoint to avoid noise from other report types and minimize downstream filtering.

#### References
- https://issues.chromium.org/issues/414723480 (Tracking bug #414723480)  
- https://chromestatus.com/feature/5129218731802624 (ChromeStatus.com entry)  
- https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority (Spec)