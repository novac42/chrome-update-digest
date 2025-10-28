领域摘要

Chrome 136 (stable) 在“other”类别引入了一项面向用户的改进：在 WebGPU 画布的上下文菜单中直接提供保存或复制渲染图像的操作。这个小但实用的更改使开发者和用户无需对页面进行插装或使用外部工具，就能更方便地捕获 GPU 渲染的输出。它通过使 WebGPU 画布与现有画布 UX（右键 Save/Copy）保持一致，推动了 Web 平台的发展，减少了调试、资源捕获和内容工作流的摩擦。这些更新很重要，因为它们简化了开发者迭代和面向用户的 GPU 驱动网页图形的内容导出。

## 详细更新

以下是上述更改的详细说明及其对开发工作流的影响。

### Save and copy canvas images (保存与复制画布图像)

#### 新增内容
Chrome 用户现在可以在 WebGPU 画布上右键单击，并在上下文菜单中访问选项 "Save Image As…" 或 "Copy Image"。

#### 技术细节
此功能将浏览器上下文菜单中的保存/复制图像操作暴露给由 WebGPU 渲染支持的画布。此更改在下文引用的 Chromium issue 中进行跟踪。

#### 适用场景
- 快速捕获 WebGPU 渲染的帧以用于调试或视觉回归检查。
- 设计师和测试人员在无需添加页面级图像导出代码的情况下导出渲染结果的便利性。
- 在开发评审期间简化共享 GPU 生成的视觉快照。

与领域特定关注点的相关性：
- graphics-webgpu: 通过简化画布输出的捕获，直接有利于围绕 GPU 渲染的工作流。
- webapi: 改善了使用 WebGPU 的画布元素的最终用户体验，而无需修改 API。
- performance & debugging: 低成本的捕获有助于性能分析和视觉调试工作流。
- multimedia & developer tooling: 便于为文档和测试提取资源。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/40902474)

已保存到： digest_markdown/webplatform/other/chrome-136-stable-en.md