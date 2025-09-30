领域摘要

Chrome 136 的 origin trials 致力于在广泛推出前，为开发者提供针对性且可测试的平台变更访问。本次发行的试验涵盖音频路由（在 `MediaDevices` 上新增 `setDefaultSinkId`）、用于区分冷启动的双模性能计时测量，以及可能影响性能的实验性 Canvas 文本渲染实现。这些试验让开发者在变更广泛落地前验证行为、调整应用并反馈真实世界的影响。

## 详细更新

以下条目总结了 Chrome 136 中正在进行的 origin trials 以及开发者为何应参与测试。

### Audio Output Devices API: setDefaultSinkId()（音频输出设备 API）

#### 新增内容
向 `MediaDevices` 添加 `setDefaultSinkId()`，允许顶层框架更改其子框架使用的默认音频输出设备。

#### 技术细节
此 API 扩展通过 origin trial 暴露，并向 `MediaDevices` 附加一个默认输出设备控制，作用域为顶层框架并应用于子框架。

#### 适用场景
适用于管理嵌入式内容或跨框架音频的 Web 应用（例如会议应用、嵌入式小部件），顶层上下文需要将子框架的音频输出定向到特定设备的场景。

#### 参考资料
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- ChromeStatus.com entry: https://chromestatus.com/feature/5066644096548864
- Spec: https://webaudio.github.io/web-audio-api/#dom-mediadevices-setdefaultsinkid

### Enable web applications to understand bimodal performance timings（帮助 Web 应用理解双模性能计时）

#### 新增内容
一个 origin trial，用于帮助 Web 应用检测并推断页面加载性能中的双模分布（例如区分冷启动与已热身场景）。

#### 技术细节
该试验暴露用于让应用识别页面加载计时何时受到外部因素影响的信号，例如耗时的用户代理初始化（冷启动），并引用导航计时语义。

#### 适用场景
使开发者能更好地诊断并调整在遇到慢冷启动的用户的用户体验，实施有条件的度量，以及更准确地解释由 Navigation Timing 数据驱动的遥测数据。

#### 参考资料
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- Tracking bug #1413848: https://bugs.chromium.org/p/chromium/issues/detail?id=1413848
- ChromeStatus.com entry: https://chromestatus.com/feature/5037395062800384
- Spec: https://w3c.github.io/navigation-timing/

### Update of Canvas text rendering implementation（Canvas 文本渲染实现更新）

#### 新增内容
一个针对 Canvas 文本渲染方法（`measureText()`、`fillText()` 与 `strokeText()`）内部实现重大变更的 origin trial；该变更并非 Web 可见的 API 更改，但可能影响性能。

#### 技术细节
此试验向起源暴露了新的内部 Canvas 文本渲染实现，以便 Canvas 重负载的应用评估更新后的渲染管线在性能和行为上的差异。

#### 适用场景
Canvas 重负载的应用（游戏、编辑器、复杂可视化）可选择加入试验以验证文本测量和文本绘制的性能、检测回归，并在实现广泛发布前提供反馈。

#### 参考资料
- Origin Trial: https://developer.chrome.com/origintrials/#/trials/active
- Tracking bug #389726691: https://bugs.chromium.org/p/chromium/issues/detail?id=389726691
- ChromeStatus.com entry: https://chromestatus.com/feature/5104000067985408