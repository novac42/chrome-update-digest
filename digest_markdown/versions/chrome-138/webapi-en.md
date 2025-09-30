---
layout: default
title: webapi-en
---

## Area Summary

Chrome 138 for the Web API area emphasizes built-in language and AI-assisted capabilities (Translator, Language Detector, Summarizer), plus platform hardening and lifecycle improvements for service workers and reporting. The most impactful changes let developers leverage browser-provided translation/detection/summarization models and avoid shipping large ML artifacts, while security and reliability improvements (attribute serialization escaping, richer crash reports, and push subscription lifecycle events) reduce attack surface and improve diagnostics. Collectively these updates advance the web platform by exposing native language-model services, tightening serialization behavior to mitigate mutation XSS, and making push and crash reporting semantics more actionable for developers. These updates matter because they improve developer ergonomics, user privacy/performance trade-offs, and overall platform resilience.

## Detailed Updates

The following items expand on the summary above with concise, developer-focused details.

### Translator API

#### What's New
A JavaScript API to provide language translation capabilities to web pages, exposing browser-level translation functionality to developers.

#### Technical Details
Exposes translation functionality via a web API so pages can request translations without bundling models. Relevant to webapi and javascript domains; links point to MDN, a tracking bug, ChromeStatus, and the WICG spec.

#### Use Cases
On-demand translation of user-generated content or UI text when built-in browser translation is insufficient or when site-controlled translation workflows are needed.

#### References
- https://developer.mozilla.org/docs/Web/API/Translator
- https://bugs.chromium.org/p/chromium/issues/detail?id=322229993
- https://chromestatus.com/feature/5652970345332736
- https://wicg.github.io/translation-api/

### Language Detector API

#### What's New
A JavaScript API for detecting the language of text, returning confidence levels to assist downstream actions.

#### Technical Details
Provides language-detection functionality separate from translation; intended to be combined with translation or other flows. Relevant to webapi and javascript integration points; spec and status links provided.

#### Use Cases
Automatically determine input language for auto-translation, routing, or analytics; precondition step before calling Translator API.

#### References
- https://developer.mozilla.org/docs/Web/API/LanguageDetector
- https://chromestatus.com/feature/5134901000871936
- https://wicg.github.io/language-detection-api/

### Summarizer API

#### What's New
A JavaScript API that produces summaries of input text backed by a built-in AI language model exposed by the browser.

#### Technical Details
Browsers expose an on-device/OS-provided language model via a Summarizer API so sites can summarize content without each site downloading large models. See spec and tracking entries for design details.

#### Use Cases
Client-side summarization of articles, messages, or user-generated content for previews, accessibility, or assistant-like features while reducing network/model-loading costs.

#### References
- https://developer.mozilla.org/docs/Web/API/Summarizer
- https://bugs.chromium.org/p/chromium/issues/detail?id=351744634
- https://chromestatus.com/feature/5134971702001664
- https://wicg.github.io/summarization-api/

### Escape < and > in attributes on serialization

#### What's New
Escape `<` and `>` in values of attributes during HTML serialization to mitigate mutation XSS risks.

#### Technical Details
Serialization now ensures `<` and `>` characters in attribute values are escaped so they cannot be misinterpreted as start-tag tokens after serializing and reparsing. This change aligns with the HTML spec on serializing fragments and is a security-hardening measure relevant to security-privacy and parsing behavior.

#### Use Cases
Reduces the class of mutation XSS issues when applications serialize DOM fragments or set attributes that may later be reparsed or injected.

#### References
- https://chromestatus.com/feature/5125509031477248
- https://html.spec.whatwg.org/multipage/parsing.html#serializing-html-fragments

### Crash Reporting API: is_top_level and visibility_state

#### What's New
Adds string fields `is_top_level` and `visibility_state` to the crash reporting API payload sent to the default reporting endpoint.

#### Technical Details
Crash report bodies now include these additional context fields to improve understanding of crash circumstances. This change affects reporting semantics and backend diagnostics; see the reporting spec and ChromeStatus entry for the intended fields.

#### Use Cases
Improves server-side crash analytics and client-side triage by providing visibility context and top-level frame status, aiding debugging and prioritization.

#### References
- https://chromestatus.com/feature/5112885175918592
- https://w3c.github.io/reporting/#crash-report

### Fire the pushsubscriptionchange event upon resubscription

#### What's New
Service workers will fire the `pushsubscriptionchange` event when notification permission for an origin that previously had a subscription is re-granted; the event is dispatched with an empty oldSubscription in such cases.

#### Technical Details
This behavior change makes push subscription lifecycle more explicit when permission transitions (granted → denied/default → granted) occur. It follows the Push API spec semantics for the `pushsubscriptionchange` event and impacts pwa-service-worker and permission-handling flows.

#### Use Cases
Allows service workers to re-subscribe or reconcile push state when permissions are re-granted, enabling reliable push delivery recovery and improved developer handling of permission churn.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=407523313
- https://chromestatus.com/feature/5115983529336832
- https://w3c.github.io/push-api/#the-pushsubscriptionchange-event
