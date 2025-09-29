---
layout: default
title: Chrome 140 Stable - Devices Updates
---

# Chrome 140 Stable - Devices Updates

## Area Summary

Chrome 140 带来了重要的 WebGPU 规范合规性更新，这将影响使用 GPU 加速的开发者的设备管理工作流程。关键变更涉及实现正确的适配器消费语义，即 WebGPU 适配器在成功的设备请求后会被正确标记为"已消费"。此更新确保 Chrome 的 WebGPU 实现与官方规范保持一致，为依赖 GPU 设备管理的应用程序提供更可预测的行为。虽然这是一个单一的重点变更，但它代表了朝向完整 WebGPU 规范合规性迈出的关键步骤，并将帮助开发者构建更健壮的图形应用程序。

## Detailed Updates

本次发布专注于一项关键的 WebGPU 规范对齐更新，影响开发者在应用程序中处理 GPU 设备请求的方式。

### Device requests consume adapter

#### What's New
WebGPU 适配器现在会在成功的设备请求后被正确标记为"已消费"，使 Chrome 的实现与官方 WebGPU 规范保持一致。这意味着在同一适配器上的后续 `requestDevice()` 调用将被拒绝并返回 promise 拒绝。

#### Technical Details
根据 WebGPU 规范，当适配器通过 `requestDevice()` 成功创建设备时，该适配器会转换为"已消费"状态。这防止了来自同一适配器实例的多个设备请求，确保了适当的资源管理并防止 GPU 设备分配中的潜在冲突。

#### Use Cases
此变更对于构建 WebGPU 应用程序的开发者特别重要，他们需要：
- 为设备请求失败实现适当的错误处理
- 在复杂图形应用程序中管理多个 GPU 适配器
- 确保在不同浏览器实现中使用 GPU 资源时的可预测行为
- 构建符合规范的健壮 WebGPU 应用程序

#### References
- [WebGPU specification](https://gpuweb.github.io/gpuweb/#ref-for-dom-adapter-state-consumed%E2%91%A1)
- [issue 415825174](https://issues.chromium.org/issues/415825174)
