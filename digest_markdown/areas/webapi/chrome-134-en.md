---
layout: default
title: chrome-134-en
---

## Area Summary

Chrome 134's Web API updates focus on enhancing privacy-preserving measurement, shared storage capabilities, and API parity while reducing race conditions and improving on-device abuse detection. Key changes include new Shared Storage worklet APIs (interestGroups, Web Locks integration, and Private Aggregation controls), attribution-reporting adjustments, cache-based bounce-tracking mitigations, OffscreenCanvas parity, and an on-device LLM-based notification filter. These changes advance the platform by enabling richer, synchronized measurement and storage workflows while tightening privacy and abuse protections. Developers handling measurement, concurrency, graphics, and notifications should review the new primitives and limits to adapt implementations accordingly.

## Detailed Updates

Below are concise, developer-focused descriptions of each Web API change in Chrome 134 and how they affect common workflows.

### Allow reading interest groups in Shared Storage Worklet

#### What's New
Adds an interestGroups() method to the shared storage worklet that returns the Protected Audience interest groups associated with the shared storage origin's owner, with additional metadata.

#### Technical Details
The worklet API surface now exposes interest group data to Shared Storage worklets, scoped to the shared storage origin's owner; metadata is included per entry.

#### Use Cases
Allows buyers and measurement code running in Shared Storage worklets to inspect associated interest groups to better understand and validate Protected Audience flows.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5074536530444288

### Attribution reporting Feature: Remove aggregatable report limit when trigger context ID is non-null

#### What's New
Removes the existing cap on aggregatable reports per source registration in cases where the trigger context ID is non-null, responding to API caller needs.

#### Technical Details
When a trigger provides a non-null context ID, the previous 20-report limit on aggregatable reports per source registration is lifted to allow higher-volume conversion measurement.

#### Use Cases
Measurement systems that require more than 20 aggregatable reports for certain user flows can now rely on fuller reporting when using trigger context IDs.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5079048977645568

### Bounce tracking mitigations on HTTP Cache

#### What's New
Extends anti-bounce-tracking behavior to the HTTP cache by removing the requirement that a suspected tracking site must have performed storage access to trigger mitigations.

#### Technical Details
Bounce-tracking mitigations are applied to HTTP cache interactions independently of storage-access state, aligning cache-level protections with navigation tracking mitigations defined in the spec.

#### Use Cases
Sites and intermediaries should expect stricter cache behavior for suspected trackers; developers may need to review cross-site measurement that relied on cache semantics.

#### References
- Tracking bug #40264244: https://issues.chromium.org/issues/40264244
- ChromeStatus.com entry: https://chromestatus.com/feature/6299570819301376
- Spec: https://privacycg.github.io/nav-tracking-mitigations/#bounce-tracking-mitigations

### LLM-powered on-device detection of abusive notifications on Android

#### What's New
Introduces on-device LLM-based detection to hide contents of notifications suspected to be abusive, offering users options to dismiss, reveal, or unsubscribe from the origin.

#### Technical Details
An on-device model classifies potentially abusive notifications; flagged notifications are initially hidden until user action.

#### Use Cases
Notification-heavy web apps and push providers should be aware that some notifications may be hidden by default on Android when flagged; implementers should provide clear unsubscribe and user controls.

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5303216063119360

### `OffscreenCanvas` `getContextAttributes`

#### What's New
Adds the getContextAttributes interface from CanvasRenderingContext2D to OffscreenCanvasRenderingContext2D.

#### Technical Details
OffscreenCanvas contexts now expose the same getContextAttributes method signature and behavior as main-thread CanvasRenderingContext2D for retrieving context creation attributes.

#### Use Cases
Worker-based rendering and off-main-thread canvas workflows gain API parity, simplifying feature detection and portability of canvas-based rendering code.

#### References
- Tracking bug #388437261: https://issues.chromium.org/issues/388437261
- ChromeStatus.com entry: https://chromestatus.com/feature/5508068999430144
- Spec: https://github.com/whatwg/html/pull/10904

### Private Aggregation API: per-context contribution limits for Shared Storage callers

#### What's New
Enables Shared Storage callers to set a per-context contribution limit for Private Aggregation reports via a new maxContributions field.

#### Technical Details
Callers can override default contribution counts for Private Aggregation by supplying maxContributions per context, affecting how many contributions are aggregated into reports.

#### Use Cases
Measurement integrators using Shared Storage can tune noise and payload size of Private Aggregation reports to match expected contribution density per context.

#### References
- Tracking bug #376707230: https://issues.chromium.org/issues/376707230
- ChromeStatus.com entry: https://chromestatus.com/feature/5189366316793856
- Spec: https://github.com/patcg-individual-drafts/private-aggregation-api/pull/164/files

### Support Web Locks API in Shared Storage

#### What's New
Integrates the Web Locks API into Shared Storage worklets, adding navigator.locks.request to the worklet environment.

#### Technical Details
Shared Storage worklets can use navigator.locks.request to acquire locks, preventing race conditions across get()/set() operations and duplicate reporting in cross-site measurement.

#### Use Cases
Worklets performing concurrent reads/writes to Shared Storage can serialize critical sections, avoiding duplicate reports and improving data consistency in measurement and storage workflows.

#### References
- Tracking bug #373899210: https://issues.chromium.org/issues/373899210
- ChromeStatus.com entry: https://chromestatus.com/feature/5133950203461632

File saved to: digest_markdown/webplatform/Web API/chrome-134-stable-en.md
