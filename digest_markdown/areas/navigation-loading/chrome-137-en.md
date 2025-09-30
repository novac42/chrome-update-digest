---
layout: default
title: chrome-137-en
---

## Area Summary

Chrome 137 continues the Storage Partitioning work by applying Storage Key partitioning to Blob URL access in the Navigation-Loading domain. The primary change partitions Blob URL access by Storage Key (top-level site, frame origin, and has-cross-site-ancestor), with an explicit exception that top-level navigations remain partitioned only by frame origin. This update most impacts cross-site embedding and navigation flows that rely on Blob URLs, tightening privacy boundaries while minimizing top-level navigation breakage. Developers should evaluate Blob URL usage in cross-origin frames and update tests to reflect new access semantics.

## Detailed Updates

This section lists the Navigation-Loading change in Chrome 137 and its developer implications.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Chrome partitions Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean), except that top-level navigations remain partitioned only by frame origin.

#### Technical Details
- Blob URL access is scoped to a Storage Key composed of the top-level site, the frame origin, and whether the frame has a cross-site ancestor.
- An exception exists: top-level navigations are still partitioned only by the frame origin (not the full Storage Key).
- This aligns Blob URL access control with the broader Storage Partitioning model to reduce cross-site data exposure.

#### Use Cases
- Prevents Blob URLs created in one Storage Key (e.g., an embedded cross-site frame) from being used in a different Storage Key, improving privacy boundaries.
- Minimizes regressions for top-level navigations by keeping them partitioned by frame origin only.
- Requires developers to audit Blob URL sharing patterns across frames and update navigation/test flows that assume global Blob URL accessibility.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646
- https://chromestatus.com/feature/5037311976488960

## Area-Specific Expertise (Navigation-Loading implications)

- css: No direct CSS changes, but cross-origin iframe behaviors that affect scrolling/layout during navigations may need revalidation when Blob URL access changes.
- webapi: Blob URL fetch/navigation semantics are now Storage Key–scoped; APIs that create or resolve Blob URLs must consider storage partition boundaries.
- graphics-webgpu: Blob-sourced assets used for textures or shaders in cross-site frames may become inaccessible across Storage Keys; validate resource loading in GPU pipelines.
- javascript: JS that generates or consumes Blob URLs across frames must handle storage-partitioned access and fallbacks.
- security-privacy: Strengthens privacy by limiting cross-site Blob reuse; reduces risk of cross-site data exfiltration via Blob URLs.
- performance: Partitioning can affect caching/memoization of Blob-backed resources across contexts; review performance assumptions for navigations.
- multimedia: Media elements using Blob URLs in cross-origin frames may experience access restrictions; ensure media provisioning accounts for Storage Key scope.
- devices: Blob-based device data (e.g., camera captures) stored as Blob URLs should respect Storage Key boundaries when used across frames or navigations.
- pwa-service-worker: Service worker fetches and navigation flows that rely on Blob URLs should be tested under Storage Key partitioning.
- webassembly: WASM modules loaded from Blob URLs need to be validated for accessibility across Storage Keys in multi-origin scenarios.
- deprecations: Treat this as a behavioral change rather than a deprecation; provide migration tests and explicit handling for cross-context Blob sharing.
