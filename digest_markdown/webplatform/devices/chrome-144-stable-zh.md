# Chrome 144 Devices 更新

## 领域摘要

Chrome 144 为 WebXR 生态系统带来了重要的性能增强，引入了 XRVisibilityMaskChange 事件。此更新解决了虚拟和增强现实体验中的关键优化挑战，为开发者提供精确的视口可见性信息。通过使应用程序能够将渲染限制在用户视口的可见部分，该功能可以大幅降低 GPU 工作负载并提高沉浸式体验的帧率。此添加通过实用的性能工具扩展了核心 WebXR 规范，使开发者和体验 VR/AR 内容的最终用户均受益。

## 详细更新

本次发布专注于单个但影响深远的增强功能，通过可见性遮罩为 WebXR 开发者提供更好的渲染性能控制。

### XRVisibilityMaskChange

#### 新增内容

Chrome 144 引入了 `XRVisibilityMaskChange` 事件，这是一个新的 WebXR API，将用户视口的可见部分作为网格表示公开。该事件为开发者提供顶点和索引数据，精确定义视口中用户实际可见的区域，并考虑 VR/AR 头戴设备的光学特性。

#### 技术细节

`XRVisibilityMaskChange` 事件提供两个关键数据：顶点列表和索引列表，它们共同表示可见视口区域的网格几何形状。为了支持遮罩和视图之间的正确配对，`XRView` 对象已增强了唯一标识符，使将每个可见性遮罩与其对应视图关联变得简单明了。此实现通过标准 API 中以前不可用的功能扩展了核心 WebXR 规范。

#### 适用场景

该功能的主要应用是优化 WebXR 体验的性能。通过准确了解视口的哪些部分可见，开发者可以实现视锥体剔除或基于模板的渲染技术，跳过绘制可见区域之外的像素。这对于 GPU 性能至关重要的复杂 VR/AR 场景尤其有价值，因为它可以显著减少片段着色器工作负载并提高帧率。该功能对于高保真应用程序特别有益，例如建筑可视化、培训模拟和沉浸式游戏体验，在这些应用中保持一致的帧率对用户舒适度至关重要。

#### 参考资料

- [跟踪错误 #450538226](https://issues.chromium.org/issues/450538226)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5073760055066624)
- [规范](https://immersive-web.github.io/webxr/#xrvisibilitymaskchangeevent-interface)
