# Chrome 134 Release Notes (Stable)

Source: https://developer.chrome.com/release-notes/134

  * [ Chrome for Developers ](https://developer.chrome.com/)
  * [ Docs ](https://developer.chrome.com/docs)
  * [ Release notes ](https://developer.chrome.com/release-notes)

#  Chrome 134

Stay organized with collections  Save and categorize content based on your preferences. 

**Stable release date:** March 4th, 2025

Unless otherwise noted, the following changes apply to Chrome 134 stable channel release for Android, ChromeOS, Linux, macOS, and Windows. 

Want just the highlights? Check out [New in Chrome 134](/blog/new-in-chrome-134). 

## HTML and DOM

### Customizable `<select>` Element

Customizable `<select>` allows developers to take complete control of the rendering of `<select>` elements by adding the `appearance: base-select` CSS property and value.

This feature relies on the `SelectParserRelaxation` flag, which changes the HTML parser to allow more tags within the `<select>` tag.

[Tracking bug #40146374](https://issues.chromium.org/issues/40146374) | [ChromeStatus.com entry](https://chromestatus.com/feature/5737365999976448) | [Spec](https://github.com/whatwg/html/issues/9799)

### Select parser relaxation

This change makes the HTML parser allow additional tags in `<select>` besides `<option>`, `<optgroup>`, and `<hr>`.

This feature is gated by the temporary policy (`SelectParserRelaxationEnabled`). This is a temporary transition period, and the policy will stop working from Chrome 141.

If you are experiencing problems that you believe are caused by this change, there's a reverse origin trial to disable the parser relaxation.

[Tracking bug #335456114](https://issues.chromium.org/issues/335456114) | [ChromeStatus.com entry](https://chromestatus.com/feature/5145948356083712) | [Spec](https://github.com/whatwg/html/pull/10557)

### Dialog light dismiss

One of the nice features of the Popover API is its light dismiss behavior. This behavior is now part of `<dialog>`, with a new `closedby` attribute controlling the behavior:

  * `<dialog closedby="none">`: No user-triggered closing of dialogs at all.
  * `<dialog closedby="closerequest">`: Pressing `Esc` (or other close trigger) closes the dialog
  * `<dialog closedby="any">`: Clicking outside the dialog, or pressing `Esc`, closes the dialog. Akin to `popover="auto"` behavior.

[Tracking bug #376516550](https://issues.chromium.org/issues/376516550) | [ChromeStatus.com entry](https://chromestatus.com/feature/5097714453577728) | [Spec](https://html.spec.whatwg.org/#attr-dialog-closedby)

## CSS

### CSS highlight inheritance

With CSS highlight inheritance, the CSS highlight pseudo-classes, such as `::selection` and `::highlight`, inherit their properties through the pseudo highlight chain, rather than the element chain. The result is a more intuitive model for inheritance of properties in highlights.

[ChromeStatus.com entry](https://chromestatus.com/feature/5090853643354112) | [Spec](https://drafts.csswg.org/css-pseudo-4/#highlight-cascade)

## PWA

### Document subtitle (Fix PWA app titles)

This feature allows to specify complementary information about the current window of an installed running PWA. It adds a subtitle to the page to provide contextual information that is displayed in the window's title bar. This replaces the text contained in the HTML title element.

[Tracking bug #1351682](https://issues.chromium.org/issues/1351682) | [ChromeStatus.com entry](https://chromestatus.com/feature/5168096826884096) | [Spec](https://github.com/whatwg/html/compare/main...diekus:html:main)

### User link capturing on PWAs

Web links automatically direct users to installed web apps. To better align with users' expectations around installed experiences, Chrome makes it easier to move between the browser and installed web apps. When the user clicks a link that could be handled by an installed web app, the link will open in that installed web app. Users can change this behavior through the installed web app's settings. Developers can control this behavior with the [`launch_handler`](/docs/web-platform/launch-handler) manifest property, and can reference this [developer documentation](https://docs.google.com/document/d/e/2PACX-1vSqYzAmiLr-58OgSWBITtAAu6_2XUpjjNEdMvc6IdZn9DjQCeVrE0SKViumyly0cpryxAONMq62zwHw/pub) for more information about how deep linking works with installed web apps.

[ChromeStatus.com entry](https://chromestatus.com/feature/5194343954776064)

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

## Web APIs

### Allow reading interest groups in Shared Storage Worklet

Adds an `interestGroups()` method to the shared storage worklet, to return the Protected Audience interest groups associated with the shared storage origin's owner, with some additional metadata.

This API provides the Protected Audience buyer with a better picture of what's happening with their users, allowing for Private Aggregation reports.

[ChromeStatus.com entry](https://chromestatus.com/feature/5074536530444288)

### Attribution reporting Feature: Remove aggregatable report limit when trigger context ID is non-null

This change is based on API caller feedback and the need for being able to measure a higher number of conversion events for certain user flows.

Currently the API has a limit that allows up to 20 aggregatable reports to be generated per source registration which is restrictive for use cases where a user may have a longer user journey. This change removes the aggregatable report limit when a trigger context ID is provided as part of the registration. The removal of this limit is restricted to only when the trigger context ID is specified, because when it is specified the API applies a higher rate of null reports which helps to protect against cross-site information leaking through report counts.

Additionally, aggregatable reports will still be bound by other limits that restrict the total amount of information that can be measured, such as the L1 contribution budget (65,536) per source and the attribution rate limit.

[ChromeStatus.com entry](https://chromestatus.com/feature/5079048977645568)

### Bounce tracking mitigations on HTTP Cache

Bounce tracking mitigations for the HTTP cache is an extension to existing anti-bounce-tracking behavior. It removes the requirement that a suspected tracking site must have performed storage access in order to activate bounce tracking mitigations.

Chrome's initially proposed bounce tracking mitigation solution triggers when a site accesses browser storage (for example, in cookies) during a redirect flow. However, bounce trackers can systematically circumvent such mitigations by using the HTTP cache to preserve data. By relaxing the triggering conditions for bounce tracking mitigations, the browser should be able to catch bounce trackers using the HTTP cache.

[Tracking bug #40264244](https://issues.chromium.org/issues/40264244) | [ChromeStatus.com entry](https://chromestatus.com/feature/6299570819301376) | [Spec](https://privacycg.github.io/nav-tracking-mitigations/#bounce-tracking-mitigations)

### LLM-powered on-device detection of abusive notifications on Android

This launch aims to hide the contents of notifications that are suspected to be abusive. The user will then have the options to dismiss, show the notification, or unsubscribe from the origin. This detection is to be done by an on-device model.

[ChromeStatus.com entry](https://chromestatus.com/feature/5303216063119360)

### `OffscreenCanvas` `getContextAttributes`

Add the `getContextAttributes` interface from `CanvasRenderingContext2D` to `OffscreenCanvasRenderingContext2D`.

[Tracking bug #388437261](https://issues.chromium.org/issues/388437261) | [ChromeStatus.com entry](https://chromestatus.com/feature/5508068999430144) | [Spec](https://github.com/whatwg/html/pull/10904)

### Private Aggregation API: per-context contribution limits for Shared Storage callers

Enables Shared Storage callers to customize the number of contributions per Private Aggregation report.

This feature enables Shared Storage callers to configure per-context contribution limits with a new field, `maxContributions`. Callers set this field to override the default number of contributions per report—larger and smaller numbers will both be permitted. Chrome will accept values of `maxContributions` between 1 and 1000 inclusive; larger values will be interpreted as 1000.

Due to padding, the size of each report's payload will be roughly proportional to the chosen number of contributions per report. We expect that opting into larger reports will increase the cost of operating the Aggregation Service.

Protected Audience callers won't be affected by this feature. However, we are planning to add support for customizing the number of contributions for Protected Audience reports in future features.

[Tracking bug #376707230](https://issues.chromium.org/issues/376707230) | [ChromeStatus.com entry](https://chromestatus.com/feature/5189366316793856) | [Spec](https://github.com/patcg-individual-drafts/private-aggregation-api/pull/164/files)

### Support Web Locks API in Shared Storage

Integrates the Web Locks API into Shared Storage. This prevents scenarios such as where cross-site reach measurement can result in duplicate reporting, due to the potential race conditions within the `get()` and `set()` logic.

This change:

  * Introduces `navigator.locks.request` to the worklet environment.
  * Introduces `{ withLock: <resource>}` option to all modifier methods.
  * Introduces a batch modify method: `sharedStorage.batchUpdate(methods, options)`. This method, with the `withLock` option, allows multiple modifier methods to be executed atomically, enabling use cases where a website needs to maintain consistency while updating data organized across multiple keys.

[Tracking bug #373899210](https://issues.chromium.org/issues/373899210) | [ChromeStatus.com entry](https://chromestatus.com/feature/5133950203461632)

## Rendering and graphics

### Support `ImageSmoothingQuality` in `PaintCanvas`

Add support for the `imageSmoothingQuality` attribute on Paint Canvas. This lets you choose the quality or performance tradeoff when scaling images. There are three options in total for `imageSmoothingQuality`: `low`, `medium` and `high`.

[Tracking bug #None](https://issues.chromium.org/issues/None) | [ChromeStatus.com entry](https://chromestatus.com/feature/4666019443113984) | [Spec](https://drafts.css-houdini.org/css-paint-api-1/#paintrenderingcontext2d)

### WebGPU subgroups

Adds subgroup functionality to WebGPU. Subgroup operations perform SIMT operations to provide efficient communication and data sharing among groups of invocations. These operations can be used to accelerate applications by reducing memory overheads incurred by inter-invocation communication.

[ChromeStatus.com entry](https://chromestatus.com/feature/5126409856221184) | [Spec](https://github.com/gpuweb/gpuweb/pull/4963)

## WebGPU

### Improve machine-learning workloads with subgroups

After a year of development and trials, the subgroups WebGPU feature enabling SIMD-level parallelism is now available. It allows threads in a workgroup to communicate and execute collective math operations, such as calculating a sum of numbers, and offers an efficient method for cross-thread data sharing. See the [original proposal](https://github.com/gpuweb/gpuweb/blob/main/proposals/subgroups.md) and [chromestatus entry](https://chromestatus.com/feature/5126409856221184).

For reference, Google Meet saw 2.3-2.9 times speed increases when benchmarking subgroups against [packed integer dot products](/blog/io24-webassembly-webgpu-2#packed_integer_dot_products) for matrix-vector multiply shaders on some devices during the [origin trial](https://developer.chrome.com/origintrials/#/view_trial/4130363808252166145).

When the `"subgroups"` feature is available in a `GPUAdapter`, request a `GPUDevice` with this feature to get subgroups support in WGSL. It's helpful to check `subgroupMinSize` and `subgroupMaxSize` adapter info values—for example, if you have a hardcoded algorithm that requires a subgroup of a certain size.

You also need to explicitly enable this extension in your WGSL code with `enable subgroups;` to get access to the following built-in values in both compute and fragment shaders stages:

  * `subgroup_invocation_id`: A built-in value for the index of the thread within the subgroup.

  * `subgroup_size`: A built-in value for subgroup size access.

The numerous [subgroup built-in functions](https://gpuweb.github.io/gpuweb/wgsl/#subgroup-builtin-functions) (for example, `subgroupAdd()`, `subgroupBallot()`, `subgroupBroadcast()`, `subgroupShuffle()`) enable efficient communication and computation between invocations within a subgroup. These subgroup operations are classified as single-instruction multiple-thread (SIMT) operations. Additionally, the [quad built-in functions](https://gpuweb.github.io/gpuweb/wgsl/#quad-builtin-functions), which operate on a [quad](https://gpuweb.github.io/gpuweb/wgsl/#quad) of invocations facilitate data communication within the quad.

You can use f16 values with subgroups when you request a `GPUDevice` with both `"shader-f16"` and `"subgroups"` features.

The following sample is a good starting point for exploring subgroups: it shows a shader that uses the `subgroupExclusiveMul()` built-in function to compute factorials without reading or writing memory to communicate intermediate results.

See the Pen [WebGPU subgroups](https://codepen.io/web-dot-dev/pen/emOqWQJ). 

### Remove float filterable texture types support as blendable

Now that the [32-bit float textures blending](/blog/new-in-webgpu-132#32-bit_float_textures_blending) is available with the `"float32-blendable"` feature, the incorrect support for float filterable texture types as blendable is removed. See [issue 364987733](https://issues.chromium.org/issues/364987733).

### Dawn updates

Dawn now requires macOS 11 and iOS 14 and only supports Metal 2.3+. See [issue 381117827](https://crbug.com/381117827).

The new `GetWGSLLanguageFeatures()` method of the `wgpu::Instance` now replaces `EnumerateWGSLLanguageFeatures()`. See [issue 368672124](https://issues.chromium.org/issues/368672124).

The following binding types have an `Undefined` value and their default values in binding layout have been changed. See [issue 377820810](https://issues.chromium.org/issues/377820810).

  * `wgpu::BufferBindingType::Undefined` is now `Uniform`
  * `wgpu::SamplerBindingType::Undefined` is now `Filtering`
  * `wgpu::TextureSampleType::Undefined` is now `Float`
  * `wgpu::StorageTextureAccess::Undefined`is now `WriteOnly`

This covers only some of the key highlights. Check out the exhaustive [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/6943..chromium/6998?n=1000).

## Origin trials

### Digital Credential API

Websites can and do get credentials from mobile wallet apps through a variety of mechanisms today, for example, custom URL handlers and QR code scanning. This feature lets sites request identity information from wallets using Android's `IdentityCredential` `CredMan` system. It is extensible to support multiple credential formats (for example, ISO mDoc and W3C verifiable credential) and allows multiple wallet apps to be used. Mechanisms are being added to help reduce the risk of ecosystem-scale abuse of real-world identity.

The origin trial starting in Chrome 134 adds support for this API on desktop platform, where Chrome on Desktop will securely communicate with the digital wallet on the Android phone to fetch the requested credentials.

[Origin Trial](/origintrials#/view_trial/3139571890230657025) | [Tracking bug #40257092](https://issues.chromium.org/issues/40257092) | [ChromeStatus.com entry](https://chromestatus.com/feature/5166035265650688) | [Spec](https://wicg.github.io/digital-credentials)

### Deprecation trial for `SelectParserRelaxation`

This is a deprecation trial, which re-enables the old parser behavior for parsing `<select>` tags. Under that old behavior, non-supported content is silently discarded and not included in the DOM content underneath the `<select>`. This trial can be used in case the new behavior enabled from Chrome 135 breaks a site.

[Origin Trial](/origintrials#/view_trial/182958734861926401) | [ChromeStatus.com entry](https://chromestatus.com/feature/5145948356083712)

## Deprecations and removals

### Remove nonstandard `getUserMedia` audio constraints

Blink supports a number of nonstandard `goog`-prefixed constraints for `getUserMedia` from some time before constraints were properly standardized.

Usage has gone down significantly to between 0.000001% to 0.0009% (depending on the constraint) and some of them don't even have an effect due to changes in the Chromium audio-capture stack. Soon none of them will have any effect due to other upcoming changes.

We don't expect any major regressions due to this change. Applications using these constraints will continue to work, but will get audio with default settings (as if no constraints were passed). They can opt to migrate to standard constraints.

[Tracking bug #377131184](https://issues.chromium.org/issues/377131184) | [ChromeStatus.com entry](https://chromestatus.com/feature/5097536380207104) | [Spec](https://w3c.github.io/mediacapture-main/#media-track-constraints)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-03-04 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-03-04 UTC."],[],[]] 
