---
layout: default
title: webapi-zh
---

## 领域摘要

Chrome 134 的 Web API 更新侧重于增强隐私保护测量、共享存储能力和 API 等价性，同时减少竞态条件并改进设备端滥用检测。关键更改包括新的 Shared Storage worklet APIs（interestGroups、Web Locks 集成和 Private Aggregation 控制）、attribution-reporting 调整、基于缓存的 bounce-tracking 缓解措施、OffscreenCanvas 等价性，以及基于设备端 LLM 的通知过滤器。这些更改通过支持更丰富且同步的测量与存储工作流，同时收紧隐私和滥用防护，推动平台演进。处理测量、并发、图形和通知的开发者应审阅新的原语和限制以相应调整实现。

## 详细更新

下面是对 Chrome 134 每项 Web API 更改的简明、面向开发者的描述，以及它们如何影响常见工作流。

### Allow reading interest groups in Shared Storage Worklet（允许在 Shared Storage Worklet 中读取 interest groups）

#### 新增内容
为 shared storage worklet 添加了一个 `interestGroups()` 方法，该方法返回与 shared storage origin 的所有者关联的 Protected Audience interest groups，并包含附加元数据。

#### 技术细节
worklet 的 API 表面现在向 Shared Storage worklets 暴露 interest group 数据，作用域限定为 shared storage origin 的所有者；每条条目包含元数据。

#### 适用场景
允许在 Shared Storage worklets 中运行的买方和测量代码检查关联的 interest groups，以便更好地理解和验证 Protected Audience 流程。

#### 参考资料
- ChromeStatus.com entry: https://chromestatus.com/feature/5074536530444288

### Attribution reporting Feature: Remove aggregatable report limit when trigger context ID is non-null（Attribution reporting 特性：当 trigger context ID 非空时移除可聚合报告限制）

#### 新增内容
在触发器提供非空 context ID 的情况下，移除了现有的每个 source registration 的 aggregatable 报告上限，以响应 API 调用方的需求。

#### 技术细节
当触发器提供非空的 context ID 时，先前对每个 source registration 的最多 20 份 aggregatable 报告的限制将被取消，以便支持更高容量的转化测量。

#### 适用场景
需要针对某些用户流程生成超过 20 份 aggregatable 报告的测量系统现在可以在使用 trigger context IDs 时依赖更完整的报告。

#### 参考资料
- ChromeStatus.com entry: https://chromestatus.com/feature/5079048977645568

### Bounce tracking mitigations on HTTP Cache（对 HTTP Cache 的 bounce-tracking 缓解措施）

#### 新增内容
将反跳转跟踪（anti-bounce-tracking）行为扩展到 HTTP cache，移除了对可疑跟踪站点必须执行 storage access 才能触发缓解措施的要求。

#### 技术细节
bounce-tracking 缓解措施现在独立于 storage-access 状态应用于 HTTP cache 交互，使缓存级别的保护与规范中定义的导航跟踪缓解措施保持一致。

#### 适用场景
站点和中间件应预期对可疑跟踪者施加更严格的缓存行为；依赖缓存语义进行跨站测量的开发者可能需要审查并调整其实现。

#### 参考资料
- Tracking bug #40264244: https://issues.chromium.org/issues/40264244
- ChromeStatus.com entry: https://chromestatus.com/feature/6299570819301376
- Spec: https://privacycg.github.io/nav-tracking-mitigations/#bounce-tracking-mitigations

### LLM-powered on-device detection of abusive notifications on Android（在 Android 上基于 LLM 的设备端滥用通知检测）

#### 新增内容
引入了设备端基于 LLM 的检测，用于隐藏被怀疑为滥用的通知内容，并为用户提供解散、显示或取消订阅该来源的选项。

#### 技术细节
一个设备端模型对可能滥用的通知进行分类；被标记的通知在用户操作前会先被隐藏。

#### 适用场景
以通知为主的 Web 应用和推送提供者应注意，当通知被标记时，Android 上的部分通知可能默认被隐藏；实现者应提供清晰的取消订阅和用户控制选项。

#### 参考资料
- ChromeStatus.com entry: https://chromestatus.com/feature/5303216063119360

### `OffscreenCanvas` `getContextAttributes`

#### 新增内容
将 CanvasRenderingContext2D 的 getContextAttributes 接口添加到 OffscreenCanvasRenderingContext2D。

#### 技术细节
OffscreenCanvas 上的上下文现在公开与主线程 CanvasRenderingContext2D 相同的 getContextAttributes 方法签名和行为，用于检索上下文创建属性。

#### 适用场景
基于 worker 的渲染和离主线程的 canvas 工作流获得了 API 等价性，简化了基于 canvas 的渲染代码的特性检测和可移植性。

#### 参考资料
- Tracking bug #388437261: https://issues.chromium.org/issues/388437261
- ChromeStatus.com entry: https://chromestatus.com/feature/5508068999430144
- Spec: https://github.com/whatwg/html/pull/10904

### Private Aggregation API: per-context contribution limits for Shared Storage callers（Private Aggregation API：为 Shared Storage 调用方设置按上下文的贡献限制）

#### 新增内容
允许 Shared Storage 调用方通过新的 `maxContributions` 字段为 Private Aggregation 报告设置每个上下文的贡献上限。

#### 技术细节
调用方可以为每个上下文提供 `maxContributions` 来覆盖 Private Aggregation 的默认贡献计数，从而影响聚合进报告中的贡献数量。

#### 适用场景
使用 Shared Storage 的测量集成者可以根据每个上下文的预期贡献密度调整 Private Aggregation 报告的噪声和有效载荷大小。

#### 参考资料
- Tracking bug #376707230: https://issues.chromium.org/issues/376707230
- ChromeStatus.com entry: https://chromestatus.com/feature/5189366316793856
- Spec: https://github.com/patcg-individual-drafts/private-aggregation-api/pull/164/files

### Support Web Locks API in Shared Storage（在 Shared Storage 中支持 Web Locks API）

#### 新增内容
将 Web Locks API 集成到 Shared Storage worklets 中，为 worklet 环境添加了 navigator.locks.request。

#### 技术细节
Shared Storage worklets 可以使用 `navigator.locks.request` 获取锁，从而在 `get()`/`set()` 操作之间防止竞态条件并避免跨站测量中的重复报告。

#### 适用场景
对 Shared Storage 执行并发读/写的 worklets 可以序列化关键区段，避免重复报告并提升测量与存储工作流中的数据一致性。

#### 参考资料
- Tracking bug #373899210: https://issues.chromium.org/issues/373899210
- ChromeStatus.com entry: https://chromestatus.com/feature/5133950203461632

File saved to: digest_markdown/webplatform/Web API/chrome-134-stable-en.md
