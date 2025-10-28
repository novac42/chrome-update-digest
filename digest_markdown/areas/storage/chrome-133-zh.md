---
layout: default
title: chrome-133-zh
---

## 领域摘要

Chrome 133 引入了 Storage Access Headers，作为已认证嵌入内容选择使用未分区 cookie 的替代性可选机制。此更改允许服务器指示未分区 cookie 是否或可能包含在网络请求中，并使服务器能够激活先前已授予的 'storage-access' 权限。对于开发者，这提供了一条由服务器控制的路径来管理嵌入内容的 cookie 可用性，而无需完全依赖客户端 API。此功能通过在跨源嵌入上下文中为存储访问语义提供更灵活的服务器端控制，推动了 Web 平台的发展。

## 详细更新

本节将摘要扩展为对在嵌入或跨源场景中处理存储的开发者的具体更新和实际影响。

### Storage Access Headers（存储访问标头）

#### 新增内容
提供了一种已认证嵌入内容为未分区 cookie 选择加入的替代方式。这些标头表明未分区 cookie 是否（或可能）包含在某个网络请求中，并允许服务器激活已经授予的 'storage-access' 权限。

#### 技术细节
- 该机制基于标头：服务器可以在网络请求上指示未分区 cookie 的包含或可能包含情况。
- 服务器可以使用这些标头来激活已为某个嵌入之前授予的 'storage-access' 权限。
- 有关确切的标头名称和预期的请求/响应行为，请参见规范和跟踪资源。

#### 适用场景
- 需要未分区 cookie 访问的已认证第三方嵌入（例如小部件、联合服务），同时须尊重用户隐私和权限授予。
- 由服务器驱动的流程，其中服务器负责协调嵌入内容的 storage-access 激活，而不是依赖客户端提示。
- 依赖于嵌入上下文中 cookie 的服务的迁移路径，从仅客户端 API 过渡到通过标头介导的选择加入。

#### 参考资料
- [跟踪 bug #329698698](https://issues.chromium.org/issues/329698698)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6146353156849664)
- [规范](https://privacycg.github.io/storage-access-headers)

## 领域专长（存储相关指导）

- css: 对 CSS 布局的直接影响很小，但依赖服务器端会话状态（通过 cookie）的嵌入组件在启用存储访问时可能改变渲染选择。
- webapi: Storage Access Headers 补充了现有的存储访问 Web API，提供了一个服务器控制的选择加入通道；开发者应将标头使用与客户端权限检查协调起来。
- graphics-webgpu: 对 GPU 没有直接影响，但通过服务器端身份验证解锁更大图形内容的已认证嵌入可能会改变资源预算。
- javascript: 读取 cookie 或依赖 storage-access 状态的脚本应验证基于标头的激活，并在标头缺失时优雅回退。
- security-privacy: 标头将部分控制权转移到服务器；确保与用户同意、同站策略和现有隐私保护配合使用，以避免回归。
- performance: 基于标头的激活可以减少用于权限协商的客户端往返，但可能增加请求/响应的复杂性；衡量对延迟的影响。
- multimedia: 需要已认证会话（DRM/会话 cookie）的媒体嵌入可以利用标头在无需额外客户端提示的情况下恢复访问。
- devices: 设备能力使用不受影响，但使用 cookie 进行个性化的嵌入式设备特定流程可以受益于服务器端激活。
- pwa-service-worker: Service worker 在拦截嵌入作用域的 fetch 时应注意标头影响下的 cookie 可用性。
- webassembly: 依赖已认证存储的 WASM 模块可以依赖服务器激活的访问，但应在运行时验证 cookie 可用性。
- 弃用: 这是一个增加性的可选机制；评估现有基于客户端的 storage-access 流程是否应弃用或为兼容性保留。

保存到: digest_markdown/webplatform/storage/chrome-133-stable-en.md
