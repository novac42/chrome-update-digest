## Area Summary

Chrome 141’s CSS updates focus on CSSOM correctness and interoperability. The primary change fixes custom property enumeration in getComputedStyle(), ensuring that computed style iteration and length reflect custom properties as expected. This improves spec compliance and cross-browser consistency, reducing edge-case bugs in tooling and tests that rely on computed style inspection. The result is more reliable CSS inspection, diagnostics, and automation across modern development workflows.

## Detailed Updates

This release sharpens CSSOM behavior to match developer expectations and the specification, improving reliability for style introspection and tooling.

### Custom property enumeration in `getComputedStyle()`

#### What's New
Chrome 141 fixes a bug where iterating over window.getComputedStyle(element) did not include custom properties, and the length of the returned object did not account for them.

#### Technical Details
- Iteration over the CSSStyleDeclaration returned by getComputedStyle(element) now includes custom properties defined on the element.
- The length attribute of the returned object reflects the presence of these custom properties.
- Behavior is aligned with the CSSOM specification for computed style enumeration.

#### Use Cases
- Style inspection and diagnostics tools that enumerate computed styles now capture custom properties without workarounds.
- Test suites and linters relying on CSSStyleDeclaration.length get accurate counts, reducing false negatives/positives.
- Telemetry, serialization, or debugging workflows that iterate computed styles produce complete datasets.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5070655645155328
- Spec: https://drafts.csswg.org/cssom/#dom-window-getcomputedstyle