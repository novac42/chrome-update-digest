## 领域摘要

Chrome 133 在三个实用方向上推进了性能：基于 Energy Saver 的标签冻结、对元素/ LCP 指标的更具隐私意识的时序可见性，以及对 Early Hints 周围资源时序语义的更清晰定义 —— 另外还有针对 WGSL 的 GPU 着色器级别优化。对开发者影响最大的更改是 Energy Saver 冻结行为（影响后台工作和媒体/会议页面）、对跨域 `renderTime` 的粗化暴露（改善元素时序和 LCP 的可观测性）以及为首次响应头引入专用时间戳 `firstResponseHeadersStart` 以澄清资源时序。总体而言，这些更新在兼顾隐私的同时改善了功耗、测量准确性和 GPU 着色器吞吐量。

## 详细更新

以下条目扩展了上面的摘要，并列出针对关注性能的团队的可操作注意事项。

### Freezing on Energy Saver（节能模式下的冻结）

#### 新增内容
当 Energy Saver 启用且某个被隐藏并保持静默超过五分钟的 browsing context group，其内任何同源帧子组超过 CPU 使用阈值时，Chrome 将对该 browsing context group 执行冻结，但为提供音频或视频会议功能的页面设有例外（特征文本中描述了检测方式）。

#### 技术细节
冻结在五分钟的隐藏并静默窗口之后作用于 browsing-context-group 级别，并考虑同源帧子组的 CPU 使用情况以决定何时冻结。如特征描述所述，提供实时会议功能的页面通过检测逻辑被豁免。

#### 适用场景
在 Energy Saver 下，预计后台标签页和隐藏帧将被更积极地冻结；请设计后台任务、计时器和实时通信页面，以避免保持静默或在需要时显示阻止冻结的活动。

#### 参考资料
- [Tracking bug #325954772](https://issues.chromium.org/issues/325954772)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5158599457767424)

### Expose coarsened cross-origin `renderTime` in element timing and LCP (regardless of `Timing-Allow-Origin`)（在元素时序和 LCP 中暴露粗化的跨域 `renderTime`（不依赖 `Timing-Allow-Origin`））

#### 新增内容
Element timing 和 LCP 条目暴露 `renderTime` 属性（与图像或文本首次绘制的帧对齐）。Chrome 133 对跨域资源即使在未提供 `Timing-Allow-Origin` 头时也暴露一个粗化的 `renderTime`。

#### 技术细节
`renderTime` 属性仍与首次绘制帧语义对齐。对于跨域图像，原先要求 `Timing-Allow-Origin` 头部的做法被放宽，通过暴露一个粗化值在提高可观测性的同时保持隐私保护（参见特征文本和规范引用）。

#### 适用场景
元素时序和 LCP 的性能测量将对跨域资源的渲染事件获得可见性，而无需第三方资源修改头部；预计时间戳精度较低（粗化），但在诊断感知绘制时序方面覆盖率更好。

#### 参考资料
- [Tracking bug #373263977](https://issues.chromium.org/issues/373263977)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5128261284397056)
- [Spec](https://w3c.github.io/paint-timing/#mark-paint-timing)

### Revert `responseStart` and introduce `firstResponseHeadersStart`（恢复 `responseStart` 并引入 `firstResponseHeadersStart`）

#### 新增内容
Chrome 133 引入 `firstResponseHeadersStart` 来表示第一次响应头的时间戳（例如 Early Hints / 103），并恢复 `responseStart` 的语义以澄清资源时序测量。

#### 技术细节
在存在 Early Hints (103) 的情况下，会有不同的时间戳：Early Hints 到达与最终响应头到达。Chrome 先前引入了 `firstInterimResponseStart` 并更改了 `responseStart`；此更新添加 `firstResponseHeadersStart` 以明确捕获首次头部到达，并恢复 `responseStart` 的语义以便资源时序 API 更清晰。

#### 适用场景
依赖 Resource Timing 的遥测和监控工具在测量头部到达时应迁移去观察 `firstResponseHeadersStart`（例如为 Early Hints 做计量），并更新任何依赖先前 `responseStart` 语义的逻辑。

#### 参考资料
- [Tracking bug #40251053](https://issues.chromium.org/issues/40251053)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5158830722514944)
- [Spec](https://w3c.github.io/resource-timing/#dom-performanceresourcetiming-finalresponseheadersstart)

### WGSL performance gains with discard（使用 discard 的 WGSL 性能提升）

#### 新增内容
Chrome 133 更新了 WGSL `discard` 语句的实现，在平台提供将其降级为 helper invocation 的语义时加以利用，从而在受影响的渲染场景中大幅恢复性能。

#### 技术细节
该更改针对 `discard` 导致性能下降的情况（尤其是复杂的屏幕空间反射）。通过利用平台语义将其降级为 helper invocation，过去触发高开销行为的着色器执行路径现在如特征说明所述表现更好。

#### 适用场景
使用 WGSL 的 WebGPU 着色器作者（尤其是像 SSR 这样的效果）在使用 `discard` 时可以期待性能改善。审查那些以前为缓解其他问题而使用 `discard` 的着色器——平台级优化可能消除了先前的性能惩罚。

#### 参考资料
- [discard statement](https://gpuweb.github.io/gpuweb/wgsl/#discard-statement)
- [issue 372714384](https://issues.chromium.org/372714384)