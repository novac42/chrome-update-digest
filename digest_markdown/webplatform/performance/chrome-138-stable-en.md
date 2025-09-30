## Area Summary

Chrome 138 (stable) continues to refine prerendering and prefetching controls to improve runtime performance and developer control. The release adds targeted Clear-Site-Data values to evict prefetch and prerender caches, and extends speculation rules with a target_hint to better associate prerendered pages with their eventual navigable targets. These changes give developers finer-grained lifecycle control of speculative resources, reducing stale cache usage and improving activation accuracy for prerendered content. For performance-focused teams, the updates help manage memory, resource reuse, and navigation activation behavior more predictably.

## Detailed Updates

Below are the Performance-area updates from Chrome 138 that flow directly from the summary above.

### Add prefetchCache and prerenderCache to Clear-Site-Data header

#### What's New
Two new values for the Clear-Site-Data header to help developers target clearing the prerender and prefetch cache: "prefetchCache" and "prerenderCache".

#### Technical Details
Clear-Site-Data gains two explicit cache directives that map to the browser's prefetch and prerender caches. The change is tracked in Chromium and referenced by the Clear-Site-Data spec.

#### Use Cases
- Precisely evict stale prefetch/prerendered resources without clearing other site data.
- Reduce memory and network usage by invalidating speculative caches when app state changes.
- Improve correctness when server-side changes make prefetched/prerendered responses obsolete.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=398149359  
https://chromestatus.com/feature/5110263659667456  
https://w3c.github.io/webappsec-clear-site-data/#grammardef-cache-directive

### Speculation rules: target_hint field

#### What's New
Speculation rules syntax now allows developers to specify the target_hint field, providing a hint about the target navigable where a prerendered page will eventually be activated.

#### Technical Details
The target_hint hint signals the anticipated navigable target (for example, when `_blank` is provided) so a prerendered page can be matched and activated for that target when navigation occurs. The feature is tracked in Chromium and specified in the nav-speculation spec.

#### Use Cases
- Improve activation accuracy of prerendered pages by indicating the intended target context (e.g., same tab vs. new tab).
- Enable better resource scheduling and lifecycle decisions for prerendered documents based on intended activation target.

#### References
https://bugs.chromium.org/p/chromium/issues/detail?id=40234240  
https://chromestatus.com/feature/5084493854924800  
https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-target-hint

Saved file: digest_markdown/webplatform/Performance/chrome-138-stable-en.md