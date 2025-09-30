---
layout: default
title: html-dom-en
---

## Detailed Updates

The following entry explains the specific HTML-DOM change in Chrome 139 and its developer implications.

### Allow more characters in JavaScript DOM APIs

#### What's New
The validation performed by JavaScript DOM APIs when creating elements and attributes has been relaxed so that the set of allowed characters and names is more consistent with what the HTML parser accepts.

#### Technical Details
The change adjusts DOM API validation logic to align with parser behavior and the DOM specification for names/namespaces. Implementation and tracking are recorded in Chromium issue trackers and ChromeStatus. See the spec for authoritative rules about namespace and name handling.

#### Use Cases
- Libraries and frameworks that synthesize elements or attributes dynamically will face fewer failures when using nonstandard or non-ASCII names.
- Localization and i18n scenarios where element/attribute names may include wider character ranges will be more reliable.
- Reduces need for encoding or fallback strategies when dynamically generating DOM nodes.

#### References
- Tracking bug #40228234 - https://issues.chromium.org/issues/40228234
- ChromeStatus.com entry - https://chromestatus.com/feature/6278918763708416
- Spec - https://dom.spec.whatwg.org/#namespaces

## Area-Specific Expertise (HTML-DOM implications)

- css: Broader allowed names can affect authoring and tooling that match elements/attributes by name; ensure selector generation/escaping accounts for extended name forms.
- webapi: DOM creation APIs (e.g., element/attribute constructors) will accept a wider character set; review code that previously sanitized or rejected names.
- graphics-webgpu: No direct effect on GPU pipelines; however, dynamically generated DOM used for rendering controls may be more flexible.
- javascript: Reduces runtime exceptions when calling DOM APIs to create nodes with nonstandard names; fewer polyfills required.
- security-privacy: Relaxed validation should be reviewed for any interaction with CSP or sanitizers—ensure application-level validation remains appropriate.
- performance: Eliminates some defensive logic and round trips to sanitize names, possibly simplifying DOM construction paths.
- multimedia: No direct change to media APIs, but dynamically created attribute names for metadata become more permissive.
- devices: No direct effect on hardware APIs; DOM naming relaxations don't change capabilities exposure.
- pwa-service-worker: Service worker generated DOM snapshots or serialization strategies may need less name-mangling.
- webassembly: WASM modules that emit DOM-manipulating JS benefit from fewer name validation edge cases.
- deprecations: Not a deprecation; this is an interoperability improvement. Check compatibility for older user agents that still enforce stricter validation.

Save path:
```text
digest_markdown/webplatform/HTML-DOM/chrome-139-stable-en.md
