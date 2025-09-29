Area Summary

Chrome 139 的 Graphics 和 WebGPU 更新侧重于更广泛的设备兼容性以及扩展的纹理/压缩功能。主要内容包括引入 WebGPU 兼容模式（可选/origin trial）和将“core-features-and-limits”作为一种能力正式化以简化运行时能力协商。对开发者有影响的更改包括新增对 3D 块压缩纹理（BC/ASTC）的支持、Dawn API 的调整以及用于在旧 GPU 上测试兼容性的工具。这些更新通过降低在旧硬件上运行 GPU 加速应用的门槛，同时保留通向现代 WebGPU 功能的路径，推动了平台发展。

## Detailed Updates

Below are concise, developer-focused summaries of each Graphics and WebGPU feature in Chrome 139.

### 3D texture support for BC and ASTC compressed formats

#### What's New
Adds the "texture-compression-bc-sliced-3d" and "texture-compression-astc-sliced-3d" WebGPU features to allow 3D textures using BC and ASTC block-compressed formats.

#### Technical Details
These are opt-in WebGPU features that enable block-compressed 3D texture formats, reducing memory and bandwidth for volumetric textures and large 3D assets.

#### Use Cases
Volume rendering, medical/scientific visualization, texture atlases for 3D tiles, and any app needing lower GPU memory and bandwidth for 3D textures.

#### References
- https://webgpu.github.io/webgpu-samples/?sample=volumeRenderingTexture3D
- https://chromestatus.com/feature/5080855386783744

### New "core-features-and-limits" feature

#### What's New
Introduces a "core-features-and-limits" feature for upcoming WebGPU compatibility mode to indicate an adapter/device supports the spec's core features and limits.

#### Technical Details
This capability flag signals core spec conformance to simplify feature negotiation; currently "core" is the only WebGPU version, so implementations should advertise this when appropriate.

#### Use Cases
Runtime checks to select code paths that rely on guaranteed core behavior, simplifying fallback logic and reducing per-feature probing.

#### References
- https://gist.github.com/greggman/0dea9995e33393c546a4c2bd2a12e50e
- https://issues.chromium.org/issues/418025721

### Origin trial for WebGPU compatibility mode

#### What's New
An origin trial enables evaluation of WebGPU compatibility mode so WebGPU apps can target older devices lacking modern native APIs (e.g., large fractions of Windows and Android users).

#### Technical Details
Compatibility mode imposes light restrictions to map WebGPU to older graphics APIs; origin trial tokens allow site-level experimentation and telemetry gathering.

#### Use Cases
Broaden device reach for GPU-accelerated web apps, test fallback constraints, and validate behavior (e.g., generate mipmaps) on legacy GPUs.

#### References
- https://developer.mozilla.org/docs/Web/API/GPU/requestAdapter
- https://webgpufundamentals.org/webgpu/lessons/webgpu-compatibility-mode.html
- https://webgpu.github.io/webgpu-samples/?sample=generateMipmap

### Dawn updates

#### What's New
Dawn changes include adding a `message` argument to WGPUQueueWorkDoneCallback for consistency and build/run fixes when emdawnwebgpu is linked with `-sSHARED_MEMORY`.

#### Technical Details
API header update in webgpu-headers and associated Dawn CLs/commits adjust callback signatures and address shared-memory build/runtime behavior.

#### Use Cases
Better parity between native bindings and expected callbacks for consumers of Dawn-based WebGPU, and more robust embedding scenarios when using shared memory builds.

#### References
- https://github.com/webgpu-native/webgpu-headers/pull/528
- https://dawn-review.googlesource.com/c/dawn/+/244075
- https://dawn.googlesource.com/dawn/+log/chromium/7204..chromium/7258?n=1000

### Enable the feature

#### What's New
WebGPU compatibility mode is not enabled by default in Chrome 139 but can be experimented with locally by enabling experimental Web Platform features.

#### Technical Details
Developers can opt into testing the compatibility mode via experimental flags (or origin trial registration) to exercise the constrained WebGPU subset on their sites.

#### Use Cases
Local testing, debugging, and validation of compatibility mode behavior before broader deployment or origin-trial registration.

#### References
- https://chromestatus.com/feature/6436406437871616

### WebGPU `core-features-and-limits`

#### What's New
Clarifies that `core-features-and-limits` designates adapters/devices that meet the spec's core features and limits.

#### Technical Details
This is a formalized capability used in capability reporting and matching; tracking and spec links provide the formal definition and implementation tracking.

#### Use Cases
Simplifies code that needs guaranteed minimum GPU capabilities without enumerating per-feature checks.

#### References
- https://issues.chromium.org/issues/418025721
- https://chromestatus.com/feature/4744775089258496
- https://gpuweb.github.io/gpuweb/#core-features-and-limits

### WebGPU compatibility mode

#### What's New
Adds an opt-in, lightly restricted subset of WebGPU that can run on older backends like OpenGL and Direct3D11 to extend WebGPU reach.

#### Technical Details
Compatibility mode defines constraints and mappings to older APIs; it is exposed via an origin trial and tracked as a Chromium feature with a proposal in the GPUWeb repo.

#### Use Cases
Targeting legacy devices, progressive enhancement strategies, and staged rollouts where modern WebGPU features are unavailable.

#### References
- https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241
- https://issues.chromium.org/issues/40266903
- https://chromestatus.com/feature/6436406437871616
- https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md

要保存的文件: digest_markdown/webplatform/Graphics and WebGPU/chrome-139-stable-en.md