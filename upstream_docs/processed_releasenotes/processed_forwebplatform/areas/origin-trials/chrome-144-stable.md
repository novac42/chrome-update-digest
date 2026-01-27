## Origin trials

### Enhanced Canvas API `TextMetrics`

Expands the `TextMetrics` Canvas API to support selection rectangles, bounding box queries, and glyph cluster-based operations.

This new functionality enables complex text editing applications with accurate selection, caret positioning, and hit testing. Additionally, cluster-based rendering facilitates sophisticated text effects, for example, independent character animations and styling.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/1646628613757337601) | [Tracking bug #341213359](https://issues.chromium.org/issues/341213359) | [ChromeStatus.com entry](https://chromestatus.com/feature/5075532483657728) | [Spec](https://github.com/whatwg/html/pull/11000)

### Context-aware media elements

Context-aware media elements, are a declarative, user-activated control for accessing the starting and interacting with media streams.

This addresses the long-standing problem of permission prompts being triggered directly from JavaScript without a strong signal of user intent. By embedding a browser-controlled element in the page, the user's click provides a clear, intentional signal. This enables a much better prompt UX and, crucially, provides a recovery path for users who have previously denied the permission.

**Note:** This feature was previously developed and tested in an Origin Trial as the more generic `<permission>` element. Based on feedback from developers and other browser vendors, it has evolved into capability-specific elements to provide a more tailored and powerful developer experience.

[Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3736298840857247745) | [Tracking bug #443013457](https://issues.chromium.org/issues/443013457) | [ChromeStatus.com entry](https://chromestatus.com/feature/4926233538330624) | [Spec](https://wicg.github.io/PEPC/permission-elements.html)
