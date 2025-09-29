## Area Summary

Chrome 137 继续通过 Storage Partitioning 的工作，根据 Storage Key（top-level site、frame origin 和 has-cross-site-ancestor 标志）对 Blob URL 访问进行分区，但有意保留一个例外：顶级导航仍仅按 frame origin 分区。对开发者影响最大的变化是跨存储分区对 Blob URL 的隐式共享减少，这会影响跨框架和源如何获取或导航到 blobs。此举通过收紧数据隔离并使 blob 处理与 site-isolation 和隐私目标一致，推进了 Web 平台。生成或在框架、service workers 或导航之间传递 Blob URL 的团队应审查共享模式并测试跨源场景。

## Detailed Updates

Below are the Navigation-Loading–specific changes in Chrome 137 derived from the release data.

### Blob URL Partitioning: Fetching/Navigation (Blob URL 访问分区：获取/导航)

#### What's New
Partitioning of Blob URL access by Storage Key (top-level site, frame origin, and the has-cross-site-ancestor boolean) has been implemented as part of Storage Partitioning. Top-level navigations are an exception and remain partitioned only by frame origin.

#### Technical Details
This feature continues Storage Partitioning work; Blob URL access is scoped to Storage Key components listed above. The described exception (top-level navigations partitioned only by frame origin) is preserved per the release notes.

#### Use Cases
- Prevent accidental cross-site access to blobs created in a different storage partition.
- Require explicit sharing strategies if blobs must be consumed across different top-level sites or cross-site frames.
- Review PWA, service-worker, and navigation flows that rely on blob: URLs to ensure expected availability after partitioning.

#### References
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)  
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

## Area-Specific Expertise (Navigation-Loading implications)

- css: 验证在 CSS 中使用的基于 Blob 的任何资源（例如通过 blobs 生成并用于 `url()` 引用的数据）是否在相同的 storage partition 中提供，或已针对分区进行调整。
- webapi: Blob URL 创建和 fetch/navigation 语义现在以分区为范围；将 `blob:` URLs 在帧之间传递的 APIs 可能需要进行协调。
- graphics-webgpu: 如果 Blob URL 提供跨帧加载的 shader 或二进制资产，请确保分区对齐以避免资源丢失。
- javascript: 在 window/frames 之间发布 Blob URL 的代码可能会因 Storage Key 而表现出不同的可用性；请在跨源测试用例中验证。
- security-privacy: 更强的隔离减少了与 Blob URL 相关的跨站数据泄露向量。
- 性能: 当在不同分区中重新请求 blobs 时，分区可能影响缓存命中或资源重用。
- multimedia: 基于 Blob 的媒体源（例如用于媒体的 object URLs）应在导航和框架间验证其可用性。
- devices: 来自生成 blobs 的设备 API 的文件/Blob 访问模式必须考虑分区边界。
- pwa-service-worker: 涉及 Blob URL 的 service worker fetch/navigation 可能受到影响；请测试离线场景以及提供或转发 blobs 的 fetch 处理程序。
- webassembly: 通过 Blob URL 交付的 WASM 二进制在跨帧使用时需要分区感知的加载。
- 弃用: 未宣布任何弃用；将此视为行为改变，在依赖 Blob 共享的场景中需要进行迁移/测试。