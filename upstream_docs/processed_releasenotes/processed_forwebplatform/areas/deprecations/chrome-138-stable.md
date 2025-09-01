## Deprecations and removals

### WebGPU: Deprecate GPUAdapter isFallbackAdapter attribute

Deprecates the `GPUAdapter` `isFallbackAdapter` boolean attribute from WebGPU, which is redundant with the `GPUAdapterInfo` `isFallbackAdapter` boolean attribute. This upcoming removal is a minor breaking change as support for fallback adapters has not yet been implemented in any browser, thereby resulting in both `isFallbackAdapter` attributes consistently returning a falsy value.

**References:** [Tracking bug #409259074](https://bugs.chromium.org/p/chromium/issues/detail?id=409259074) | [ChromeStatus.com entry](https://chromestatus.com/feature/5125671816847360) | [Spec](https://gpuweb.github.io/gpuweb/#gpu-adapter)

### Deprecate asynchronous range removal for Media Source Extensions

The Media Source standard long ago changed to disallow ambiguously defined behavior involving asynchronous range removals: `SourceBuffer.abort()` no longer aborts `SourceBuffer.remove()` operations. Setting `MediaSource.duration` can no longer truncate currently buffered media. Exceptions will be thrown in both of these cases now. Safari and Firefox have long shipped this behavior, Chromium is the last browser remaining with the old behavior. Use counters show that around 0.001%-0.005% of page loads hit the deprecated behavior. If a site hits this issue, playback may now break. Usage of `abort()` cancelling removals is increasing, so it's prudent to resolve this deprecation before more incompatible usage appears.

**References:** [Tracking bug #40474569](https://bugs.chromium.org/p/chromium/issues/detail?id=40474569) | [ChromeStatus.com entry](https://chromestatus.com/feature/5073717525970944) | [Spec](https://w3c.github.io/media-source/#dom-sourcebuffer-abort)

---

*Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.*

*Last updated 2025-06-24 UTC.*
