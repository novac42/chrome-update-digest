## Performance

### Performance and Event Timing: `interactionCount`

The Event Timing API is part of the Performance Timeline and measures the performance of user interactions. Certain events have an `interactionId` value assigned to them. This is useful for grouping related interactions based on common physical user inputs or gestures.

This feature adds a `performance.interactionCount` property, which is the total number of interactions that occurred on the page.

In particular, this feature is useful for computing the Interaction to Next Paint (INP) metric value. This requires knowing the total number of interactions to compute a high percentile score (p98 for pages with more than 50 total interactions).

This feature has been specified for a long time, was prototyped in Chromium a long time ago but never shipped, is part of Interop 2025, and is available in other browsers.

**Note:** A more powerful `performance.eventCounts` map for specific events exists, but you can't accurately map event counts to interaction counts.

[ChromeStatus.com entry](https://chromestatus.com/feature/5153386492198912) | [Spec](https://www.w3.org/TR/event-timing/#dom-performance-interactioncount)
