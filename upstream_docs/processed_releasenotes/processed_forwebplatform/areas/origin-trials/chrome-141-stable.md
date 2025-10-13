## Origin trials

### Local network access restrictions

Chrome 141 [restricts the ability to make requests to the user's local network](/blog/local-network-access), gated behind a permission prompt.

This origin trial temporarily allows for access to resources on local networks to originate from non-secure contexts. This will give developers more time to migrate Local Network Access requests to originate from a secure context.

[Origin Trial](/origintrials#/view_trial/3826370833404657665) | [Tracking bug #394009026](https://issues.chromium.org/issues/394009026) | [ChromeStatus.com entry](https://chromestatus.com/feature/5152728072060928) | [Spec](https://wicg.github.io/local-network-access)

### Proofreader API

A JavaScript API for [proofreading input text with suggested corrections](/blog/proofreader-api-ot), backed by an AI language model.

[Origin Trial](/origintrials#/register_trial/1988902185437495297) | [Tracking bug #403313556](https://issues.chromium.org/issues/403313556) | [ChromeStatus.com entry](https://chromestatus.com/feature/5164677291835392) | [Spec](https://github.com/webmachinelearning/proofreader-api/blob/main/README.md#full-api-surface-in-web-idl)

### Extend CSP `script-src` (also known as `script-src-v2`)

This feature adds new keywords to the `script-src` Content Security Policy (CSP) directive. This adds two new hash-based allowlisting mechanisms: script sources based on hashes of URLs and contents of `eval()` and `eval()`-like functions. This is sometimes referred to as script-src-v2, although it is backward compatible with the existing script-src, and uses the same directive.

Extending hashes to cover URL and `eval()` hashes lets developers set reasonably strict security policies by narrowly allowlisting scripts by their hashes even when script contents are subject to frequent changes, and known-safe contents of `eval()` without permitting unchecked use of `eval()` broadly.

The new keywords override host-based script-src when provided. This allows a single header to be compatible with browsers that both do or do not implement the new keywords.

[Tracking bug #392657736](https://issues.chromium.org/issues/392657736) | [ChromeStatus.com entry](https://chromestatus.com/feature/5196368819519488) | [Spec](https://github.com/w3c/webappsec-csp/pull/784)

### WebAssembly custom descriptors

Lets WebAssembly store data associated with source-level types more efficiently in new "custom descriptor" objects. These custom descriptors can be configured with prototypes for the WebAssembly objects of that source-level type. This lets you install methods on a WebAssembly object's prototype chain and call them directly from JavaScript using normal method call syntax. The prototypes and methods can be configured declaratively using an imported built-in function.

[Origin Trial](/origintrials#/view_trial/619807898716864513) | [ChromeStatus.com entry](https://chromestatus.com/feature/6024844719947776) | [Spec](https://github.com/WebAssembly/custom-descriptors/blob/main/proposals/custom-descriptors/Overview.md)
