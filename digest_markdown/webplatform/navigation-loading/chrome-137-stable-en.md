### 1. Area Summary

Chrome 137 continues the Storage Partitioning work by partitioning Blob URL access according to Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean), with the exception that top-level navigations remain partitioned only by frame origin. The most impactful change for developers is that Blob URLs are now scoped more strictly to storage keys, which changes access boundaries for blobs used during fetches and navigations. This advances the web platform by tightening storage and resource isolation across frames and sites, reducing cross-site leakage risk. Teams should review any workflows that rely on shared Blob URL access across origins or frames to ensure compatibility.

## Detailed Updates

Below are the Navigation-Loading changes relevant to developers working on navigation, fetch, and storage isolation.

### Blob URL Partitioning: Fetching/Navigation

#### What's New
Partitioning of Blob URL access is implemented by Storage Key (top-level site, frame origin, and has-cross-site-ancestor boolean); top-level navigations remain partitioned only by frame origin.

#### Technical Details
Blob URL access checks now consider the Storage Key triple (top-level site, frame origin, has-cross-site-ancestor) when deciding whether a blob is accessible from a given context. Top-level navigations are treated as an exception and continue to be partitioned solely by frame origin.

#### Use Cases
- Audit and update codepaths that generate Blob URLs and share them across frames or origins.
- Validate service-worker or fetch flows that expect cross-frame Blob accessibility.
- Test navigations that rely on Blob URLs to ensure they still resolve under the more granular Storage Key partitioning.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

## Area-Specific Expertise

- css: Layout and rendering are unaffected directly, but Blob-based resources used for images or media may be inaccessible across frames if previously shared.
- webapi: Blob URL resolution now consults Storage Key; APIs that pass Blob URLs between contexts should be reviewed.
- graphics-webgpu: No direct change, but GPU resources referencing blob-backed assets should be validated for cross-context access.
- javascript: Blob URL creation and transfer semantics in scripts must account for Storage Key scoping.
- security-privacy: Strengthens isolation by reducing cross-site blob exposure, lowering the surface for cross-origin data leaks.
- performance: Minor regressions possible if developers need to re-fetch blobs across partitions; consider caching strategies per Storage Key.
- multimedia: Media elements sourcing blob: URLs should be tested across frames and navigations for access failures.
- devices: Blob delivery for device-captured data (e.g., camera) may be partitioned by Storage Key; check sharing workflows.
- pwa-service-worker: Service workers interacting with blobs should ensure blobs are available in the service worker’s storage key context.
- webassembly: WASM modules using blob-sourced binaries should validate module fetch paths under the new partitioning.
- deprecations: No explicit deprecations in this change; treat it as a behavioral partitioning update that may require migration of cross-origin blob-sharing patterns.

File path for the generated digest:
digest_markdown/webplatform/Navigation-Loading/chrome-137-stable-en.md