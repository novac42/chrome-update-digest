---
layout: default
title: Chrome 140 Web API Updates
---

# Chrome 140 Web API Updates

## Area Summary

Chrome 140 brings significant enhancements to the Web API landscape with three key updates that strengthen data streaming, application integration, and security mechanisms. The release introduces refined control over readable streams through the new `ReadableStreamBYOBReader` `min` option, extends the Get Installed Related Apps API to desktop platforms for better cross-platform app discovery, and implements HTTP cookie prefixes to enhance security by distinguishing server-set cookies from client-set ones. These updates collectively advance the web platform's capabilities in performance optimization, application ecosystem integration, and security hardening.

## Detailed Updates

These Web API improvements focus on enhancing developer control over data flows, expanding platform capabilities, and strengthening security foundations across web applications.

### `ReadableStreamBYOBReader` `min` option

#### What's New
The `ReadableStreamBYOBReader.read(view)` method now accepts a `min` option that guarantees a minimum number of elements will be written before the read operation resolves.

#### Technical Details
Previously, the `ReadableStreamBYOBReader.read()` method would read data into an `ArrayBufferView` but provided no control over how many elements were written before resolving. The new `min` parameter allows developers to specify the minimum amount of data they want to receive in a single read operation, providing better control over buffer management and reducing the number of read calls needed for larger data transfers.

#### Use Cases
This enhancement is particularly valuable for applications that process streaming data in chunks, such as media players, file processors, or network protocols that require specific buffer sizes. Developers can now optimize their streaming implementations by ensuring they receive adequate data volumes per read operation, reducing overhead and improving performance.

#### References
- [Tracking bug #40942083](https://issues.chromium.org/issues/40942083)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6396991665602560)
- [Spec](https://streams.spec.whatwg.org/#byob-reader-read)

### Get Installed Related Apps API on desktop

#### What's New
The Get Installed Related Apps API (`navigator.getInstalledRelatedApps`) is now available on desktop platforms, allowing websites to detect if their corresponding applications are installed on the user's system.

#### Technical Details
Originally launched in Chrome 80 for mobile platforms, this API enables sites to query for related applications that have established associations with the web origin. The API maintains strict security requirements, only allowing access when applications have properly declared their relationship with the website through manifest files or platform-specific mechanisms.

#### Use Cases
Desktop support opens new possibilities for seamless user experiences across web and native applications. Websites can now provide contextual app download prompts, offer deep-linking to installed applications, or adjust their interface based on available native counterparts. This is particularly useful for productivity apps, communication tools, and content platforms that offer both web and desktop experiences.

#### References
- [Tracking bug #895854](https://issues.chromium.org/issues/895854)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5695378309513216)
- [Spec](https://wicg.github.io/get-installed-related-apps/spec)

### Http cookie prefix

#### What's New
Chrome 140 introduces HTTP cookie prefixes that allow servers to distinguish between cookies set by the server versus those set by client-side code, enhancing security against various attack vectors.

#### Technical Details
This security feature implements a mechanism to mark cookies with specific prefixes that indicate their origin. The implementation helps prevent scenarios where malicious code (such as XSS exploits, browser extensions, or compromised scripts) could set cookies that might be confused with legitimate server-set cookies. This distinction is crucial for maintaining the integrity of authentication and session management systems.

#### Use Cases
The cookie prefix feature is essential for applications with strict security requirements, particularly those handling sensitive data or authentication flows. It helps prevent attacks where malicious scripts attempt to forge server cookies, and provides servers with reliable ways to validate cookie authenticity. This is especially valuable for financial services, enterprise applications, and any system where cookie integrity is critical for security.

#### References
- [Tracking bug #426096760](https://issues.chromium.org/issues/426096760)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5170139586363392)
- [Spec](https://github.com/httpwg/http-extensions/pull/3110)
