# Chrome 136 稳定版 - Origin Trial 分析

## 区域摘要

Chrome 136 引入了三项重要的 origin trial，在设备交互、性能监控和图形渲染方面推进了关键的 Web 平台能力。Audio Output Devices API 通过允许顶级框架为子框架管理默认音频输出来扩展多媒体控制，而新的性能时序 API 帮助开发者理解和优化影响用户体验的双峰性能分布。此外，Canvas 文本渲染实现的重大更新为图形密集型应用程序提供了潜在的性能改进，展现了 Chrome 在扩展 Web API 和优化现有功能方面的承诺。

## 详细更新

这些 origin trial 体现了 Chrome 在完全标准化之前测试新功能和实现改进的方法，允许开发者试验前沿能力，同时提供反馈来塑造 Web 平台的未来。

### Audio Output Devices API: setDefaultSinkId()

**新增功能**：
此功能向 `MediaDevices` 引入了 `setDefaultSinkId()` 方法，使顶级框架能够程序化地更改其子框架使用的默认音频输出设备。

**技术细节**：
该 API 通过新方法扩展了现有的 MediaDevices 接口，允许父框架控制嵌入内容的音频路由。这实现了跨 iframe 边界的集中式音频设备管理，为复杂 Web 应用程序中的音频输出控制提供了统一方法。

**使用场景**：
带有嵌入式媒体播放器的 Web 应用程序现在可以为用户提供适用于所有内容的单一音频设备选择。这对于仪表板应用程序、具有多个媒体源的教育平台以及需要在各种嵌入组件之间保持一致音频路由的企业应用程序特别有价值。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [ChromeStatus.com entry](https://chromestatus.com/feature/5066644096548864) | [Spec](https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid)

### Enable web applications to understand bimodal performance timings

**新增功能**：
此 origin trial 引入了新的性能时序能力，帮助 Web 应用程序识别和理解由应用程序直接控制范围外的因素导致的页面加载性能双峰分布。

**技术细节**：
该 API 提供增强的时序数据，区分不同的性能场景，例如冷启动与热启动条件。这允许应用程序基于浏览器初始化状态和系统资源可用性来分离性能指标，提供更准确的性能洞察。

**使用场景**：
开发者现在可以实现更智能的性能监控，考虑到不同的系统条件。这通过识别何时性能不佳是由于外部因素而非应用程序问题来实现更好的用户体验优化，从而制定更准确的性能预算和有针对性的优化。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #1413848](https://bugs.chromium.org/p/chromium/issues/detail?id=1413848) | [ChromeStatus.com entry](https://chromestatus.com/feature/5037395062800384) | [Spec](https://w3c.github.io/navigation-timing/)

### Update of Canvas text rendering implementation

**新增功能**：
对 `CanvasRenderingContext2D` 文本渲染实现的重大改进影响了 `measureText()`、`fillText()` 和 `strokeText()` 方法，可能为 canvas 密集型应用程序提高性能。

**技术细节**：
这主要是一个内部实现更改，现代化了 Canvas API 内的文本渲染管线。虽然没有暴露新的面向 Web 的功能，但更新的实现可能显著影响渲染性能和跨不同平台的行为一致性。

**使用场景**：
大量依赖 canvas 文本渲染的应用程序，如数据可视化工具、带有文本覆盖的游戏和交互式图形应用程序，可以从潜在的性能改进中受益。origin trial 允许开发者针对新实现测试其应用程序，以确保兼容性并衡量性能提升。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials/#/trials/active) | [Tracking bug #389726691](https://bugs.chromium.org/p/chromium/issues/detail?id=389726691) | [ChromeStatus.com entry](https://chromestatus.com/feature/5104000067985408)