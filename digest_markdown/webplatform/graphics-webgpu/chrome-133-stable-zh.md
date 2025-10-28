## 领域摘要

Chrome 133 继续扩展并稳定 WebGPU 的功能面：新增顶点格式（包括 1 分量类型和 unorm8x4-bgra）、为正确性与性能调整的 WGSL 对齐与 discard 相关更改、改进对外部纹理和图像方向的处理，以及设备/限制的人机工程学改进。本次发布还通过弃用、实验性功能清理和 Dawn 实现更新来提升兼容性和 API 卫生。对开发者而言，这意味着更细粒度的顶点输入选项、更少令人惊讶的运行时限制错误、更高保真的外部媒体到纹理传递，以及可测量的着色器性能提升。这些更新共同使高级 GPU 功能对 Web 应用和引擎而言更可预测、更易集成。

## 详细更新

下面的要点基于 Chrome 133 发布数据，扩展了上述摘要，列出各项功能说明。

### Rendering and graphics（渲染与图形）

#### 新增内容
本节汇总了 Chrome WebGPU 的亮点以及本次发布的详细 WebGPU 更新说明。

#### 技术细节
标注为本次发行中 WebGPU 更改的总体说明。

#### 适用场景
为跟踪 WebGPU 与渲染改进的开发者提供切入点。

#### 参考资料
未提供

### WebGPU: 1-component vertex formats (and unorm8x4-bgra)（WebGPU：1 分量顶点格式（和 unorm8x4-bgra））

#### 新增内容
添加了最初 WebGPU 发行时遗漏的额外顶点格式；1 分量顶点格式允许仅请求所需的数据，而不是至少两个分量。

#### 技术细节
解决了早期因平台支持差异（例如旧版 macOS）导致的遗漏。参见跟踪链接以了解进展和状态。

#### 适用场景
当顶点属性为单值（例如标量权重、偏移量）时，可降低内存和带宽开销。

#### 参考资料
- [跟踪 bug #376924407](https://issues.chromium.org/issues/376924407)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4609840973086720)

### Detailed WebGPU Updates（详细的 WebGPU 更新）

#### 新增内容
指向本发布的 Chrome 开发者博客文章和 WebGPU 更改日志的参考指针。

#### 技术细节
资源来源列举 developer.chrome.com 和开发者博客。

#### 适用场景
使用这些资源获取深入的发行说明和示例。

#### 参考资料
- [Chrome for Developers（Chrome 开发者）](https://developer.chrome.com/)
- [Blog（博客）](https://developer.chrome.com/blog)

### Additional unorm8x4-bgra and 1-component vertex formats（额外的 unorm8x4-bgra 与 1 分量顶点格式）

#### 新增内容
添加了 "unorm8x4-bgra" 以及多种 1 分量格式："uint8", "sint8", "unorm8", "snorm8", "uint16", "sint16", "unorm16", "snorm16", 和 "float16"。

#### 技术细节
unorm8x4-bgra 格式简化了对 BGRA 编码数据的加载；列出的 1 分量类型扩展了属性粒度。

#### 适用场景
更好地与 BGRA 源互操作，并在单分量属性足够时提供更紧凑的顶点流。

#### 参考资料
- [chromestatus 条目](https://chromestatus.com/feature/4609840973086720)
- [issue 376924407](https://issues.chromium.org/issues/376924407)

### Allow unknown limits to be requested with undefined value（允许使用 undefined 值请求未知限制）

#### 新增内容
现在可以在请求 GPU 设备时通过指定 `undefined` 来请求未知的 GPU 适配器限制。

#### 技术细节
这使得在规范限制随时间演化且 `adapter.limits.someLimit` 可能缺失时，WebGPU 的设备请求更不易脆弱。

#### 适用场景
在按条件查询适配器限制并希望向前兼容的应用中，能更安全地请求设备。

#### 参考资料
- [spec PR 4781](https://github.com/gpuweb/gpuweb/pull/4781)

### WGSL alignment rules changes（WGSL 对齐规则更改）

#### 新增内容
在结构体成员上使用的 `@align(n)` 现在必须为所有结构体除以 RequiredAlignOf；不再允许太小的对齐值。

#### 技术细节
此项强制简化了 WGSL 用法，并移除某些不正确对齐注释的类别。

#### 适用场景
提高 WGSL 着色器在不同实现间的可移植性与正确性。

#### 参考资料
- [`RequiredAlignOf`](https://gpuweb.github.io/gpuweb/wgsl/#requiredalignof)
- [spec PR](https://github.com/gpuweb/gpuweb/pull/4978)

### WGSL performance gains with discard（WGSL 使用 discard 的性能提升）

#### 新增内容
WGSL 的 discard 语句在可用时使用平台提供的语义降级为 helper invocation，从而解决了在 SSR 中观察到的大幅性能下降问题。

#### 技术细节
采用平台的 discard/demote 语义以避免导致病态性能回退的情况。

#### 适用场景
恢复使用 discard 的着色器在复杂屏幕空间效果中的预期性能。

#### 参考资料
- [discard statement](https://gpuweb.github.io/gpuweb/wgsl/#discard-statement)
- [issue 372714384](https://issues.chromium.org/372714384)

### Use VideoFrame displaySize for external textures（对外部纹理使用 VideoFrame 的 displaySize）

#### 新增内容
在将 VideoFrame 导入为 GPUExternalTexture 时，Chrome 现在使用该帧的 `displayWidth` 和 `displayHeight` 作为表观尺寸。

#### 技术细节
此前使用的是可见尺寸，这在对 GPUExternalTexture 使用 `textureLoad()` 时导致问题。

#### 适用场景
在编码尺寸与显示尺寸不同的外部视频纹理上采样或加载时，提高正确性。

#### 参考资料
- [issue 377574981](https://issues.chromium.org/issues/377574981)

### Handle images with non-default orientations using copyExternalImageToTexture（使用 copyExternalImageToTexture 处理非默认方向的图像）

#### 新增内容
`copyExternalImageToTexture()` 现在能正确处理具有非默认方向的图像（例如 ImageBitmap，使用 `imageOrientation: "from-image"` 的情况）。

#### 技术细节
修复了当源带有方向元数据应用时先前的不正确处理。

#### 适用场景
将带有方向元数据的画布或图像准确复制到 GPU 纹理，无需手动预旋转。

#### 参考资料
- [`\"from-image\"`](https://developer.mozilla.org/docs/Web/API/Window/createImageBitmap#from-image)
- [issue 384858956](https://issues.chromium.org/issues/384858956)

### Improving developer experience（改善开发者体验）

#### 新增内容
围绕适配器限制的错误信息已扩充，包含提示，告知开发者何时必须显式请求更高的限制。

#### 技术细节
目的是减少出现 `adapter.limits` 显示高值但设备请求未包含所需更高限制而失败的意外情况。

#### 适用场景
帮助开发者在遇到运行时限制之前诊断并修正设备请求错误。

#### 参考资料
- [issue 42240683](https://issues.chromium.org/issues/42240683)

### Enable compatibility mode with featureLevel（通过 featureLevel 启用兼容模式）

#### 新增内容
可以通过设置标准化的 `featureLevel` 选项请求实验性的兼容模式适配器。

#### 技术细节
通过标准化的 `featureLevel` 适配器请求选项暴露了兼容性提案。

#### 适用场景
在需要时便于与旧版或非标准 GPU 行为互操作。

#### 参考资料
- [experimental compatibility mode](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md#webgpu-spec-changes)
- [`featureLevel`](https://gpuweb.github.io/gpuweb/#dom-gpurequestadapteroptions-featurelevel)
- [spec PR 4897](https://github.com/gpuweb/gpuweb/pull/4897)
- [webgpureport.org](https://webgpureport.org)

### Experimental subgroup features cleanup（实验性子组功能清理）

#### 新增内容
已移除弃用的实验性子组功能 `"chromium-experimental-subgroups"` 和 `"chromium-experimental-subgroup-uniform-control-flow"`；当前只需使用 `"subgroups"` 功能。

#### 技术细节
清理跟随上游实验整合。

#### 适用场景
简化子组功能的特性标志。

#### 参考资料
- [issue 377868468](https://issues.chromium.org/issues/377868468)
- [issue 380244620](https://issues.chromium.org/issues/380244620)

### Deprecate maxInterStageShaderComponents limit（弃用 maxInterStageShaderComponents 限制）

#### 新增内容
`maxInterStageShaderComponents` 限制因与 `maxInterStageShaderVariables` 冗余且存在少量差异而被弃用。

#### 技术细节
弃用旨在减少 API 面并避免在重叠限制间引起混淆。

#### 适用场景
开发者应在适用时迁移至 `maxInterStageShaderVariables`。

#### 参考资料
- [intent to deprecate](https://groups.google.com/a/chromium.org/g/blink-dev/c/i5oJu9lZPAk)
- [issue 364338810](https://issues.chromium.org/issues/364338810)

### Dawn updates（Dawn 更新）

#### 新增内容
Dawn API 更改：添加了 `wgpu::Device::GetAdapterInfo(adapterInfo)` 并将 `WGPUProgrammableStageDescriptor` 重命名为 `WGPUComputeState`，以及其他提交。

#### 技术细节
实现与 API 调整以保持 Dawn 与规范和使用模式一致。

#### 适用场景
本机引擎作者与绑定维护者应审查这些更改以更新绑定。

#### 参考资料
- [issue 376600838](https://issues.chromium.org/issues/376600838)
- [issue 379059434](https://issues.chromium.org/issues/379059434)
- [issue 383147017](https://issues.chromium.org/issues/383147017)
- [提交列表](https://dawn.googlesource.com/dawn/+log/chromium/6834..chromium/6943?n=1000)

### Opt out of freezing on Energy Saver（在省电模式下选择不冻结）

#### 新增内容
一个原点试验允许站点选择不启用 Chrome 133 中的 Energy Saver 冻结行为。

#### 技术细节
作为站点注册的可选退出试验提供。

#### 适用场景
依赖持续 GPU 工作或媒体播放的站点可以选择退出以避免在省电模式下被冻结。

#### 参考资料
- [跟踪 bug #325954772](https://issues.chromium.org/issues/325954772)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5158599457767424)
- [Spec（规范）](https://wicg.github.io/page-lifecycle)

### Reference Target for Cross-root ARIA（跨根 ARIA 的参考目标）

#### 新增内容
Reference Target 允许 IDREF 属性（例如 `for`, `aria-labelledby`）引用 shadow DOM 内的元素，同时保持封装性。

#### 技术细节
旨在让 ARIA 在不暴露内部 DOM 细节的情况下跨 shadow root 生效。

#### 适用场景
改进使用 shadow DOM 的组件的可访问性。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5188237101891584)

### Deprecate WebGPU limit `maxInterStageShaderComponents`（弃用 WebGPU 限制 `maxInterStageShaderComponents`）

#### 新增内容
重复/弃用注记：`maxInterStageShaderComponents` 已弃用，计划在 Chrome 135 中移除。

#### 技术细节
重申与 `maxInterStageShaderVariables` 的冗余并指出计划移除。

#### 适用场景
在 Chrome 135 之前准备迁移以移除对此限制的依赖。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4853767735083008)

### Remove `<link rel=prefetch>` five-minute rule（移除 `<link rel=prefetch>` 五分钟规则）

#### 新增内容
Chrome 移除了对预取资源的特殊五分钟规则；从首次使用开始适用正常的 HTTP 缓存语义（例如 max-age、no-cache）。

#### 技术细节
预取不再在初始五分钟窗口内覆盖缓存头。

#### 适用场景
开发者应依赖标准缓存语义来理解 prefetch 行为。

#### 参考资料
- [跟踪 bug #40232065](https://issues.chromium.org/issues/40232065)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5087526916718592)

### Remove Chrome Welcome page triggering with initial prefs first run tabs（移除通过初始偏好 first_run_tabs 触发 Chrome 欢迎页）

#### 新增内容
在 `initial_preferences` 的 `first_run_tabs` 中包含 `chrome://welcome` 不再会触发欢迎页。

#### 技术细节
移除此行为，因为在桌面端与现有首次运行体验重复。

#### 适用场景
管理员和 OEM 不应依赖此偏好来触发 Chrome 欢迎页。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5118328941838336)
- [Creative Commons Attribution 4.0 License（知识共享署名 4.0 许可证）](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 License（Apache 2.0 许可证）](https://www.apache.org/licenses/LICENSE-2.0)
- [Google Developers Site Policies（Google 开发者站点政策）](https://developers.google.com/site-policies)