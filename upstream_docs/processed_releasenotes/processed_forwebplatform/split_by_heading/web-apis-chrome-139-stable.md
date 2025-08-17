## Web APIs

### Web app scope extensions

Adds a `scope_extensions` web app manifest field that enables web apps to extend their scope to other origins.

This allows sites that control multiple subdomains and top level domains to be presented as a single web app.

Requires listed origins to confirm association with the web app using a `.well-known/web-app-origin-association` configuration file.

[Tracking bug #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011) | [ChromeStatus.com entry](https://chromestatus.com/feature/5746537956114432) | [Spec](https://github.com/WICG/manifest-incubations/pull/113)

### Specification-compliant JSON MIME type detection

Chrome now recognizes all valid JSON MIME types as defined by the WHATWG mimesniff specification. This includes any MIME type whose subtype ends with `+json`, in addition to `application/json` and `text/json`. This change ensures that web APIs and features relying on JSON detection behave consistently with the web platform standard and other browsers.

[ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528) | [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

### WebGPU `core-features-and-limits`

The `core-features-and-limits` feature signifies a WebGPU adapter and device support the core features and limits of the spec.

[Tracking bug #418025721](https://issues.chromium.org/issues/418025721) | [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496) | [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports

This feature ensures developers receive only crash reports by specifying the endpoint named `crash-reporting`. By default, crash reports are delivered to the `default` endpoint which receives many other kinds of reports besides crash reports. Developers can supply a separate URL to the well-known endpoint named `crash-reporting`, to direct crash reports there, instead of the `default` endpoint.

[Tracking bug #414723480](https://issues.chromium.org/issues/414723480) | [ChromeStatus.com entry](https://chromestatus.com/feature/5129218731802624) | [Spec](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)
