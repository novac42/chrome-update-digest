## Deprecations and removals

### Deprecate and remove: Private Aggregation API

The Private Aggregation API is a generic mechanism for measuring aggregate, cross-site data in a privacy-preserving manner. It was originally designed for a future without third-party cookies.

Following Chrome's announcement that the current approach to third-party cookies will be maintained, Chrome plans to deprecate and remove the Private Aggregation API (along with certain other Privacy Sandbox APIs, as outlined on the Privacy Sandbox feature status page). This API is only exposed through the Shared Storage and Protected Audience APIs, which are also planned for deprecation and removal. Therefore, no additional work is required for Private Aggregation.

[ChromeStatus.com entry](https://chromestatus.com/feature/4683382919397376) | [Spec](https://patcg-individual-drafts.github.io/private-aggregation-api)

### Deprecate and Remove: Shared Storage API

The Shared Storage API is a privacy-preserving web API that enables storage not partitioned by a first-party site.

Following Chrome's announcement that the current approach to third-party cookies will be maintained, Chrome plans to deprecate and remove the Shared Storage API (along with certain other Privacy Sandbox APIs, as outlined on the Privacy Sandbox feature status page).

[Tracking bug #462465887](https://issues.chromium.org/issues/462465887) | [ChromeStatus.com entry](https://chromestatus.com/feature/5076349064708096) | [Spec](https://wicg.github.io/shared-storage)

### Deprecate and Remove Protected Audience

The Protected Audience API provides a method of interest-group advertising without third-party cookies or user tracking across sites.

Following Chrome's announcement that the current approach to third-party cookies will be maintained, Chrome plans to deprecate and remove the Protected Audience API (along with certain other Privacy Sandbox APIs, as outlined on the Privacy Sandbox feature status page).

[ChromeStatus.com entry](https://chromestatus.com/feature/6552486106234880) | [Spec](https://wicg.github.io/turtledove)

### Externally loaded entities in XML parsing

Chrome synchronously fetches external XML entities or DTDs and incorporates them into parsing under specific circumstances. This document proposes removing this functionality.

For example, `http/tests/security/contentTypeOptions/xml-external-entity.xml` shows how external entities can be defined in the trailing part of the `DOCTYPE` statement. These entities then refer to resources that are synchronously loaded and included as context when parsing XML.

Another syntax example is a `DOCTYPE` that, using the `SYSTEM` keyword followed by a URL, points to a DTD that contains additional entity definitions.

The parser passes up such external load requests.

According to the XML specification, non-validating processors are not required to read external entities.

Chrome plans to deprecate loading external entity definitions in XML documents that don't use XSLT.

[Tracking bug #455813733](https://issues.chromium.org/issues/455813733) | [ChromeStatus.com entry](https://chromestatus.com/feature/6734457763659776) | [Spec](https://www.w3.org/TR/xml/#proc-types)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-01-13 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-01-13 UTC."],[],[]] 
