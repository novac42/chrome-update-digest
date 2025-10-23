---
layout: default
title: chrome-141-en
---

## Area Summary

Chrome 141 origin trials emphasize security tightening and capability exploration: local network request restrictions with a permission prompt and a temporary opt-in to ease transition, an AI-backed Proofreader API, extended CSP script-src with hash-based allowlisting, and WebAssembly custom descriptors. The most impactful updates are the local network access gating and finer-grained script control, while new APIs expand text assistance and Wasm ergonomics. These trials let teams test, adapt, and provide feedback before defaults solidify. They advance the platform by balancing stronger security with targeted, opt-in innovation.

## Detailed Updates

Below are the Chrome 141 origin trials, with concise technical context, developer-oriented use, and references.

### Local network access restrictions

#### What's New
Restricts the ability to make requests to the user’s local network, gated behind a permission prompt. The origin trial temporarily allows access to local network resources from non-secure contexts.

#### Technical Details
- Network access to local resources is permission-gated.
- The origin trial relaxes this restriction for non-secure contexts on a temporary basis.

#### Use Cases
- Maintain local network access from non-secure contexts during migration and evaluation.
- Collect feedback while adapting to permission-gated local requests.

#### References
- [Tracking bug #394009026](https://issues.chromium.org/issues/394009026)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928)
- [Spec](https://wicg.github.io/local-network-access)

### Proofreader API

#### What's New
A JavaScript API for proofreading input text with suggested corrections, backed by an AI language model.

#### Technical Details
- Exposes a JavaScript interface to request proofreading and receive suggestions.
- Available via an origin trial.

#### Use Cases
- Provide in-product proofreading with suggested corrections for user input.

#### References
- [Tracking bug #403313556](https://issues.chromium.org/issues/403313556)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5164677291835392)
- [Spec](https://github.com/webmachinelearning/proofreader-api/blob/main/README.md#full-api-surface-in-web-idl)

### Extend CSP `script-src` (also known as `script-src-v2`)

#### What's New
Adds new keywords to the `script-src` CSP directive, introducing two new hash-based allowlisting mechanisms: script sources based on hashes of URLs and contents of `eval()` and `eval()`-like functions.

#### Technical Details
- Extends `script-src` to support URL-hash and eval-content-hash based allowlisting.
- Sometimes referred to as “script-src-v2.”

#### Use Cases
- Allowlist scripts via hashes of URLs.
- Allowlist `eval()` and similar content via content hashes.

#### References
- [Tracking bug #392657736](https://issues.chromium.org/issues/392657736)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5196368819519488)
- [Spec](https://github.com/w3c/webappsec-csp/pull/784)

### WebAssembly custom descriptors

#### What's New
Lets WebAssembly store data associated with source-level types more efficiently in new “custom descriptor” objects, which can be configured with prototypes for WebAssembly objects of that type. Enables installing methods on a WebAssembly object’s prototype chain.

#### Technical Details
- Introduces custom descriptor objects to associate data with source-level types.
- Supports configuring prototypes for corresponding WebAssembly objects.

#### Use Cases
- Attach type-specific behavior and methods via prototypes.
- More efficient handling of data associated with source-level types.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/6024844719947776)
- [Spec](https://github.com/WebAssembly/custom-descriptors/blob/main/proposals/custom-descriptors/Overview.md)
