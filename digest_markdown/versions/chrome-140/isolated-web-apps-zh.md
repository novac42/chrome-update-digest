---
layout: default
title: Chrome 140 Stable - Isolated Web Apps 更新
---

# Chrome 140 Stable - Isolated Web Apps 更新

## Area Summary

Chrome 140 通过新的 Controlled Frame API 为独立 Web 应用 (IWA) 带来重要进展，这代表了安全 Web 应用架构的重大步骤。此功能使 IWA 能够嵌入任何内容，包括传统 `<iframe>` 元素无法处理的第三方资源，同时保持严格的安全边界。Controlled Frame API 通过提供对嵌入内容的精细控制，为 Web 平台带来桌面级应用能力，类似于原生应用框架。此更新强化了 Chrome 通过 IWA 模型实现更强大和安全的 Web 应用的承诺，为开发者创建具有增强隔离和控制机制的复杂 Web 应用提供新的可能性。

## Detailed Updates

在独立 Web 应用基础上，Chrome 140 提供强大的新嵌入能力，扩展了在安全 IWA 环境中的可能性。

### Controlled Frame API (available only to IWAs)

#### What's New
Controlled Frame API 为独立 Web 应用引入了一种嵌入内容的新方式，超越了传统 `<iframe>` 元素的限制。此 API 允许 IWA 嵌入所有类型的内容，包括无法使用标准 Web 技术嵌入的第三方资源，同时提供对嵌入内容行为和交互的增强控制。

#### Technical Details
Controlled Frame API 专门在独立 Web 应用安全模型内运行，确保强大的嵌入能力仅适用于满足 IWA 严格隔离要求的应用。与标准 `<iframe>` 元素不同，后者受到各种安全限制和跨源策略约束，可能阻止某些第三方内容的嵌入，Controlled Frame 提供了更灵活的嵌入机制。该 API 允许开发者控制嵌入内容执行环境和行为的各个方面，为 IWA 提供类似于其他平台原生应用框架的能力。

#### Use Cases
此功能使开发者能够创建更复杂的 Web 应用，可以集成多样的内容源而不受传统 Web 安全限制约束。潜在应用包括需要嵌入遗留系统的商业应用、集成多个第三方工具的教育平台，或需要各种 Web 服务无缝集成的企业软件。受控环境确保即使嵌入不受信任的第三方内容时，宿主 IWA 也能保持安全性和稳定性。

#### References
- [Isolated Web Apps explainer](https://github.com/WICG/isolated-web-apps/blob/main/README.md)
- [Tracking bug #40191772](https://issues.chromium.org/issues/40191772)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5199572022853632)
- [Spec](https://wicg.github.io/controlled-frame)
