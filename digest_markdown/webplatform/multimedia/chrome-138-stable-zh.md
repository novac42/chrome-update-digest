## 领域摘要

Chrome 138（stable）在 WebCodecs 中引入了对多媒体帧方向元数据的支持。此更改添加了显式的方向字段，使开发者能够检测并传递来自诸如 Android 相机等来源的旋转和翻转信息。它将帧方向处理在 WebCodecs 管线内标准化，使渲染、编码和处理更加可预测。对开发者而言，此更新减少了对临时变换的需求并简化了捕获设备与基于 Web 的媒体处理之间的互操作性。

## 详细更新

下面的单项 multimedia 更新在 WebCodecs 中实现了方向元数据，并直接支持上述摘要。

### Add support for video frame orientation metadata to WebCodecs（为 WebCodecs 添加视频帧方向元数据支持）

#### 新增内容
向 WebCodecs 中的各类视频相关接口引入了 `rotation: int` 和 `flip: bool` 值，以便开发者能够处理具有方向信息的帧来源（例如 Android 相机、某些媒体）。`VideoFrame` 接口获得了创建带有方向元数据的 VideoFrame 的能力。

#### 技术细节
- 在相关的 WebCodecs 接口中新增了方向元数据字段（`rotation`、`flip`），且 VideoFrame 构造 API 接受方向信息。
- 这些元数据随帧在 WebCodecs 管线中传递，因此下游消费者（编码器、渲染器、处理器）可以应用或保留期望的方向。
- 有关权威接口细节，请参阅 WebCodecs 规范，并参阅 ChromeStatus/跟踪 bug 了解部署状态。

#### 适用场景
- 在硬件提供方向元数据的相机捕获中正确渲染，而无需额外的基于 CPU 的旋转。
- 在基于 Web 的媒体工作流中，在编码/转码期间保留源方向。
- 将带方向的帧输入到渲染管线（Canvas、WebGL/WebGPU）或带有显式方向语义的 WebRTC。
- 通过避免手动元数据 hack 简化媒体编辑和播放器逻辑。

#### 参考资料
- [Tracking bug](https://bugs.chromium.org/p/chromium/issues/detail?id=40243431)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5098495055380480)
- [Link](https://w3c.github.io/webcodecs/#videoframe-interface)

Developer implications by domain (concise):
- webapi: New WebCodecs fields expand the VideoFrame contract; update code that constructs/consumes VideoFrames.
- graphics-webgpu: Texture uploads and shader transforms may use orientation metadata instead of pre-rotating pixels.
- javascript: Surface-level API additions; no language-level changes.
- multimedia: Clarifies codec/processing semantics when source hardware supplies orientation.
- devices: Improves integration with camera hardware that reports frame orientation.
- performance: Potentially reduces CPU work by avoiding software rotation; use metadata-aware pipelines.
- security-privacy: No new permission surface is introduced by orientation metadata.