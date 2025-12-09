---
layout: default
title: chrome-143-en
---

## Area Summary

Chrome 143 relaxes JavaScript DOM API validation so element and attribute names accepted by the HTML parser are also accepted when created from scripts. This reduces surprising mismatches between parsed HTML and DOM-created nodes, making DOM APIs more permissive and consistent. For developers, the change lowers friction when programmatically creating elements/attributes that previously failed strict validation. Overall, it advances platform consistency and interoperability between parsing and scripting paths.

## Detailed Updates

The single update below expands on the summary and explains practical effects for DOM-focused development.

### Allow more characters in JavaScript DOM APIs

#### What's New
The JavaScript DOM APIs now accept a wider set of characters for element and attribute names by relaxing validation to match what the HTML parser allows.

#### Technical Details
The change aligns DOM API validation rules with the HTML parser's name handling so that names permitted during parsing are also permitted when created via scripting interfaces.

#### Use Cases
- Programmatic creation of elements and attributes that previously failed validation will now succeed.
- Reduces the need for workarounds (e.g., constructing nodes via innerHTML) to represent names allowed in parsed HTML.
- Improves parity between DOM produced by parsing and by script, simplifying developer reasoning about node creation.

#### References
- [Tracking bug #40228234](https://issues.chromium.org/issues/40228234)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416)  
- [Spec](https://dom.spec.whatwg.org/#namespaces)
