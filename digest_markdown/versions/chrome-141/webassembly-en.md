---
layout: default
title: Area Summary
---

# Area Summary

Chrome 141 (stable) introduces a focused advancement for WebAssembly: custom descriptors. This feature enables more efficient storage of data associated with source-level types and allows configuring prototypes for corresponding WebAssembly objects, making it possible to install methods on those prototypes. It advances the web platform by improving ergonomics and expressiveness when modeling WebAssembly types and behaviors in JavaScript. Delivered via an origin trial, it offers developers an opportunity to evaluate patterns for per-type data and method exposure.

## Detailed Updates

Building on the theme of efficiency and ergonomics for WebAssembly type modeling, this release adds:

### WebAssembly custom descriptors

#### What's New
- Lets WebAssembly store data associated with source-level types more efficiently in new “custom descriptor” objects.
- Allows configuring prototypes for WebAssembly objects of that source-level type, enabling installation of methods on a WebAssembly object's prototype.
- Available via origin trial.

#### Technical Details
- Introduces custom descriptor objects that hold data tied to a source-level type.
- These descriptors can specify the prototype for WebAssembly objects of that type, supporting method installation on the prototype.

#### Use Cases
- Attaching type-specific methods to WebAssembly objects through configured prototypes.
- Organizing and accessing per-type metadata more efficiently.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/6024844719947776
- Spec: https://github.com/WebAssembly/custom-descriptors/blob/main/proposals/custom-descriptors/Overview.md
