## 区域摘要

Chrome 140 Stable 引入了 Controlled Frame API，专门面向 Isolated Web Apps (IWAs)。主要趋势是通过允许嵌入标准 <iframe> 拒绝的内容来扩展 IWA 的安全嵌入能力，同时让宿主应用对该内容拥有控制权。对于需要在不牺牲隔离保证的情况下将第三方或遗留内容集成到 IWA 的开发者来说，此更改具有重要影响。它通过提供一个新的、IWA 范围的 Web API 来推进 Web 平台，在更丰富的集成与明确的应用级控制之间取得平衡。

## 详细更新

下面的单个功能直接源自摘要，并突出了对 IWA 开发者的实际影响。

### Controlled Frame API (available only to IWAs)（仅对 IWAs 可用）

#### 新增内容
Controlled Frame 是一个仅对 Isolated Web Apps 可用的新 API，能够嵌入所有内容——包括无法在标准 <iframe> 中嵌入的第三方内容——并对该嵌入内容提供编程控制。

#### 技术细节
- 范围：API 面向仅限 IWAs（依据 IWA 模型）。
- 目的：通过提供受控的嵌入原语绕过 iframe 嵌入限制；控制语义和安全模型由规范定义。
- 关键参考和规范文本可在链接的说明文档与规范中查看，以了解实现和行为细节。

与平台领域的关联：
- webapi / javascript: 引入一个新的 JS API，供 IWAs 实例化并控制嵌入的帧。
- security-privacy：改变了 IWA 内的嵌入模型；预期为明确的 IWA 范围隔离语义，而不是广泛的跨源 iframe 行为。
- performance / graphics-webgpu / css：嵌入任意内容可能影响布局和渲染管线；开发者应对渲染和绘制成本进行分析。
- pwa-service-worker：使用 service workers 的 IWAs 可能需要考虑受控 frame 内容的资源路由和缓存。
- 弃用：这并不移除 iframe，而是在 iframe 嵌入被阻止的情况下，提供一个仅限 IWA 的替代原语。

#### 适用场景
- 在传统 <iframe> 嵌入被阻止的情况下，在 IWA 内集成第三方小部件或遗留页面。
- 在 IWA 内构建需要对嵌入式导航和 UI 进行细粒度控制的自助终端或受管内容查看器。
- 使用明确的应用级控制钩子（例如导航、输入调解）创建对远程内容的安全沙箱托管。

#### 参考资料
- https://github.com/WICG/isolated-web-apps/blob/main/README.md — Isolated Web Apps 说明
- https://issues.chromium.org/issues/40191772 — '跟踪缺陷 #40191772'
- https://chromestatus.com/feature/5199572022853632 — ChromeStatus.com 条目
- https://wicg.github.io/controlled-frame — 规范