# Chrome 136 Navigation-Loading Updates

## Area Summary

Chrome 136 introduces a significant security enhancement to the Navigation-Loading domain with an updated HTTP cache partition key that incorporates navigation initiator information. This change strengthens the browser's defense against cross-site leak attacks by preventing malicious sites from exploiting cached resources through top-level navigation manipulation. The update represents Chrome's continued commitment to improving web security while maintaining performance benefits of HTTP caching. This security-focused enhancement demonstrates how modern browsers are evolving to address sophisticated attack vectors that target navigation and resource loading mechanisms.

## Detailed Updates

Building on the security improvements outlined above, Chrome 136 delivers a targeted enhancement that addresses a critical vulnerability in how cached resources are accessed across different navigation contexts.

### Incorporate navigation initiator into the HTTP cache partition key

#### What's New
Chrome's HTTP cache keying scheme now includes an `is-cross-site-main-frame-navigation` boolean flag to prevent cross-site leak attacks that exploit top-level navigation patterns. This enhancement adds an additional layer of security to the browser's caching mechanism without compromising performance.

#### Technical Details
The updated cache partition key incorporates navigation context information to distinguish between same-site and cross-site main frame navigations. When a cross-site navigation occurs, the cache partition is modified to prevent attackers from accessing cached resources that could leak sensitive information. This implementation follows HTTP caching specifications while adding security boundaries that weren't previously enforced.

#### Use Cases
This security enhancement protects users from sophisticated attacks where malicious websites attempt to:
- Initiate cross-site navigations to probe for cached resources
- Exploit timing differences in cache hits to infer user browsing history
- Access cached content from other origins through navigation-based attacks

Developers benefit from this automatic protection without needing to modify existing code, as the security enhancement operates transparently within Chrome's navigation and caching systems.

#### References
- [Tracking bug #398784714](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5108419906535424)
- [Spec](https://httpwg.org/specs/rfc9110.html#caching)