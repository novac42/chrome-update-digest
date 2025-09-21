# Chrome 140 Web API Release Analysis

## Summary

Chrome 140 introduces three significant Web API enhancements focused on streaming capabilities, cross-platform app integration, and cookie security. The most notable additions include improved byte stream reading with minimum read guarantees, expanded desktop support for the Get Installed Related Apps API, and enhanced HTTP cookie security through prefixing mechanisms.

## Feature Details

### `ReadableStreamBYOBReader` `min` option

**What Changed**:
This enhancement adds a `min` option to the `ReadableStreamBYOBReader.read(view)` method, addressing a key limitation in the current Streams API. Previously, while the method accepted an `ArrayBufferView` for reading data, it provided no guarantee about how many elements would be written before the read operation resolved. The new `min` parameter allows developers to specify a minimum number of bytes that must be read before the promise resolves, providing more predictable and efficient streaming behavior. This is particularly valuable for applications that need to ensure sufficient data availability before processing, such as media streaming, file processing, or network protocol implementations.

**References**:
- [Tracking bug #40942083](https://issues.chromium.org/issues/40942083)
- [ChromeStatus.com entry](https://chromestatus.com/feature/6396991665602560)
- [Spec](https://streams.spec.whatwg.org/#byob-reader-read)

### Get Installed Related Apps API on desktop

**What Changed**:
The Get Installed Related Apps API (`navigator.getInstalledRelatedApps`) expands its availability to desktop platforms, building on its initial launch in Chrome 80. This API enables websites to detect whether their corresponding native applications are installed on the user's device, but only when there's an established association between the web origin and the application. The desktop expansion significantly broadens the API's utility, allowing web applications to provide seamless integration experiences across different platforms. This enables scenarios like prompting users to open content in the native app when available, providing app-specific features, or offering installation suggestions when the related app isn't detected.

**References**:
- [Tracking bug #895854](https://issues.chromium.org/issues/895854)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5695378309513216)
- [Spec](https://wicg.github.io/get-installed-related-apps/spec)

### Http cookie prefix

**What Changed**:
This security enhancement introduces HTTP cookie prefixing to help servers distinguish between cookies set by the server versus those set by client-side code. This distinction is crucial for security-sensitive scenarios where cookies are typically server-controlled but could be compromised through XSS exploits, malicious browser extensions, or developer errors. The prefixing mechanism provides a standardized way to mark cookies with their origin, enabling servers to validate cookie authenticity and implement more robust security policies. This feature strengthens web application security by providing a clear separation between trusted server-set cookies and potentially untrusted client-set cookies.

**References**:
- [Tracking bug #426096760](https://issues.chromium.org/issues/426096760)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5170139586363392)
- [Spec](https://github.com/httpwg/http-extensions/pull/3110)