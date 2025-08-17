# Deprecate asynchronous range removal for Media Source extensions

**Relevance Score**: 35.0

**Type**: Chrome Browser changes
**Platform**: Desktop (Linux, Windows, macOS), Mobile (Android)
**Status**: Current
**Categories**: Security/Privacy
**Matched Keywords**: sync

**Description**:
The [Media Source standard](https://www.w3.org/TR/media-source-2/) changed in the past to disallow ambiguously-defined behavior involving asynchronous range removals:
    - `SourceBuffer.abort()` no longer aborts `SourceBuffer.remove()` operations
    - Setting `MediaSource.duration` can no longer truncate currently buffered media
    Exceptions are thrown in both of these cases now. Safari and Firefox have long shipped this behavior; Chromium is the last browser remaining with the old behavior. Use counters show ~0.001%-0.005% of page loads hit the deprecated behavior. If a site hits this issue, playback may now break. Usage of abort() cancelling removals is increasing, so it's prudent to resolve this deprecation before more incompatible usage appears.
    - **Chrome 138 on Windows, macOS, Linux, Android**

**Key Context**: Deprecate a**sync**hronous range removal for Media Source extensions The [Media Source standard](https://www.w3.org/TR/

## Management
