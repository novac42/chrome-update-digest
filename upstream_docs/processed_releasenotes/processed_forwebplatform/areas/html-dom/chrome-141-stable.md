## DOM

### ARIA Notify API

`ariaNotify` provides a JavaScript API that lets content authors tell a screen reader what to read.

`ariaNotify` improves reliability and developer control compared to ARIA live regions, allowing for announcing changes not tied to DOM updates. This enables more consistent and ergonomic accessibility experiences across dynamic web applications. Iframe usage of this feature can be controlled using the `"aria-notify"` permission policy.

[Tracking bug #326277796](https://issues.chromium.org/issues/326277796) | [ChromeStatus.com entry](https://chromestatus.com/feature/5745430754230272) | [Spec](https://github.com/w3c/aria/pull/2577)

### Update `hidden=until-found` and details ancestor revealing algorithm

The specification recently had some small changes to the revealing algorithms for `hidden=until-found` and details elements to prevent the browser from getting stuck in an infinite loop, these are now shipping in Chrome.

[Tracking bug #433545121](https://issues.chromium.org/issues/433545121) | [ChromeStatus.com entry](https://chromestatus.com/feature/5179013869993984) | [Spec](https://github.com/whatwg/html/pull/11457)
