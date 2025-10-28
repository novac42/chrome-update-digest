---
layout: default
title: chrome-139-zh
---

## 领域摘要

Chrome 139 (stable) 在设备领域为 WebXR 深度感知引入了有针对性的性能改进。该版本公开了若干机制，允许开发者自定义深度缓冲行为（尤其是请求原始或平滑深度缓冲的能力），以降低生成或使用深度的成本。这些更改使 XR 和设备相关团队能够在延迟与质量之间进行更细粒度的权衡，并在受限硬件上实现更高效的渲染和传感器管线。对开发者而言，这通过公开更底层的深度选项，直接转化为更好的运行时性能和在设备上更可预测的资源使用。

## 详细更新

The following update expands on the summary above and highlights practical implications for device- and XR-focused development teams.

### WebXR depth sensing performance improvements（WebXR 深度感知性能改进）

#### 新增内容
公开了若干新机制，用于在 WebXR 会话中自定义深度感知功能的行为，目标是提高深度缓冲生成或使用的性能。关键机制包括能够请求原始或平滑的深度缓冲。

#### 技术细节
该功能提供选项，用于改变生成或传递给 WebXR 会话使用方的深度数据形式（raw vs. smoothed）。这些选项允许实现者和 Web 应用在处理（平滑、过滤）与更低延迟、更低开销的深度数据消耗之间进行权衡。有关权威的 API 形式和状态，请参阅规范和跟踪链接。

#### 适用场景
- 需要更低延迟深度用于遮挡或交互的 AR/VR 应用可以请求原始深度，以减少预处理成本。  
- 需要视觉稳定深度以实现效果的应用可以选择平滑深度，在质量比最小延迟更重要的情况下使用。  
- 设备团队和引擎集成者可以调优深度生成以匹配受限设备上的 GPU/CPU 预算，从而提升帧率和能耗表现。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/410607163)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864)
- [Link](https://immersive-web.github.io/depth-sensing)

已保存文件：digest_markdown/webplatform/Devices/chrome-139-stable-en.md
