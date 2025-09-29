---
layout: default
title: Area Summary
---

# Area Summary

Chrome 137 (stable) continues the Storage Partitioning work by introducing Blob URL partitioning for navigation and fetch contexts. The main theme is stronger isolation of Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean), with a stated exception for top-level navigations (partitioned only by frame origin). This change most impacts developers who rely on sharing blob: URLs across origins, frames, or storage partitions, and advances the web platform by tightening privacy and storage isolation boundaries. Because the release note text is truncated, see the references for full context.

## Detailed Updates

Below are the Navigation-Loading–specific changes in this release and what they mean for developers.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Chrome partitions Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean), except that top-level navigations remain partitioned only by frame origin.

#### Technical Details
The release note states Blob URL access is tied to Storage Key components (top-level site, frame origin, has-cross-site-ancestor boolean). Top-level navigations are treated as a special case and remain partitioned only by frame origin. The provided description is truncated; consult the links below for the full tracking details.

#### Use Cases
- Sites that create and pass blob: URLs between frames or origins may observe different accessibility semantics when Storage Keys differ.
- Single-origin blob: URLs used for navigation or fetches within the same Storage Key should continue to work, but cross-partition reuse can be restricted.
- Developers using blobs with service workers, cross-origin iframes, or complex multi-site flows should audit blob usage and test navigation/fetch behaviors under partitioning.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)  
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

## Area-Specific Expertise (Navigation-Loading relevance)

- css: Blob URL partitioning is orthogonal to CSS layout but can affect resources referenced via blob: URLs (images, fonts) used in rendering flows.
- webapi: Direct impact — Blob URL access rules are part of fetch/navigation semantics and resource resolution.
- graphics-webgpu: Limited direct impact; blob: resources used as binary inputs to GPU workflows should be validated for partition visibility.
- javascript: JS-created object URLs (URL.createObjectURL) may no longer be accessible across different Storage Keys; audit cross-context message passing.
- security-privacy: Enhances isolation and reduces cross-site data leakage vectors by scoping blob: access to Storage Keys.
- performance: Partitioning may increase cache fragmentation or duplicate data across partitions; measure storage and fetch patterns.
- multimedia: Blob URLs used for media playback should be tested across frames/origins to ensure playback is not broken by partitioning.
- devices: Minimal direct effect; device APIs that accept blob: inputs should respect the same access constraints.
- pwa-service-worker: Service workers that serve blobs or rely on shared blob URLs may need changes to ensure coverage within a partition.
- webassembly: WASM modules loaded via blob: URLs are subject to the same partitioning; verify module load paths.
- deprecations: Treat this as a behavioral migration item — test and update cross-partition blob sharing patterns.

Saved to: digest_markdown/webplatform/Navigation-Loading/chrome-137-stable-en.md
