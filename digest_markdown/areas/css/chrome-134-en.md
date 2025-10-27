---
layout: default
title: chrome-134-en
---

## Area Summary

Chrome 134 introduces CSS highlight inheritance, changing how highlight pseudo-classes like ::selection and ::highlight inherit properties. The key trend is clarifying cascade semantics for pseudo highlights by following a pseudo highlight chain instead of the element chain. This makes highlight styling more predictable, reducing author workarounds and aligning behavior with the evolving CSS Pseudo-Elements spec. Developers should expect more consistent selection/highlight styling across shadow DOM and composed trees.

## Detailed Updates

The entry below expands on the summary and explains practical effects for developers.

### CSS highlight inheritance

#### What's New
With CSS highlight inheritance, CSS highlight pseudo-classes (for example `::selection` and `::highlight`) inherit their properties through the pseudo highlight chain rather than the element chain, producing a more intuitive inheritance model for highlights.

#### Technical Details
Inheritance now follows the "highlight cascade" described in the CSS Pseudo-Elements level 4 draft: highlights form their own cascade chain, so computed values for highlight pseudo-classes derive from highlight ancestors in that chain rather than from host element ancestry. This aligns delivery of style properties for highlight pseudo-elements with the spec's pseudo highlight chain semantics.

#### Use Cases
- Authoring consistent `::selection` or `::highlight` styles across shadow DOM boundaries and composed components.
- Reducing CSS specificity workarounds when styling highlights inside nested components.
- More predictable computed style behavior for tooling that inspects or overrides selection/highlight styles.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5090853643354112
- Spec: https://drafts.csswg.org/css-pseudo-4/#highlight-cascade

## Area-Specific Expertise

- css: Clarifies cascade/inheritance semantics for highlight pseudo-classes; aligns UA behavior with the CSS Pseudo-Elements spec.
- webapi: Affects computed style retrieval and styling interactions for pseudo-elements exposed via the DOM/style APIs.
- graphics-webgpu: No direct impact on rendering pipelines; styling changes may alter GPU compositing inputs only insofar as paint differences change layers.
- javascript: getComputedStyle and dynamic style adjustments involving highlights will reflect the new inheritance model.
- security-privacy: Minimal direct effect; selection styling remains a UI-only concern but consistency reduces unexpected visibility changes.
- performance: Simplifies author styles and may reduce forced style recalculations from workaround patterns.
- multimedia: No material effect on media playback or codecs.
- devices: No device-API impact.
- pwa-service-worker: No direct relation.
- webassembly: Not affected.
- deprecations: No deprecation; this is a normative behavior change aligning with spec.
