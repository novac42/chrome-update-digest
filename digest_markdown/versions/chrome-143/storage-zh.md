---
layout: default
title: storage-zh
---

## 领域摘要

Chrome 143（stable）移除了在 WebGPU 中将 "bgra8unorm" 格式用于只读存储纹理的支持。此更改通过取消先前作为浏览器错误的允许项，使 Chrome 与 WebGPU 规范保持一致。对于开发者，最主要的影响是依赖该格式作为只读存储纹理的着色器和绑定布局需要更新为使用其他格式或使用模式。本次更新提高了 WebGPU 的跨浏览器一致性，并减少了令人惊讶的平台特定行为。

## 详细更新

下面的条目扩展了摘要，并解释了对开发者的影响和缓解措施。

### Remove bgra8unorm read-only storage texture usage（移除 bgra8unorm 只读存储纹理用法）

#### 新增内容
Chrome 不再允许在 WebGPU 中将 "bgra8unorm" 纹理格式用于只读存储纹理。先前 Chrome 中允许该用法的行为是一个错误，现已移除。

#### 技术细节
WebGPU 规范明确禁止将 "bgra8unorm" 用于只读存储纹理，Chrome 的实现已修改以符合该规范。对于尝试此组合的 pipeline 或 bind-group 设置，预计会出现错误或验证失败；请更新纹理格式或使用方式以符合规范。

#### 适用场景
- 图形/WebGPU：更新假定对 bgra8unorm 纹理具有只读存储访问的着色器和 bind group 布局。  
- WebAPI & JavaScript：调整应用和库中的资源创建与验证逻辑，避免创建被禁止的纹理使用方式。  
- 性能与可移植性：与规范保持一致可防止平台特定的回退，并确保可预测的跨浏览器行为。

#### 参考资料
- [跟踪错误 427681156](https://issues.chromium.org/issues/427681156)

文件已保存到：digest_markdown/webplatform/storage/chrome-143-stable-en.md