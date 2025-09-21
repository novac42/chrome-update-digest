---
layout: default
title: chrome-140
---

## Web APIs

### `ReadableStreamBYOBReader` `min` option

This feature introduces a `min` option to the existing `ReadableStreamBYOBReader.read(view)` method. The method already accepts an `ArrayBufferView` into which it reads data, but currently does not guarantee how many elements are written before the read resolves. By specifying a `min` value, you can require that the stream wait until at least that many elements are available before resolving the read. This improves upon the current behavior, where reads may resolve with fewer elements than the view can hold.

[Tracking bug #40942083](https://issues.chromium.org/issues/40942083) | [ChromeStatus.com entry](https://chromestatus.com/feature/6396991665602560) | [Spec](https://streams.spec.whatwg.org/#byob-reader-read)

### Get Installed Related Apps API on desktop

The Get Installed Related Apps API (navigator.getInstalledRelatedApps) provides sites access to if their corresponding related applications are installed. Sites are only allowed to use this API if the application has an established association with the web origin.

The API was launched in Chrome 80 for Android. Additional support for web apps on Desktop was enabled in Chrome 140.

[Docs](/docs/capabilities/get-installed-related-apps) | [Tracking bug #895854](https://issues.chromium.org/issues/895854) | [ChromeStatus.com entry](https://chromestatus.com/feature/5695378309513216) | [Spec](https://wicg.github.io/get-installed-related-apps/spec)

### Http cookie prefix

In some cases, it's important to distinguish on the server side between cookies set by the server and those set by the client. One such case involves cookies normally always set by the server. However, unexpected code (such as an XSS exploit, a malicious extension, or a commit from a confused developer) might set them on the client. This proposal adds a signal that lets servers make such a distinction. More specifically, it defines the `__Http` and `__HostHttp` prefixes, which ensure a cookie is not set on the client side using script.

[Tracking bug #426096760](https://issues.chromium.org/issues/426096760) | [ChromeStatus.com entry](https://chromestatus.com/feature/5170139586363392) | [Spec](https://github.com/httpwg/http-extensions/pull/3110)
