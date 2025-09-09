---
layout: default
title: chrome-139
---

## On-device AI

### On-device Web Speech API

This feature adds on-device speech recognition support to the Web Speech API, allowing websites to ensure that neither audio nor transcribed speech are sent to a third-party service for processing.

Websites can query the availability of on-device speech recognition for specific languages, prompt users to install the necessary resources for on-device speech recognition, and choose between on-device or cloud-based speech recognition as needed.

[ChromeStatus.com entry](https://chromestatus.com/feature/6090916291674112) | [Spec](https://webaudio.github.io/web-speech-api)


## Origin trials

### Prompt API

An API designed for interacting with an AI language model using text, image, and audio inputs. It supports various use cases, from generating image captions and performing visual searches to transcribing audio, classifying sound events, generating text following specific instructions, and extracting information or insights from text. It supports structured outputs which ensure that responses adhere to a predefined format, typically expressed as a JSON schema, to enhance response conformance and facilitate seamless integration with downstream applications that require standardized output formats.

This API is also exposed in Chrome Extensions. This feature entry tracks the exposure on the web. An enterprise policy (`GenAILocalFoundationalModelSettings`) is available to disable the underlying model downloading which would render this API unavailable.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313) | [Origin trial blog post](/blog/prompt-multimodal-origin-trial) | [Tracking bug #417530643](https://issues.chromium.org/issues/417530643) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134603979063296)

### Extended lifetime shared workers

This adds a new option, `extendedLifetime: true`, to the `SharedWorker` constructor. This requests that the shared worker be kept alive even after all current clients have unloaded. The primary use case is to allow pages to perform asynchronous work that requires JavaScript after a page unloads, without needing to rely on a service worker.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849) | [Origin trial blog post](/blog/extended-lifetime-shared-workers-origin-trial) | [Tracking bug #400473072](https://issues.chromium.org/issues/400473072) | [ChromeStatus.com entry](https://chromestatus.com/feature/5138641357373440)

### `SoftNavigation` performance entry

Exposes the (experimental) soft navigation heuristics to web developers, using both `PerformanceObserver` and the performance timeline.

This feature reports two new performance entries:

  * `soft-navigation`, for user interactions which navigate the page. Defines a new `timeOrigin` to help slice the performance timeline.
  * `interaction-contentful-paint`, which reports on the loading performance of interactions (beyond just next paint), used as LCP for soft-navigations.

[Origin Trial](https://developer.chrome.com/origintrials#/view_trial/21392098230009857) | [Origin trial blog post](/blog/new-soft-navigations-origin-trial) | [Tracking bug #1338390](https://issues.chromium.org/issues/1338390) | [ChromeStatus.com entry](https://chromestatus.com/feature/5144837209194496) | [Spec](https://wicg.github.io/soft-navigations)

### Web Authentication immediate mediation

A mediation mode for `navigator.credentials.get()` that causes browser sign-in UI to be displayed to the user if there is a passkey or password for the site that is immediately known to the browser. Otherwise, it rejects the with `NotAllowedError` if there is no such credential available. This allows the site to avoid showing a sign-in page if the browser can offer a choice of sign-in credentials that are likely to succeed, while still allowing a sign-in page flow for cases where there are no such credentials.

[Tracking bug #408002783](https://issues.chromium.org/issues/408002783) | [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704) | [Spec](https://github.com/w3c/webauthn/pull/2291)

### Full frame rate render blocking attribute

Adds a new render blocking token full-frame-rate to the blocking attributes. When the renderer is blocked with the full-frame-rate token, the renderer will work at a lower frame rate so as to reserve more resources for loading.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385) | [Tracking bug #397832388](https://issues.chromium.org/issues/397832388) | [ChromeStatus.com entry](https://chromestatus.com/feature/5207202081800192)

### WebGPU compatibility mode

Adds an opt-in, lightly restricted subset of the WebGPU API capable of running older graphics APIs such as OpenGL and Direct3D11. By opting into this mode and obeying its constraints, developers can extend the reach of their WebGPU applications to many older devices that don't have the modern, explicit graphics APIs that core WebGPU requires.

[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241) | [Tracking bug #40266903](https://issues.chromium.org/issues/40266903) | [ChromeStatus.com entry](https://chromestatus.com/feature/6436406437871616) | [Spec](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)
