---
layout: default
title: Chrome 144 Stable - Deprecations and Removals
---

# Chrome 144 Stable - Deprecations and Removals

## Area Summary

Chrome 144 marks a significant shift in the Privacy Sandbox initiative, with the deprecation and removal of three key Privacy Sandbox APIs: Private Aggregation, Shared Storage, and Protected Audience. Following Chrome's announcement to maintain the current approach to third-party cookies, these APIs—originally designed for a cookieless future—are being phased out. Additionally, Chrome 144 addresses a security concern by deprecating externally loaded entities in XML parsing, which reduces synchronous network requests and potential attack vectors. These changes reflect Chrome's evolving approach to privacy and security while simplifying the platform for developers.

## Detailed Updates

Chrome 144's deprecations focus on streamlining the web platform by removing Privacy Sandbox APIs that are no longer aligned with Chrome's third-party cookie strategy, while also addressing XML security concerns.

### Deprecate and remove: Private Aggregation API

#### What's New

The Private Aggregation API, designed to measure aggregate cross-site data in a privacy-preserving manner, is being deprecated and removed from Chrome. This API was part of the original Privacy Sandbox vision for a web without third-party cookies.

#### Technical Details

The Private Aggregation API was only exposed through the Shared Storage and Protected Audience APIs. Since both parent APIs are also being deprecated, no additional developer action is required specifically for Private Aggregation. The removal is automatic as the dependent APIs are removed.

#### Why This Matters

With Chrome maintaining its current approach to third-party cookies, the Privacy Aggregation API no longer serves its intended purpose. The removal simplifies the platform and eliminates APIs that would otherwise remain unused in the ecosystem.

#### References

- [ChromeStatus.com entry](https://chromestatus.com/feature/4683382919397376)
- [Spec](https://patcg-individual-drafts.github.io/private-aggregation-api)

### Deprecate and Remove: Shared Storage API

#### What's New

The Shared Storage API, which enables storage not partitioned by first-party site, is being deprecated and removed. This API was designed as a privacy-preserving storage mechanism for the post-third-party-cookie web.

#### Technical Details

Shared Storage provided unpartitioned storage capabilities while maintaining privacy guarantees through limited output channels. However, with third-party cookies remaining available, the API's original use cases are no longer applicable in the current Chrome architecture.

#### Migration Path

Developers using Shared Storage should transition back to standard storage mechanisms appropriate for their use cases, such as first-party cookies, localStorage, or IndexedDB, depending on their partitioning requirements.

#### References

- [Tracking bug #462465887](https://issues.chromium.org/issues/462465887)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5076349064708096)
- [Spec](https://wicg.github.io/shared-storage)

### Deprecate and Remove Protected Audience

#### What's New

The Protected Audience API (formerly FLEDGE), which provided interest-group-based advertising without third-party cookies or cross-site tracking, is being deprecated and removed from Chrome.

#### Technical Details

Protected Audience enabled on-device ad auctions based on interest groups, allowing advertisers to reach relevant audiences while preserving user privacy. The API included components for joining interest groups, running auctions, and rendering ads in isolated contexts.

#### Impact on Developers

Developers who implemented Protected Audience for advertising use cases should evaluate alternative approaches within the context of continued third-party cookie availability. The removal timeline follows Chrome's Privacy Sandbox feature status page.

#### References

- [ChromeStatus.com entry](https://chromestatus.com/feature/6552486106234880)
- [Spec](https://wicg.github.io/turtledove)

### Externally loaded entities in XML parsing

#### What's New

Chrome is deprecating the loading of external entity definitions in XML documents that don't use XSLT. This removes synchronous fetching of external XML entities and DTDs during parsing.

#### Technical Details

Currently, Chrome synchronously fetches external XML entities or DTDs under specific circumstances, such as when external entities are defined in the DOCTYPE statement or when a DOCTYPE uses the SYSTEM keyword to point to an external DTD. The XML specification does not require non-validating processors to read external entities, giving Chrome the flexibility to remove this behavior.

#### Security and Performance Benefits

Removing external entity loading eliminates synchronous network requests during XML parsing, reducing both security risks (such as XML External Entity attacks) and performance overhead. Documents using XSLT will continue to support external entities where necessary for transformation processing.

#### Migration Guidance

Developers should inline necessary entity definitions within XML documents rather than relying on external references. For complex scenarios requiring external definitions, consider preprocessing XML documents or migrating to JSON-based data formats.

#### References

- [Tracking bug #455813733](https://issues.chromium.org/issues/455813733)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6734457763659776)
- [Spec](https://www.w3.org/TR/xml/#proc-types)
