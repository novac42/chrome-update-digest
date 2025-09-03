````markdown
digest_markdown/webplatform/Performance/chrome-139-stable-zh.md

---

# Chrome 139 性能更新摘要

## 1. 执行摘要

Chrome 139 在性能领域带来了三项重要更新：增强的 WebXR 深度感知自定义、实验性软导航性能条目，以及 Android 上显著加快的后台冻结速度。这些更改共同提升了资源管理、开发者可观测性，以及 Web 应用的实时性能优化能力。

## 2. 关键影响

### 技术影响

- **现有实现**：使用 WebXR 深度感知的应用现在可以更精细地调整缓冲区行为以提升性能。依赖导航启发式的网站获得了新的可观测工具。Android Web 应用需适应更激进的后台冻结策略。
- **新能力**：开发者可在 WebXR 中请求原始或平滑深度缓冲区，通过性能时间线观察软导航事件，并依赖更快的 Android 页面资源释放。
- **技术债务考量**：依赖 Android 较长后台生命周期的旧代码可能需要重构。监控和分析系统应更新以利用新的性能条目。

## 3. 风险评估

**关键风险**：
- 这些功能未发现破坏性更改或直接安全问题。

**中等风险**：
- **弃用**：Android 上缩短的后台冻结窗口可能导致依赖延长后台活动的模式被弃用。
- **性能影响**：如果未正确配置，新的 WebXR 深度缓冲区选项滥用可能导致性能不佳。

## 4. 推荐行动

### 立即行动

- 检查 Android Web 应用的后台活动依赖，针对新的 1 分钟冻结窗口进行必要重构。
- 通过 Origin Trial 试验 `SoftNavigation` 性能条目，提升导航分析能力。
- 审查 WebXR 深度感知用法，更新缓冲区请求以获得最佳性能。

### 短期规划

- 更新监控和分析仪表盘，纳入新的性能条目。
- 向开发团队普及 Android 更快后台冻结的影响。
- 评估并记录 WebXR 深度缓冲区配置的最佳实践。

### 长期策略

- 跟踪 `SoftNavigation` 和 WebXR 深度感知改进的采用情况及反馈。
- 关注 Chrome 路线图中后台进程管理的进一步变化。
- 随着实验性功能趋于稳定，规划更广泛的推广和标准化。

## 5. 功能分析

---

### WebXR depth sensing performance improvements（WebXR 深度感知性能改进）

**影响级别**：🟡 重要

**变更内容**：
在 WebXR 会话中开放多种新机制，用于自定义深度感知功能的行为，旨在提升生成或使用深度缓冲区的性能。开发者现在可请求原始或平滑深度缓冲区，并调整其他参数以优化资源使用。

**重要原因**：
对深度缓冲区行为的细粒度控制，使开发者能够在沉浸式体验中平衡性能与质量，降低 AR/VR 应用的延迟和资源消耗。

**实施指南**：
- 审查当前 WebXR 深度感知用法，判断原始或平滑缓冲区更适合您的场景。
- 在实际环境中测试不同缓冲区配置的性能影响。
- 关注规范和浏览器支持的最新动态。

**参考资料**：
- [Tracking bug #410607163](https://issues.chromium.org/issues/410607163)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864)
- [Spec](https://immersive-web.github.io/depth-sensing)

---

### `SoftNavigation` performance entry（`SoftNavigation` 性能条目）

**影响级别**：🟡 重要

**变更内容**：
通过 `PerformanceObserver` 和性能时间线向 Web 开发者引入实验性软导航启发式。报告两个新的性能条目：`soft-navigation`（用于用户交互导致页面导航）以及新的 `timeOrigin`，帮助对这些事件的时间数据进行分段。

**重要原因**：
为开发者提供了对未触发完整页面重载的导航事件的深入洞察，有助于更准确地衡量和优化单页应用及动态导航模式的性能。

**实施指南**：
- 参与 Origin Trial，测试并集成 `SoftNavigation` 条目。
- 更新性能监控工具，捕获并分析这些新条目。
- 利用新的 `timeOrigin` 对导航相关指标进行分段和优化。

**参考资料**：
- [Origin Trial](https://developer.chrome.com/origintrials#/view_trial/21392098230009857)
- [Tracking bug #1338390](https://issues.chromium.org/issues/1338390)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5144837209194496)
- [Spec](https://wicg.github.io/soft-navigations)

---

### Faster background freezing on Android（Android 更快后台冻结）

**影响级别**：🔴 关键

**变更内容**：
将 Android 上后台页面及相关 worker 的冻结时间从五分钟缩短至一分钟，加快资源释放，提升设备性能。

**重要原因**：
此更改对依赖后台活动的 Web 应用影响显著，如周期性同步或延迟处理。开发者需确保关键任务能在更短窗口内完成，以避免意外中断。

**实施指南**：
- 检查 Android Web 应用中的后台任务，确保能在一分钟内完成。
- 重构长时间运行的后台进程，使其适应新的冻结时间线。
- 监控用户体验，关注与后台冻结相关的性能回退。

**参考资料**：
- [Tracking bug #435623337](https://issues.chromium.org/issues/435623337)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

---
````