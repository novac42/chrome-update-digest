## 领域摘要

Chrome 139 的 Web API 更新侧重于标准化、跨源应用边界、可预测的功能检测和更清晰的遥测路由。主要更改允许 Web 应用跨来源扩展范围，使 JSON MIME 检测完全符合 WHATWG 规范，向 WebGPU 适配器/设备标注满足核心规范特性和限制，并允许将仅崩溃报告发送到专用端点。这些进展提升了互操作性、开发者可预测性以及平台集成功能的运营清晰度。开发者应根据这些更改评估清单、内容类型处理、GPU 能力假设和崩溃报告配置。

## 详细更新

以下条目扩展了上面的摘要，说明了发生了什么、如何工作、实际开发者使用场景，以及跟踪/规范资源链接。

### Web app scope extensions (Web 应用范围扩展)

#### 新增内容
新增了一个 `scope_extensions` web app manifest 字段，允许 Web 应用将其范围扩展到其他来源，使控制多个子域和顶级域的网站可以作为单个 Web 应用呈现。列出的来源必须使用 `.well-known` 关联来确认与该 Web 应用的关联。

#### 技术细节
这是一个清单级别的扩展，要求通过所述的关联机制进行来源验证。实现和跟踪通过 Chromium 跟踪 bug 与规范 PR 协调。

#### 适用场景
将多来源属性（子域、相关顶级域）统一为单一 PWA 安装/启动体验；简化相关来源间的导航、共享和 service worker 预期行为。

#### 参考资料
- [跟踪问题 #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5746537956114432)
- [规范](https://github.com/WICG/manifest-incubations/pull/113)

### Specification-compliant JSON MIME type detection (符合规范的 JSON MIME 类型检测)

#### 新增内容
Chrome 现在根据 WHATWG mimesniff 规范识别所有有效的 JSON MIME 类型，包括任何以 `+json` 结尾的子类型，除了 `application/json` 和 `text/json` 外。这使得 JSON 检测与规范一致。

#### 技术细节
MIME 类型识别逻辑已更新为遵循 WHATWG mimesniff 的 JSON 规则。这会影响任何基于检测到的 JSON 内容类型而分支行为的功能或 API 路径。

#### 适用场景
依赖 content-type 检查的 API 和客户端代码在服务器使用 `+json` 厂商或厂商树子类型时，将会看到更一致的 JSON 解析/处理；在与使用自定义 JSON 类 MIME 类型的 API 互操作时可减少意外情况。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5470594816278528)
- [规范](https://mimesniff.spec.whatwg.org/#json-mime-type)

### WebGPU `core-features-and-limits` (WebGPU 核心特性与限制)

#### 新增内容
引入了 `core-features-and-limits` 功能标志/状态，用以表示某个 WebGPU 适配器和设备支持 GPUWeb 规范定义的核心特性和限制。

#### 技术细节
声明支持该功能的适配器/设备满足规范的基线特性和限制。跟踪和规范对齐记录在所引用的跟踪 bug 与规范部分中。

#### 适用场景
图形和计算应用可以查询并依赖已定义良好的 WebGPU 能力基线，从而在高性能渲染和 GPU 计算场景中简化能力协商和回退策略。

#### 参考资料
- [跟踪问题 #418025721](https://issues.chromium.org/issues/418025721)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4744775089258496)
- [规范](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports (崩溃报告 API：指定 `crash-reporting` 以仅接收崩溃报告)

#### 新增内容
开发者可以指定名为 `crash-reporting` 的端点，使得只有崩溃报告会被发送到该端点。默认情况下，`default` 端点会接收多种报告类型；此功能将崩溃投递与其他报告分离。

#### 技术细节
crash-reporting 端点通过 Crash Reporting API 中的 well-known 端点名称进行配置。这允许使用不同的 URL 专门用于崩溃报告，区别于更广泛的报告投递端点。

#### 适用场景
希望将仅崩溃的遥测发送到专门摄取管道（用于存储、告警或隐私隔离）的团队可以配置 `crash-reporting` 端点，以避免其他报告类型的噪声并减少下游过滤工作量。

#### 参考资料
- [跟踪问题 #414723480](https://issues.chromium.org/issues/414723480)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5129218731802624)
- [规范](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)
