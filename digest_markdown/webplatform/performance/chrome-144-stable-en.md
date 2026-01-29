# Chrome 144 Stable - Performance Updates

## Area Summary

Chrome 144 introduces a significant enhancement to the Event Timing API through the new `performance.interactionCount` property, bringing Chromium into alignment with other major browsers and the Interop 2025 initiative. This feature addresses a critical gap in measuring user interaction performance by providing developers with an accurate count of total interactions on a page, which is essential for calculating the Interaction to Next Paint (INP) metric. As part of the Performance Timeline specification, this update enables more precise performance monitoring and helps developers optimize user experience by identifying interaction bottlenecks. The addition of this long-specified feature demonstrates Chrome's commitment to standardizing performance measurement tools across the web platform.

## Detailed Updates

Chrome 144's performance improvements focus on enhancing the measurement capabilities of user interactions through the Event Timing API, providing developers with better tools to monitor and optimize page responsiveness.

### Performance and Event Timing: `interactionCount`

#### What's New

Chrome 144 introduces the `performance.interactionCount` property, which tracks the total number of user interactions that have occurred on a page. This property works in conjunction with the existing Event Timing API to provide comprehensive interaction performance data.

#### Technical Details

The Event Timing API is part of the Performance Timeline and measures the performance of user interactions. Certain events have an `interactionId` value assigned to them, which groups related interactions based on common physical user inputs or gestures. The new `performance.interactionCount` property complements this by maintaining a running count of all interactions on the page.

This feature has been specified for a long time and was previously prototyped in Chromium but never shipped. It is now part of the Interop 2025 initiative and is already available in other major browsers, ensuring cross-browser compatibility.

**Note:** While a more powerful `performance.eventCounts` map exists for tracking specific events, it cannot accurately map event counts to interaction counts, making `interactionCount` essential for interaction-specific metrics.

#### Use Cases

The primary use case for this feature is computing the Interaction to Next Paint (INP) metric value, which is a critical Core Web Vital for measuring page responsiveness. INP requires knowing the total number of interactions to compute a high percentile score (p98 for pages with more than 50 total interactions). With `performance.interactionCount`, developers can:

- Accurately calculate INP metrics for performance monitoring
- Identify pages with high interaction volumes that may need optimization
- Build more sophisticated user experience analytics
- Ensure consistent performance measurement across different browsers

#### References

- [ChromeStatus.com entry](https://chromestatus.com/feature/5153386492198912)
- [Spec](https://www.w3.org/TR/event-timing/#dom-performance-interactioncount)
