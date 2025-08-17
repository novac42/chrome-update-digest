```markdown
# Chrome 132 全领域更新摘要

---

## 1. 执行摘要

Chrome 132 带来了多项 Web 平台关键更新，涵盖 CSS、Web API、WebGPU、设备支持、安全隐私、性能优化、多媒体能力、PWA、弃用与迁移等领域。主要亮点包括：CSS anchor-size() 支持扩展、Fetch/PushMessageData/Response/Request 新增 bytes() 方法、WebGPU 多项能力增强、File System Access API 扩展至 Android/WebView、对 localhost 忽略 Strict-Transport-Security、Element Capture 与多屏幕捕获 API、WebAuthn Signal API、FedCM 新模式、以及一系列弃用和安全策略调整。这些变更提升了开发者体验、Web 应用能力与平台一致性，同时也带来部分兼容性与安全风险，需要开发团队密切关注并及时适配。

---

## 2. 关键影响

#### 技术影响

- **现有实现影响**：部分 API 行为变更（如 popover/dialog 在非激活文档抛异常、navigator.storage 不再为 EventTarget、移除 HTMLVideoElement 前缀全屏 API）可能影响依赖旧行为的代码。
- **新功能可用**：CSS anchor-size() 在 inset/margin、Fetch/PushMessageData/Response/Request bytes()、WebGPU 32-bit float blending/adapterInfo/texture view usage、Element Capture、getAllScreensMedia()、Device Posture API、File System Access for Android/WebView、WebAuthn Signal API、FedCM Mode/Use Other Account 等，极大丰富了 Web 平台能力。
- **技术债务考虑**：弃用 prefixed fullscreen API、navigator.storage EventTarget、部分权限策略默认值变更，需及时迁移和清理遗留代码。

---

## 3. 风险评估

**关键风险**：

- 破坏性更改：移除 HTMLVideoElement 前缀全屏 API、navigator.storage 不再为 EventTarget、popover/dialog 在非激活文档抛异常，可能导致旧代码报错或功能失效。
- 安全考虑：getAllScreensMedia()、Element Capture 涉及多屏/区域捕获，需严格权限与企业策略控制；Document-Isolation-Policy、Strict-Transport-Security 忽略 localhost 提升安全隔离与开发便利。

**中等风险**：

- 弃用：prefixed fullscreen API、navigator.storage EventTarget，需关注兼容性与用户影响。
- 性能影响：WebGPU 新特性、显式编译提示（magic comments）等，需评估实际性能收益与潜在回归。

---

## 4. 建议行动

#### 立即行动

- 检查并迁移依赖 HTMLVideoElement 前缀全屏 API、navigator.storage EventTarget 的代码。
- 适配 popover/dialog 异常行为，完善异常处理。
- 评估并利用 Fetch/PushMessageData/Response/Request bytes()、File System Access for Android/WebView、WebGPU 新能力等提升应用体验。

#### 短期规划

- 跟进 getAllScreensMedia()、Element Capture、Device Posture API、WebAuthn Signal API、FedCM 新模式等新特性，探索创新用例。
- 审查权限策略、存储、隔离策略相关变更，确保安全合规。
- 关注 CSS anchor-size()、writing-mode、keyboard focusable scroll containers 等布局与可访问性提升。

#### 长期战略

- 持续关注 WebGPU、WebAuthn、FedCM、PWA、设备 API 等领域演进，规划跨平台能力升级。
- 清理遗留兼容性代码，推动现代 Web API 迁移。
- 加强安全、隐私、性能监控，适应平台策略调整。

---

## 5. 功能分析

### Throw exception for popovers and dialogs in non-active documents

**影响级别**：🔴 关键

**变更内容**：
在非激活文档中调用 showPopover() 或 showModal() 现在会抛出 InvalidStateError 异常，而不是静默失败。

**重要性**：
提升了 API 行为一致性和可调试性，防止开发者误判弹窗未显示原因。

**实施指南**：
- 检查相关代码，补充异常捕获与处理逻辑。
- 避免在非激活文档中操作弹窗。

**参考资料**：
[Tracking bug #373684393](https://issues.chromium.org/issues/373684393) | [ChromeStatus.com entry](https://chromestatus.com/feature/6352111728852992) | [Spec](https://github.com/whatwg/html/pull/10705)

---

### Dialog toggle events

**影响级别**：🟡 重要

**变更内容**：
<dialog> 元素现在支持 ToggleEvent，打开/关闭时会分别派发 newState=open/closed 的事件。

**重要性**：
简化了对 dialog 状态变化的监听，提升开发便利性。

**实施指南**：
- 使用 ToggleEvent 替代 MutationObserver 监听 dialog 状态。
- 优化相关事件处理逻辑。

**参考资料**：
[Tracking bug #41494780](https://issues.chromium.org/issues/41494780) | [ChromeStatus.com entry](https://chromestatus.com/feature/5078613609938944) | [Spec](https://github.com/whatwg/html/pull/10091)

---

### Fix selection `isCollapsed` in Shadow DOM

**影响级别**：🟡 重要

**变更内容**：
Selection.isCollapsed 在 Shadow DOM 下行为修正，anchor 和 focus 相同时才为 true。

**重要性**：
保证 Selection API 在 Shadow DOM 与 Light DOM 下行为一致，减少兼容性问题。

**实施指南**：
- 检查依赖 Selection.isCollapsed 的逻辑，确保兼容新行为。

**参考资料**：
[Demo](https://codepen.io/Di-Zhang/pen/jOjdeoX) | [Tracking bug #40400558](https://issues.chromium.org/issues/40400558) | [ChromeStatus.com entry](https://chromestatus.com/feature/5175599392620544) | [Spec](https://w3c.github.io/selection-api/#dom-selection-iscollapsed)

---

### CSS Anchor Positioning: allow `anchor-size()` in `inset` and `margin` properties

**影响级别**：🟡 重要

**变更内容**：
anchor-size() 现可用于 inset 和 margin 属性，原本仅限 sizing 属性。

**重要性**：
增强了 CSS Anchor Positioning 灵活性，便于实现复杂布局。

**实施指南**：
- 利用 anchor-size() 优化定位和响应式布局。
- 检查旧代码，适配新用法。

**参考资料**：
[Tracking bug #346521300](https://issues.chromium.org/issues/346521300) | [ChromeStatus.com entry](https://chromestatus.com/feature/5203950077476864) | [Spec](https://drafts.csswg.org/css-anchor-position-1/#anchor-size-fn)

---

### CSS sideways writing modes

**影响级别**：🟢 可选

**变更内容**：
writing-mode 属性新增 sideways-rl 和 sideways-lr，适用于非 CJK 垂直文本。

**重要性**：
提升多语言排版支持，丰富排版表现力。

**实施指南**：
- 在需要非 CJK 垂直文本时使用 sideways-rl/lr。

**参考资料**：
[MDN writing-mode](https://developer.mozilla.org/docs/Web/CSS/writing-mode) | [Tracking bug #40501131](https://issues.chromium.org/issues/40501131) | [ChromeStatus.com entry](https://chromestatus.com/feature/6201053052928000) | [Spec](https://drafts.csswg.org/css-writing-modes/#propdef-writing-mode)

---

### Fetch: `Request.bytes()` and `Response.bytes()`

**影响级别**：🟡 重要

**变更内容**：
Request 和 Response 新增 bytes() 方法，直接返回 Uint8Array，提升二进制数据处理便捷性。

**重要性**：
简化了二进制数据读取流程，提升开发效率。

**实施指南**：
- 用 bytes() 替代 arrayBuffer() + Uint8Array 的组合用法。

**参考资料**：
[Tracking bug #340206277](https://issues.chromium.org/issues/340206277) | [ChromeStatus.com entry](https://chromestatus.com/feature/5239268180754432) | [Spec](https://fetch.spec.whatwg.org/#dom-body-bytes)

---

### Ignore `Strict-Transport-Security` for localhost

**影响级别**：🟡 重要

**变更内容**：
localhost 响应将忽略 Strict-Transport-Security 头，避免开发环境端口间 STS 污染。

**重要性**：
极大提升本地开发体验，避免 STS 误配置导致的调试障碍。

**实施指南**：
- 本地开发无需担心 STS 影响，生产环境仍需正确配置 STS。

**参考资料**：
[Tracking bug #41251622](https://issues.chromium.org/issues/41251622) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134293196865536)

---

### Capture all screens

**影响级别**：🟡 重要

**变更内容**：
getAllScreensMedia() 支持一次性捕获所有屏幕，需企业策略允许，仅限桌面端。

**重要性**：
便于多屏协作、演示、远程办公等场景，提升多媒体能力。

**实施指南**：
- 需配置 MultiScreenCaptureAllowedForUrls 策略。
- 明确用户授权与隐私提示。

**参考资料**：
[Design Doc](https://docs.google.com/document/d/1XB8rQRnY5N8G2PeEcNJpVO0q22CutvwW8GGKCZ1z_vc/preview?tab=t.0) | [Tracking bug #40216442](https://issues.chromium.org/issues/40216442) | [ChromeStatus.com entry](https://chromestatus.com/feature/6284029979525120) | [Spec](https://screen-share.github.io/capture-all-screens)

---

### Element Capture

**影响级别**：🟡 重要

**变更内容**：
Element Capture 支持对 tab-capture 获得的视频流，仅捕获指定 DOM 子树内容。

**重要性**：
提升区域录制灵活性，便于实现高定制化屏幕分享。

**实施指南**：
- 结合 MediaStreamTrack 使用，按需捕获页面区域。

**参考资料**：
[Demo](https://element-capture-demo.glitch.me/) | [Tracking bug #270230413](https://issues.chromium.org/issues/270230413) | [ChromeStatus.com entry](https://chromestatus.com/feature/5198989277790208) | [Spec](https://screen-share.github.io/element-capture)

---

### `PushMessageData::bytes()`

**影响级别**：🟡 重要

**变更内容**：
PushMessageData 新增 bytes() 方法，与 Body 接口保持一致，直接获取 Uint8Array。

**重要性**：
统一 API 设计，简化推送消息二进制处理。

**实施指南**：
- 用 bytes() 替代 arrayBuffer() + Uint8Array。

**参考资料**：
[MDN PushMessageData: bytes() method](https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData/bytes) | [Tracking bug #373336950](https://issues.chromium.org/issues/373336950) | [ChromeStatus.com entry](https://chromestatus.com/feature/5117729756151808) | [Spec](https://www.w3.org/TR/push-api/#dom-pushmessagedata-bytes)

---

### Keyboard focusable scroll containers

**影响级别**：🟡 重要

**变更内容**：
修复可键盘聚焦滚动容器的可访问性回归，继续推广该特性。

**重要性**：
提升无障碍体验，便于键盘用户操作滚动区域。

**实施指南**：
- 检查滚动容器聚焦行为，确保无障碍兼容。

**参考资料**：
[Tracking bug #40113891](https://issues.chromium.org/issues/40113891) | [ChromeStatus.com entry](https://chromestatus.com/feature/5231964663578624) | [Spec](https://drafts.csswg.org/css-overflow-3/#scroll-container)

---

### Device Posture API

**影响级别**：🟡 重要

**变更内容**：
Device Posture API 支持检测可折叠设备当前姿态，便于适配不同物理形态。

**重要性**：
为折叠屏等新型设备提供更佳体验，支持创新布局。

**实施指南**：
- 检测 posture 状态，动态调整布局与交互。

**参考资料**：
[Git Repo](https://github.com/foldable-devices) | [Tracking bug #40124716](https://issues.chromium.org/issues/40124716) | [ChromeStatus.com entry](https://chromestatus.com/feature/5185813744975872) | [Spec](https://www.w3.org/TR/device-posture)

---

### Saved queries in `sharedStorage.selectURL`

**影响级别**：🟢 可选

**变更内容**：
sharedStorage.selectURL() 支持保存查询，单页多次复用不再重复计入预算。

**重要性**：
提升 sharedStorage 查询效率，优化预算管理。

**实施指南**：
- 利用 savedQuery 参数优化多次查询场景。

**参考资料**：
[Tracking bug #367440966](https://issues.chromium.org/issues/367440966) | [ChromeStatus.com entry](https://chromestatus.com/feature/5098690386329600) | [Spec](https://github.com/WICG/shared-storage/pull/188)

---

### Private State Token API Permissions Policy default allowlist wildcard

**影响级别**：🟡 重要

**变更内容**：
Private State Token API 权限策略默认 allowlist 从 self 改为 *（通配符）。

**重要性**：
影响第三方嵌入场景的权限控制，需关注安全策略。

**实施指南**：
- 审查相关权限策略配置，确保安全合规。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/5205548434456576) | [Spec](https://github.com/WICG/trust-token-api/pull/306)

---

### FedCM Mode API and Use Other Account API

**影响级别**：🟡 重要

**变更内容**：
FedCM 新增 active mode（需用户手势，UI 更显著）和 Use Other Account 支持。

**重要性**：
提升身份认证流程灵活性与用户体验。

**实施指南**：
- 按需采用 active mode，优化登录交互。
- 支持多账号登录场景。

**参考资料**：
[Demo](https://fedcm-button.glitch.me/) | [Tracking bug #370694829](https://issues.chromium.org/issues/370694829) | [ChromeStatus.com entry](https://chromestatus.com/feature/4689551782313984) | [Spec](https://github.com/w3c-fedid/FedCM/pull/660)

---

### File System Access for Android and WebView

**影响级别**：🟡 重要

**变更内容**：
File System Access API 扩展至 Android 和 WebView，支持文件/目录读写、持久化句柄。

**重要性**：
极大提升移动端 Web 应用与本地文件系统的集成能力。

**实施指南**：
- 在 Android/WebView 环境下启用文件访问相关功能。
- 注意权限申请与用户授权。

**参考资料**：
[Tracking bug #40091667](https://issues.chromium.org/issues/40091667) | [ChromeStatus.com entry](https://chromestatus.com/feature/6284708426022912) | [Spec](https://wicg.github.io/file-system-access)

---

### WebAuthn Signal API

**影响级别**：🟡 重要

**变更内容**：
WebAuthn Signal API 支持向凭据存储提供者反馈凭据状态，便于同步撤销/更新。

**重要性**：
提升 passkey 等凭据管理一致性与安全性。

**实施指南**：
- 集成 Signal API，及时同步凭据状态。

**参考资料**：
[Demo](https://signal-api-demo.glitch.me/) | [Tracking bug #361751877](https://issues.chromium.org/issues/361751877) | [ChromeStatus.com entry](https://chromestatus.com/feature/5101778518147072) | [Spec](https://pr-preview.s3.amazonaws.com/nsatragno/webauthn/pull/2093.html#sctn-signal-methods)

---

### WebGPU: 32-bit float textures blending

**影响级别**：🟡 重要

**变更内容**：
WebGPU 支持 float32-blendable，r32float/rg32float/rgba32float 纹理可混合。

**重要性**：
提升高精度图形渲染能力，适用于科学可视化等场景。

**实施指南**：
- 在需要高精度混合的场景下启用该特性。

**参考资料**：
[Tracking bug #369649348](https://issues.chromium.org/issues/369649348) | [ChromeStatus.com entry](https://chromestatus.com/feature/5173655901044736) | [Spec](https://www.w3.org/TR/webgpu/#float32-blendable)

---

### WebGPU: Expose `GPUAdapterInfo` from `GPUDevice`

**影响级别**：🟢 可选

**变更内容**：
GPUDevice.adapterInfo 属性暴露 GPUAdapterInfo，便于获取设备信息。

**重要性**：
便于调试和设备适配。

**实施指南**：
- 按需获取 GPU 设备信息，优化渲染策略。

**参考资料**：
[Tracking bug #376600838](https://issues.chromium.org/issues/376600838) | [ChromeStatus.com entry](https://chromestatus.com/feature/6221851301511168) | [Spec](https://www.w3.org/TR/webgpu/#dom-gpudevice-adapterinfo)

---

### WebGPU: Texture view usage

**影响级别**：🟡 重要

**变更内容**：
WebGPU 纹理视图创建时可指定 usage 子集，提升兼容性与性能。

**重要性**：
优化底层资源分配，提升性能。

**实施指南**：
- 创建纹理视图时合理指定 usage，避免不兼容用法。

**参考资料**：
[Tracking bug #363903526](https://issues.chromium.org/issues/363903526) | [ChromeStatus.com entry](https://chromestatus.com/feature/5155252832305152) | [Spec](https://github.com/gpuweb/gpuweb/commit/b39d86d356eb759d7564bc7c808ca62fce8bbf3e)

---

### Detailed WebGPU Updates

**影响级别**：🟢 可选

**变更内容**：
WebGPU 132 版本详细更新，涵盖多项新特性与优化。

**重要性**：
便于开发者全面了解 WebGPU 进展。

**实施指南**：
- 参考官方博客，跟进 WebGPU 相关最佳实践。

**参考资料**：
[Chrome for Developers](https://developer.chrome.com/) | [Blog](https://developer.chrome.com/blog)

---

### Explicit compile hints with magic comments

**影响级别**：🟢 可选

**变更内容**：
支持通过 magic comments 指定 JS 文件中需提前编译的函数。

**重要性**：
有助于性能优化，提升关键路径 JS 加载速度。

**实施指南**：
- 在性能敏感代码中添加 magic comments，配合 Origin Trial 测试效果。

**参考资料**：
[Explainer](https://explainers-by-googlers.github.io/explicit-javascript-compile-hints-file-based) | [Tracking bug #42203853](https://issues.chromium.org/issues/42203853) | [ChromeStatus.com entry](https://chromestatus.com/feature/5100466238652416)

---

### `Document-Isolation-Policy`

**影响级别**：🟡 重要

**变更内容**：
Document-Isolation-Policy 支持无需 COOP/COEP 即启用 crossOriginIsolation，提升隔离级别。

**重要性**：
便于渐进式部署隔离策略，提升安全性。

**实施指南**：
- 通过 Origin Trial 测试，评估对现有架构的影响。

**参考资料**：
[Tracking bug #333029146](https://issues.chromium.org/issues/333029146) | [ChromeStatus.com entry](https://chromestatus.com/feature/5141940204208128) | [Spec](https://wicg.github.io/document-isolation-policy)

---

### `navigator.storage` no longer an `EventTarget`

**影响级别**：🔴 关键

**变更内容**：
navigator.storage 不再继承 EventTarget，移除未标准化的 Storage Pressure Event 支持。

**重要性**：
影响依赖相关事件监听的代码，需及时迁移。

**实施指南**：
- 移除对 navigator.storage 事件监听的依赖，采用其他存储压力检测方案。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/5132158480678912) | [Spec](https://storage.spec.whatwg.org/)

---

### Remove prefixed `HTMLVideoElement` fullscreen APIs

**影响级别**：🔴 关键

**变更内容**：
移除 HTMLVideoElement 的 webkit 前缀全屏 API，统一使用标准 Element.requestFullscreen()。

**重要性**：
影响依赖旧前缀 API 的代码，需全面迁移。

**实施指南**：
- 全面替换 webkit*Fullscreen 相关 API 为标准 API。
- 检查兼容性，移除冗余代码。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/5111638103687168)

---
```
