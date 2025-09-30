## Area Summary

Chrome 138 (stable) advances the Web API surface by standardizing built-in language and AI-assisted text capabilities (Translator, Language Detector, Summarizer), while also tightening serialization security and improving runtime diagnostics and push subscription behavior. The most impactful changes for developers are native language processing APIs that reduce the need for site-side large models and improved platform-level safety and observability. These updates push more responsibility to the browser for common tasks (translation, detection, summarization, secure serialization, crash context, push resubscription), simplifying web app implementation and improving end-user privacy and reliability.

## Detailed Updates

The items below expand on the summary above and outline developer-facing implications for each Web API feature in this release.

### Translator API

#### What's New
A JavaScript API that exposes language translation capabilities to web pages, enabling pages to request translations from the browser-provided translation capability.

#### Technical Details
Browser-provided translation is exposed via a web API so developers can integrate translation flows without bundling models or relying solely on browser UI. (See spec and tracking links for implementation specifics.)

#### Use Cases
On-page translation of user content, localized input handling, or augmenting UI when built-in browser translation cannot be used.

#### References
- MDN Docs: https://developer.mozilla.org/docs/Web/API/Translator
- 'Tracking bug #322229993': https://bugs.chromium.org/p/chromium/issues/detail?id=322229993
- ChromeStatus.com entry: https://chromestatus.com/feature/5652970345332736
- Spec: https://wicg.github.io/translation-api/

### Language Detector API

#### What's New
A JavaScript API that detects the language of input text and returns confidence levels, intended to complement translation workflows.

#### Technical Details
Language detection is exposed as a browser API so pages can programmatically determine input language and combine detection with translation or routing logic.

#### Use Cases
Auto-detecting user input language to select translation targets, analytics, or adaptive UI when language is unknown.

#### References
- MDN Docs: https://developer.mozilla.org/docs/Web/API/LanguageDetector
- ChromeStatus.com entry: https://chromestatus.com/feature/5134901000871936
- Spec: https://wicg.github.io/language-detection-api/

### Summarizer API

#### What's New
A JavaScript API for producing summaries of input text backed by an in-browser or OS-provided language model, reducing the need for sites to ship large models.

#### Technical Details
The API exposes summarization capabilities via the browser so sites can request concise summaries without embedding large model artifacts; see spec and tracking links for behavior and safety considerations.

#### Use Cases
Generating abstracts for long articles, previews for user-provided content, or server-side offloading of summarization to the client/browser.

#### References
- MDN Docs: https://developer.mozilla.org/docs/Web/API/Summarizer
- 'Tracking bug #351744634': https://bugs.chromium.org/p/chromium/issues/detail?id=351744634
- ChromeStatus.com entry: https://chromestatus.com/feature/5134971702001664
- Spec: https://wicg.github.io/summarization-api/

### Escape < and > in attributes on serialization

#### What's New
Attribute values are serialized with `<` and `>` escaped to mitigate mutation XSS risks when serialized attributes might be re-parsed as start-tag tokens.

#### Technical Details
The serialization algorithm now escapes `<` and `>` inside attribute values per the HTML parsing/serialization spec to reduce the risk of attribute-driven injection when content is re-serialized and re-parsed.

#### Use Cases
Improves safety of DOM serialization operations (e.g., innerHTML-like flows, HTML fragment generation) by preventing certain mutation XSS vectors.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5125509031477248
- Spec: https://html.spec.whatwg.org/multipage/parsing.html#serializing-html-fragments

### Crash Reporting API: is_top_level and visibility_state

#### What's New
Adds string fields `is_top_level` and `visibility_state` to the crash reporting API body sent to the default crash reporting endpoint.

#### Technical Details
These fields provide additional runtime context about the page when a crash report is generated, following the reporting spec extensions for crash reports.

#### Use Cases
Provides richer crash context for diagnostics and triage (e.g., whether the crash occurred in a top-level page and the document visibility state), aiding reliability engineering and debugging.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5112885175918592
- Spec: https://w3c.github.io/reporting/#crash-report

### Fire the pushsubscriptionchange event upon resubscription

#### What's New
When notification permission for an origin that previously had a push subscription is re-granted after being revoked, service workers will receive a `pushsubscriptionchange` event with an empty `oldSubscription` and the current subscription as `newSubscription`.

#### Technical Details
This behavior ensures service workers are notified of subscription lifecycle changes stemming from permission transitions, aligning with the Push API spec.

#### Use Cases
Helps push-capable applications detect resubscription scenarios after permission changes and update server-side subscription records or re-register with push services.

#### References
- 'Tracking bug #407523313': https://bugs.chromium.org/p/chromium/issues/detail?id=407523313
- ChromeStatus.com entry: https://chromestatus.com/feature/5115983529336832
- Spec: https://w3c.github.io/push-api/#the-pushsubscriptionchange-event

Saved to digest_markdown/webplatform/Web API/chrome-138-stable-en.md