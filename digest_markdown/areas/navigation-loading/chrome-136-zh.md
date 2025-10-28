---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 136 在 Navigation-Loading 中引入了一项以隐私为导向的更改：HTTP 缓存键现在包含一个 `is-cross-site-main-frame-navigation` 布尔值。此更改旨在针对利用顶级导航推断缓存状态的跨站泄露攻击。对开发者而言，最重要的影响是缓存键（从而缓存命中/未命中）可能会根据导航发起者而不同，这可能影响缓存假设和测试。总体而言，此更新通过增强缓存分区来提升 Web 隐私，同时不改变 HTTP 缓存规范定义的缓存语义。

## 详细更新

以下为 Chrome 136 中 Navigation-Loading 更改的详细信息及开发者应注意的要点。

### Incorporate navigation initiator into the HTTP cache partition key (将导航发起者纳入 HTTP 缓存分区键)

#### 新增内容
Chrome 的 HTTP 缓存键控方案更新为包含一个 `is-cross-site-main-frame-navigation` 布尔值，以缓解涉及顶级导航的跨站泄露攻击。

#### 技术细节
- 缓存分区键现在会编码请求是否由跨站顶级导航发起（`is-cross-site-main-frame-navigation`）。
- 该布尔值用于区分缓存条目，使作为此类导航一部分获取的资源被单独键控，从而降低攻击者通过触发导航推断缓存状态的风险。
- 此更改基于标准 HTTP 缓存行为，同时向键控添加了原点-导航上下文。

#### 适用场景
- 提升易受顶级导航跨站探测影响的网站的隐私保护。
- 与依赖导航驱动流程中确定性缓存命中行为的开发者相关——在导航发起者相关的场景中测试并验证缓存逻辑。
- 影响导航密集型应用（包括 PWAs 和具有跨源重定向的网站）的缓存分析、自动化测试和安全评审。

#### 参考资料
- [Tracking bug #398784714](https://bugs.chromium.org/p/chromium/issues/detail?id=398784714)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5108419906535424)
- [Spec](https://httpwg.org/specs/rfc9110.html#caching)

## 领域专门知识（Navigation-Loading 聚焦）

- css: 布局和绘制不受缓存键控影响；但是，资源计时和缓存状态可能会改变导航时的渲染性能。
- webapi: 对于由导航发起的请求，Fetch 和缓存行为可能产生不同的缓存命中；请验证 Fetch API 与 navigation preload 的交互。
- graphics-webgpu: 对 GPU 管线没有直接影响，但改变的缓存命中可能会改变资源获取时序，从而影响 GPU 上传延迟。
- javascript: 应测试 V8 和脚本驱动的导航中依赖缓存的逻辑（例如，导航驱动的模块获取）。
- security-privacy: 此更改通过基于导航上下文限定缓存条目范围，关闭了一类跨站缓存探测攻击。
- performance: 预计缓存命中率可能发生变化；在更改后测量端到端的导航延迟。
- multimedia: 顶级导航的媒体资源缓存可能会被不同地分区；验证流媒体启动行为。
- devices: 硬件触发的导航不太可能受到影响，但缓存语义对传感器驱动的用户体验仍很重要。
- pwa-service-worker: 应审核 Service Worker 的缓存使用和预期——Service Worker 控制的响应仍遵循 HTTP 缓存规则，但导航上下文可能改变键控。
- webassembly: 导航期间的 WASM 模块获取可能会看到不同的缓存结果；应重新验证预取策略。
- 弃用: 未宣布弃用；将此视为互操作性/行为更改并相应更新测试。

保存到：digest_markdown/webplatform/Navigation-Loading/chrome-136-stable-en.md
