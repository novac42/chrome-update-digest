---
layout: default
title: chrome-138-zh
---

## 详细更新

此版本中的单个多媒体更新直接解决了视频帧方向如何由 Web 应用和低级媒体管线表示与消费的问题。

### Add support for video frame orientation metadata to WebCodecs（为 WebCodecs 添加视频帧方向元数据支持）

#### 新增内容
引入了 `rotation: int` 和 `flip: bool` 值到 WebCodecs 的各类与视频相关的接口，以便开发者可以处理带有方向元数据的帧源。`VideoFrame` 接口已扩展，允许创建带有任意旋转和翻转元数据的 VideoFrame。

#### 技术细节
- 新的元数据字段：`rotation`（整数，度）和 `flip`（布尔）在 WebCodecs 视频接口和 VideoFrame 构造中暴露。
- 这些字段使消费者了解预计的视觉方向，而不需要像素缓冲区本身事先被旋转。
- 这是一个 WebCodecs 级别的更改（参见规范链接），并将与 GPU 上传和合成器路径交互；实现者可以使用该元数据选择面向方向的纹理上传或基于着色器的变换，而不是在 CPU 端重新格式化。

#### 适用场景
- 移动相机应用和基于 Web 的捕获管线：正确解释来自 Android 等设备的 EXIF/相机方向信息。
- 实时视频（会议、流媒体）：避免对每帧进行整帧的 CPU 变换，降低延迟和 CPU 使用。
- 媒体处理管线（编码/解码）：在编码/解码周期中保留方向元数据，并仅在必要时应用变换（渲染 vs 存储）。

#### 领域专家注释
- webapi: WebCodecs API 扩展以包含方向元数据；开发者应检查 VideoFrame 的创建/消费点。
- graphics-webgpu: 方向元数据使得更高效的 GPU 端处理成为可能（纹理坐标变换或着色器旋转），而非 CPU 端重绘。
- javascript: WebCodecs 在 JS 中的集成将为 VideoFrame 暴露额外属性；更新应用逻辑以查询这些字段。
- performance: 减少冗余像素操作，可降低实时应用的端到端延迟。
- multimedia: 通过将像素数据与呈现方向分离，澄清了编码器和容器对方向的处理。
- devices: 有助于规范设备相机在设备本机方向下呈现帧的行为。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40243431
- https://chromestatus.com/feature/5098495055380480
- https://w3c.github.io/webcodecs/#videoframe-interface

此摘要的文件路径：
digest_markdown/webplatform/Multimedia/chrome-138-stable-en.md
