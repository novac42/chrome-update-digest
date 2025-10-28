# Area Summary

Chrome 141’s Performance updates focus on tuning navigation speculation behavior on desktop to better align prefetch and prerender timing with real user intent. The main change refines the “eager” eagerness level so that it now triggers on a shorter hover than “moderate,” instead of acting the same as “immediate.” This provides a more nuanced balance between responsiveness and when speculative work begins during link-hover interactions. For developers, it means more predictable and practical control over when prefetches and prerenders start, advancing real-world perceived performance for hover-initiated navigations.

## Detailed Updates

This release refines how speculation rules translate user hover intent into actionable prefetch/prerender timing on desktop, offering a clearer separation between eagerness levels.

### Speculation rules: desktop "eager" eagerness improvements

#### What's New
- On desktop, “eager” speculation rules now start prefetches and prerenders when a user hovers a link for a shorter time than the “moderate” hover threshold.
- Previously, “eager” behaved like “immediate,” starting as early as possible.

#### Technical Details
- The trigger condition for “eager” has been adjusted from “as soon as possible” to a hover-duration threshold that is shorter than “moderate.”
- This creates distinct behavior across “immediate,” “eager,” and “moderate,” aligning speculation start times more closely to hover intent on desktop.

#### Use Cases
- Enable earlier-but-not-instant speculative actions for hover-driven navigations, improving responsiveness while differentiating from fully “immediate” behavior.
- Provide developers finer control over when prefetch/prerender begins for desktop users interacting via mouse hover.

#### References
- [ChromeStatus.com entry](https://chromestatus.com/feature/5113430155591680)
- [Spec](https://wicg.github.io/nav-speculation/speculation-rules.html#:~:text=early%20as%20possible.-,%22moderate%22,balance%20between%20%22eager%22%20and%20%22conservative%22.,-%22conservative%22)
