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
