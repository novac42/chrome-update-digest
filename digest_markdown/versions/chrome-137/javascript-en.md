---
layout: default
title: javascript-en
---

## Area Summary

Chrome 137 stable introduces JavaScript Promise Integration (JSPI), focusing on tighter interoperability between WebAssembly and JavaScript Promises. The primary theme is enabling WebAssembly modules to participate directly in JavaScript's async model by acting as Promise generators and interacting with Promise-bearing APIs. This change is impactful for developers mixing Wasm and JS, simplifying integration patterns and clarifying cross-language async flows. It advances the web platform by formalizing a bridge between ECMAScript Promises and WebAssembly execution contexts.

## Detailed Updates

Below are the specific updates that implement the summary above.

### JavaScript promise integration

#### What's New
JavaScript Promise Integration (JSPI) is an API that allows WebAssembly applications to integrate with JavaScript Promises. It enables a WebAssembly program to act as the generator of a Promise and to interact with Promise-bearing APIs.

#### Technical Details
The feature is specified as an API bridging WebAssembly and JavaScript Promise semantics. It defines how a Wasm program can create/drive Promises and interoperate with existing Promise-bearing JavaScript APIs. (See linked spec for authoritative details.)

#### Use Cases
- WebAssembly modules that need to initiate or return JavaScript Promises.
- Wasm-based code consuming existing async JavaScript APIs without complex glue code.
- Cleaner async control flow in applications mixing Wasm and JS components.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5059306691878912  
- Spec: https://github.com/WebAssembly/js-promise-integration
