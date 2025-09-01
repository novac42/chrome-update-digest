## Web APIs

### Translator API

A JavaScript API to provide language translation capabilities to web pages. Browsers are increasingly offering language translation to their users. Such translation capabilities can also be useful to web developers. This is especially the case when browser's built-in translation abilities cannot help. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/API/Translator) | [Tracking bug #322229993](https://bugs.chromium.org/p/chromium/issues/detail?id=322229993) | [ChromeStatus.com entry](https://chromestatus.com/feature/5652970345332736) | [Spec](https://wicg.github.io/translation-api/)

### Language Detector API

A JavaScript API for detecting the language of text, with confidence levels. An important supplement to translation is language detection. This can be combined with translation, for example, taking user input in an unknown language and translating it to a specific target language. Browsers today often already have language detection capabilities, and we want to offer them to web developers through a JavaScript API, supplementing the translation API. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/API/LanguageDetector) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134901000871936) | [Spec](https://wicg.github.io/language-detection-api/)

### Summarizer API

Summarizer API is a JavaScript API for producing summaries of input text, backed by an AI language model. Browsers and operating systems are increasingly expected to gain access to a language model. By exposing this built-in model, we avoid every website needing to download their own multi-gigabyte language model, or send input text to third-party APIs. The summarizer API in particular exposes a high-level API for interfacing with a language model in order to summarize inputs for a variety of use cases, in a way that does not depend on the specific language model in question. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

**References:** [MDN Docs](https://developer.mozilla.org/docs/Web/API/Summarizer) | [Tracking bug #351744634](https://bugs.chromium.org/p/chromium/issues/detail?id=351744634) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134971702001664) | [Spec](https://wicg.github.io/summarization-api/)

### Escape < and > in attributes on serialization

Escape `<` and `>` in values of attributes on serialization. This mitigates the risk of mutation XSS attacks, which occur when value of an attribute is interpreted as a start tag token after being serialized and re-parsed.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5125509031477248) | [Spec](https://html.spec.whatwg.org/multipage/parsing.html#serializing-html-fragments)

### Crash Reporting API: is_top_level and visibility_state

This feature adds `is_top_level` and `visibility_state` string fields to the crash reporting API body that gets sent to the default reporting endpoint for crash reports.

**References:** [ChromeStatus.com entry](https://chromestatus.com/feature/5112885175918592) | [Spec](https://w3c.github.io/reporting/#crash-report)

### Fire the pushsubscriptionchange event upon resubscription

Fire the `pushsubscriptionchange` event in service workers when an origin for which a push subscription existed in the past, but which was revoked because of a permission change (from granted to deny/default), is re-granted notification permission. The event will be fired with an empty `oldSubscription` and `newSubscription`.

**References:** [Tracking bug #407523313](https://bugs.chromium.org/p/chromium/issues/detail?id=407523313) | [ChromeStatus.com entry](https://chromestatus.com/feature/5115983529336832) | [Spec](https://w3c.github.io/push-api/#the-pushsubscriptionchange-event)
