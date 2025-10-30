---
layout: default
title: graphics-webgpu-zh
---

## 领域摘要

Chrome 142 继续扩展 WebGPU 和图形平台能力，重点是更丰富的着色器输入（primitive index）、更广的纹理格式支持（tier1/tier2）以及运行时/库改进（Dawn）。对开发者影响最大的更改是为逐原语着色引入的 WGSL 内建 `primitive_index` 和扩展的纹理格式，这些改进降低了将现有 GPU 资源移植到 WebGPU 的摩擦。总体来看，这些更新通过缩小与原生图形 API 的差距、提高视觉保真度与兼容性，以及简化跨平台 GPU 开发，推动了 Web 平台的发展。这些更新重要，因为它们减少了高级渲染的变通做法，使 WebGPU 成为 Web 上高性能图形与计算的更可行目标。

## 详细更新

下面条目扩展了上文摘要，列出 Chrome 142 中与图形和 WebGPU 相关的每个功能，并提供简明的技术说明、开发者适用场景和参考资料。

### WebGPU: `primitive_index` feature

#### 新增内容
WebGPU 添加了一个可选能力，在片段着色器中暴露 WGSL 内建 `primitive_index`，提供类似于 `vertex_index` 和 `instance_index` 的逐原语索引。

#### 技术细节
该能力为可选项并在受支持的硬件上启用；`primitive_index` 按原语（点/线/三角形）递增，并可在片段阶段着色器中使用。

#### 适用场景
逐原语拾取、每原语的程序化图案，以及需要逐原语身份以进行调试/可视化的技术。

#### 参考资料
- [跟踪错误 #342172182](https://issues.chromium.org/issues/342172182)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6467722716250112)
- [规范](https://gpuweb.github.io/gpuweb/#dom-gpufeaturename-primitive-index)

### WebGPU: Texture formats tier1 and tier2

#### 新增内容
Chrome 142 通过纹理格式分级模型扩展了 GPU 纹理格式支持，使更多格式支持如渲染附件、混合、多重采样、解析和 storage_binding 等功能。

#### 技术细节
分级纹理格式能力由 WebGPU 规范定义；tier1/tier2 为额外格式暴露更多能力，以提高与原生 API 的一致性。

#### 适用场景
将依赖更高级纹理格式与操作的现有资源和引擎移植到 WebGPU，而无需重写着色器或纹理管线。

#### 参考资料
- [跟踪错误 #445725447](https://issues.chromium.org/issues/445725447)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5116926821007360)
- [规范](https://www.w3.org/TR/webgpu/#texture-formats-tier1)

### Texture format support capabilities extended

#### 新增内容
`texture-formats-tier1` 和 `texture-formats-tier2` 功能允许 WebGPU 支持更多纹理格式（例如 16 位通道）和能力，从而更容易移植现有内容。

#### 技术细节
这些 GPU 功能按 GPUWeb 规范暴露诸如 `r16unorm`、`r16snorm`、`rg16unorm`、`rg16snorm` 以及带有渲染与存储操作支持的更高精度 RGBA 变体等格式。

#### 适用场景
依赖半精度格式或特定渲染/解析行为的游戏引擎、图像处理与视觉特效管线现在可以更少修改地迁移到 WebGPU。

#### 参考资料
- ["texture-formats-tier1"](https://gpuweb.github.io/gpuweb/#texture-formats-tier1)
- ["texture-formats-tier2"](https://gpuweb.github.io/gpuweb/#texture-formats-tier2)
- [chromestatus entry](https://chromestatus.com/feature/5116926821007360)

### Primitive index in WGSL

#### 新增内容
WGSL 内建 `primitive_index` 唯一标识片段着色器所处理的原语；从 0 开始并按原语递增。

#### 技术细节
在 WGSL 内建值中定义，`primitive_index` 在每个片段中提供，与需要在着色中使用逐原语元数据的应用兼容。

#### 适用场景
逐原语拾取、自定义光栅化效果或在顶点/实例索引不足以区分对象时的基于着色器的对象识别。

#### 参考资料
- [`primitive_index`](https://gpuweb.github.io/gpuweb/wgsl/#built-in-values-primitive_index)
- [Primitive Picking sample](https://webgpu.github.io/webgpu-samples/?sample=primitivePicking)
- [chromestatus entry](https://chromestatus.com/feature/6467722716250112)

### Dawn updates

#### 新增内容
Dawn 的构建与运行时更新：`DAWN_BUILD_MONOLITHIC_LIBRARY` 的默认值改为 `STATIC`，并改进了 PresentMode 的处理等提交。

#### 技术细节
CMake 默认更改为默认生成 `libwebgpu*` 文件；运行时现在正确处理 `wgpu::PresentMode::Undefined` 的默认值。

#### 适用场景
Dawn 的项目构建系统与下游嵌入者应审查该默认值更改并相应调整 CMake 或链接预期。

#### 参考资料
- [issue 441410668](https://issues.chromium.org/issues/441410668)
- [list of commits](https://dawn.googlesource.com/dawn/+log/chromium/7390..chromium/7444?n=1000)

### FedCM—Support showing third-party iframe origins in the UI

#### 新增内容
当 iframe 实际为第三方时，FedCM UI 现在可以在界面中显示第三方 iframe 的来源，以提高透明度。

#### 技术细节
之前 FedCM UI 始终显示顶级站点；此更改根据更新的用户体验决策在适当情况下显示 iframe 来源。

#### 适用场景
嵌入在第三方 iframe 中的身份认证和联合身份流程将向用户呈现更清晰的来源信息，利于安全性和开发者体验。

#### 参考资料
- [跟踪错误 #390581529](https://issues.chromium.org/issues/390581529)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5176474637959168)
- [规范](https://github.com/w3c-fedid/FedCM/pull/774)

### Stricter `*+json` MIME token validation for JSON modules

#### 新增内容
Chrome 142 在与 `*+json` 匹配时，拒绝其 MIME 类型的 type 或 subtype 中包含非 HTTP token 代码点的 JSON 模块脚本响应，使之与 MIME Sniffing 规范和 Interop2025 保持一致。

#### 技术细节
验证遵循 MIME Sniffing 规范的解析规则，并收紧了对 `*+json` 匹配的接受标准。

#### 适用场景
提供 JSON 模块的开发者应确保 MIME 类型为良构的 token（无空格或无效字符），以避免模块加载失败。

#### 参考资料
- [跟踪错误 #440128360](https://issues.chromium.org/issues/440128360)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5182756304846848)
- [规范](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

### Web Speech API contextual biasing

#### 新增内容
站点可以提供并更新短语列表，以便在 Web Speech API 的识别模型中对指定短语进行偏好。

#### 技术细节
该 API 暴露识别短语列表并允许更新，按规范影响语音识别模型的偏好设置。

#### 适用场景
在特定领域的应用（语音 UI、专业词汇的听写）中，通过偏向预期短语来提高识别准确率。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5225615177023488)
- [规范](https://webaudio.github.io/web-speech-api/#speechreco-phraselist)

### Media session: add reason to `enterpictureinpicture` action details

#### 新增内容
在 `MediaSessionActionDetails` 中添加了 `enterPictureInPictureReason`，使开发者能够区分用户发起与程序化的 PiP 进入。

#### 技术细节
Media Session API 中 `enterpictureinpicture` 的 action details 现在包含一个 reason 字段，按链接的 PR 所述。

#### 适用场景
基于 PiP 是由用户操作还是脚本触发来调整 UI 行为（分析、同意流程或 UX 调整）。

#### 参考资料
- [跟踪错误 #446738067](https://issues.chromium.org/issues/446738067)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6415506970116096)
- [规范](https://github.com/w3c/mediasession/pull/362)

### Local network access restrictions

#### 新增内容
Chrome 142 将对本地网络地址的请求置于权限提示之后，以限制跨源对本地 IP 和回环地址的访问。

#### 技术细节
来自公共网站到本地 IP/回环，或来自本地站点到回环的请求，将根据 WICG 的 local-network-access 提案触发权限提示。

#### 适用场景
提高与局域网设备交互的 Web 应用的安全性；LAN 管理工具的开发者必须处理权限提示与失败模式。

#### 参考资料
- [跟踪错误 #394009026](https://issues.chromium.org/issues/394009026)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5152728072060928)
- [规范](https://wicg.github.io/local-network-access)

### Interoperable pointerrawupdate events exposed only in secure contexts

#### 新增内容
`pointerrawupdate` 事件及全局监听器限定在安全上下文中，以符合 PointerEvents 规范和其他浏览器的行为。

#### 技术细节
Chrome 现在在不安全的上下文中隐藏事件触发和全局监听器的可用性，使行为与 2020 年的规范一致。

#### 适用场景
依赖原始指针更新的开发者应确保页面在安全上下文中提供；这改善了低级指针输入的跨浏览器互操作性。

#### 参考资料
- [跟踪错误 #404479704](https://issues.chromium.org/issues/404479704)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5151468306956288)
- [规范](https://w3c.github.io/pointerevents/#the-pointerrawupdate-event)

### Sticky user activation across same-origin renderer-initiated navigations

#### 新增内容
在导航到另一个同源页面时保留粘性用户激活状态，从而支持在导航间依赖用户激活的行为。

#### 技术细节
根据链接的规范更改，对于同源由渲染器发起的导航会保留粘性激活状态。

#### 适用场景
对在内部导航并需要保留用户激活的单一源应用很有用（例如触发虚拟键盘的自动聚焦输入）。

#### 参考资料
- [跟踪错误 #433729626](https://issues.chromium.org/issues/433729626)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5078337520926720)
- [规范](https://github.com/whatwg/html/pull/11454)

### Device Bound Session Credentials

#### 新增内容
引入一种机制，使服务器能够将会话绑定到单一设备，并通过涉及私钥的周期性由浏览器续期的证明实现绑定。

#### 技术细节
浏览器执行带有私钥持有证明的周期性续期；该功能有 Origin Trial 并遵循 WebAppSec DBSC 规范。

#### 适用场景
通过使被盗会话令牌在其他设备上更难使用，增强敏感应用的会话安全性；适用于银行和企业应用。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials#/view_trial/3357996472158126081)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5140168270413824)
- [规范](https://w3c.github.io/webappsec-dbsc)
- [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies](https://developers.google.com/site-policies)

已保存的文件：digest_markdown/webplatform/Graphics and WebGPU/chrome-142-stable-en.md
