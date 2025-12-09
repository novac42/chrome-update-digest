### 1. Area Summary

Chrome 143 (stable) introduces a focused Performance change: mobile speculation rules for `eager` eagerness now trigger prefetch and prerender when HTML anchor elements remain briefly in the viewport. This change is medium-impact for developers, improving speculative loading behavior on mobile. It advances the web platform by making speculation more responsive to user-visible link candidates, reducing perceived navigation latency for link-heavy mobile experiences. Teams should note the behavior change to optimize resource usage and user experience.

## Detailed Updates

Below are the Performance-area updates connected to the summary above.

### Speculation rules: mobile `eager` eagerness improvements

#### What's New
On mobile, `eager` eagerness speculation rules prefetches and prerenders now trigger when HTML anchor elements are in the viewport for a short time.

#### Technical Details
This change adjusts when `eager`-level speculative loading activates on mobile devices—specifically tied to anchor elements being briefly visible in the viewport. Implementation and tracking are captured in the Chromium tracking bug and the HTML speculative loading spec.

#### Use Cases
- Link-heavy mobile sites can achieve faster perceived navigations via earlier prefetch/prerender activation.
- Developers should consider how speculative loading timing affects resource budgeting and UX on mobile.

#### References
- [Tracking bug #436705485](https://issues.chromium.org/issues/436705485)  
- [ChromeStatus.com entry](https://chromestatus.com/feature/5086053979521024)  
- [Spec](https://html.spec.whatwg.org/multipage/speculative-loading.html#speculative-loading)