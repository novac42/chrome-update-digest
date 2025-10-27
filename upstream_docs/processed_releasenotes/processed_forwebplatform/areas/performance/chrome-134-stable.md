## Performance

### Document-Policy: `expect-no-linked-resources`

The `expect-no-linked-resources` configuration point in Document Policy allows a document to hint to the user agent to better optimize its loading sequence, such as not using the default speculative parsing behavior.

User Agents have implemented speculative parsing of HTML to speculatively fetch resources that are present in the HTML markup, to speed up page loading. For the vast majority of pages on the Web that have resources declared in the HTML markup, the optimization is beneficial and the cost paid in determining such resources is a sound tradeoff. However, the following scenarios might result in a sub-optimal performance tradeoff versus the explicit time spent parsing HTML for determining sub resources to fetch:

  * Pages that don't have any resources declared in the HTML.
  * Large HTML pages with minimal or no resource loads that could explicitly control preloading resources using other preload mechanisms available.

The `expect-no-linked-resources` Document-Policy hints the User Agent that it may choose to optimize out the time spent in such sub resource determination.

[Tracking bug #365632977](https://issues.chromium.org/issues/365632977) | [ChromeStatus.com entry](https://chromestatus.com/feature/5202800863346688) | [Spec](https://github.com/whatwg/html/pull/10718)

### Explicit resource management (async)

These features address a common pattern in software development regarding the lifetime and management of various resources (for example memory and I/O). This pattern generally includes the allocation of a resource and the ability to explicitly release critical resources.

[Tracking bug #42203814](https://issues.chromium.org/issues/42203814) | [ChromeStatus.com entry](https://chromestatus.com/feature/5087324181102592) | [Spec](https://tc39.es/proposal-explicit-resource-management)

### Explicit resource management (sync)

These features address a common pattern in software development regarding the lifetime and management of various resources (for example memory and I/O). This pattern generally includes the allocation of a resource and the ability to explicitly release critical resources.

[Tracking bug #42203506](https://issues.chromium.org/issues/42203506) | [ChromeStatus.com entry](https://chromestatus.com/feature/5071680358842368) | [Spec](https://tc39.es/proposal-explicit-resource-management)

### Extend the `console.timeStamp` API to support measurements and presentation options

Extends the `console.timeStamp()` API, in a backwards-compatible manner, to provide a high-performance method for instrumenting applications and surfacing timing data to the Performance panel in DevTools.

Timing entries added with the API can have a custom timestamp, duration and presentation options (track, swimlane, and color).

[ChromeStatus.com entry](https://chromestatus.com/feature/5133241999425536) | [Spec](https://docs.google.com/document/d/1juT7esZ62ydio-SQwEVsY7pdidKhjAphvUghWrlw0II/edit?tab=t.0#heading=h.ekp1q3o1v7v3)
