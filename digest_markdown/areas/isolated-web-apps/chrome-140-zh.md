---
layout: default
title: chrome-140-zh
---

## 领域摘要

Chrome 140 稳定版引入了仅面向 Isolated Web Apps (IWAs) 的 Controlled Frame API。主要趋势是扩展 IWAs 嵌入并控制第三方内容的能力，这类内容在传统的 <iframe> 嵌入中会被阻止。此更改对于需要在保持应用级隔离模型的同时集成外部内容的已安装网页应用开发者具有重要意义。它推动了平台发展，为 IWAs 提供了一个官方认可的、更丰富的嵌入场景表面，同时通过 IWA 模型实现集中控制与审查。

## 详细更新

上面的简短摘要概述了本次发布中的具体更改。下面列出 Chrome 140 中为 Isolated Web Apps 添加的单一功能。

### Controlled Frame API (available only to IWAs)（仅适用于 IWAs）

#### 新增内容
添加了一个仅面向 Isolated Web Apps 的 Controlled Frame API。它允许嵌入所有内容，包括无法在标准 <iframe> 中嵌入的第三方内容，并提供对嵌入内容表面的编程式控制。

#### 技术细节
- 该 API 作用域限定于 IWAs（面向隔离应用的安装与打包模型），不适用于常规网页。
- 规范与实现工作通过下列规范和 Chromium 问题跟踪进行记录；请参阅这些链接以获取精确的 API 形态和安全模型。
- 相关链接：
  - 规范: https://wicg.github.io/controlled-frame
  - 跟踪: https://issues.chromium.org/issues/40191772
  - 解释说明: https://github.com/WICG/isolated-web-apps/blob/main/README.md
  - ChromeStatus: https://chromestatus.com/feature/5199572022853632

#### 适用场景
- 在传统嵌入被 `frame-ancestors` 或其他限制阻止时，在 IWA 内嵌入第三方 UI 或内容。
- 构建混合已安装应用，将本地受信任的应用逻辑与远程内容结合，同时保持应用界面在开发者控制之下。
- 在 IWA 打包模型中，开发者需要对嵌入内容的运行时生命周期和集成点进行更细粒度控制的场景。

#### 参考资料
- [GitHub](https://github.com/WICG/isolated-web-apps/blob/main/README.md)
- [Tracking bug](https://issues.chromium.org/issues/40191772)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5199572022853632)
- [Spec](https://wicg.github.io/controlled-frame)

已保存至: digest_markdown/webplatform/Isolated Web Apps/chrome-140-stable-en.md
