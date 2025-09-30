## Area Summary

Chrome 140 introduces a small but focused HTML‑DOM enhancement: a `source` attribute on the `ToggleEvent` interface. This attribute surfaces the element that triggered a `ToggleEvent` when applicable, improving event context for handlers. For developers, the change makes it easier to identify the initiating element (e.g., a button that opened a popover) without custom DOM traversal or extra attributes. This advances the platform by making built‑in DOM events more informative and reducing boilerplate for interactive components.

## Detailed Updates

The single update below directly supports the summary above.

### `ToggleEvent` source attribute

#### What's New
The `source` attribute of a `ToggleEvent` contains the element that triggered the `ToggleEvent` to be fired, if applicable.

#### Technical Details
This adds an accessible property on the `ToggleEvent` DOM interface that references the triggering element when one exists. The release notes illustrate the behavior with an example involving a `<button>` element that opens a popover via attributes like `popovertarget` or `commandfor`.

#### Use Cases
- Event handlers on popovers or toggled UI can inspect `event.source` to determine which control initiated the toggle.
- Simplifies logic for components that need to differentiate user‑initiated toggles from programmatic ones.
- Reduces reliance on attribute-based linkage or manual element lookup to find the initiating element.

#### References
- https://chromestatus.com/feature/5165304401100800
- https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface

## Area-Specific Expertise (HTML-DOM)

- css: Minimal direct impact on layout; enables clearer linkage between controls and toggled UI without extra DOM markup.
- webapi: Extends the DOM event API by adding a `source` attribute to `ToggleEvent`.
- graphics-webgpu: No direct relevance to GPU or rendering pipelines.
- javascript: V8 consumers can read `event.source` from `ToggleEvent` handlers to simplify control flow.
- security-privacy: Exposes an element reference in event objects; standard same-origin and DOM access rules continue to apply.
- performance: Low overhead; avoids extra DOM queries in common toggle handling paths.
- multimedia: Not applicable to codecs/streaming.
- devices: No direct device API implications.
- pwa-service-worker: No direct effect on service worker behavior.
- webassembly: No direct WASM runtime impact.
- deprecations: No deprecation implications reported. 

Saved to: digest_markdown/webplatform/HTML-DOM/chrome-140-stable-en.md