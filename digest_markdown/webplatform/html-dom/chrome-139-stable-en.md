## Area Summary

Chrome 139 (stable) delivers two HTML-DOM–relevant updates: a networking change that randomizes TCP ephemeral port allocation on modern Windows, and a relaxation of character validation for JavaScript DOM creation APIs so they align better with the HTML parser. The port-randomization change reduces risks from rapid port reuse, while the DOM validation change removes a class of developer friction when creating elements/attributes from script. Together these changes improve platform robustness and interoperability, reducing subtle failures in networking and DOM construction workflows.

## Detailed Updates

The following entries expand on each change, emphasizing developer impact and technical pointers.

### Randomize TCP port allocation on Windows

#### What's New
Enables TCP port randomization on Windows versions (2020 or later) where rapid reuse of prior ports is not expected to cause rejection due to timeouts.

#### Technical Details
The change adjusts ephemeral TCP port allocation behavior on supported Windows builds to introduce randomness and reduce collisions that stem from rapid port reuse (a manifestation of the Birthday problem). This is a platform-level networking mitigation that Chrome enables where safe.

#### Use Cases
- Reduces intermittent connection failures for browser network clients and WebRTC flows caused by port reuse timing.
- Improves reliability of parallel connections and automated test runs that open many short-lived sockets.
- Developers should be aware of slightly different ephemeral port distributions when diagnosing connection-level issues.

#### References
- https://issues.chromium.org/issues/40744069
- https://chromestatus.com/feature/5106900286570496

### Allow more characters in JavaScript DOM APIs

#### What's New
Relaxes validation in JavaScript DOM creation APIs so element and attribute names accepted by the HTML parser are also accepted when created via DOM APIs.

#### Technical Details
Historically the HTML parser permitted a wide variety of valid characters in element/attribute names while JS DOM APIs enforced stricter validation. This change aligns the JavaScript-facing validation with the parser’s rules and the relevant namespace handling per the spec.

#### Use Cases
- Scripts can create elements and attributes that previously failed validation, improving parity with server-generated markup and authoring tools.
- Facilitates interoperability when working with nonstandard or internationalized names and when migrating markup-generation code to client-side APIs.
- Developers should consult namespace rules in the spec when creating names across XML/HTML namespaces.

#### References
- https://issues.chromium.org/issues/40228234
- https://chromestatus.com/feature/6278918763708416
- https://dom.spec.whatwg.org/#namespaces

Save path:
digest_markdown/webplatform/HTML-DOM/chrome-139-stable-en.md