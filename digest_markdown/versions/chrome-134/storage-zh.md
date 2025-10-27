---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 134 在 Shared Storage 上取得进展，重点改进可观测性、贡献控制和并发安全性。主要更改包括向 Shared Storage worklet 添加一个 `interestGroups()` 访问器、通过 Private Aggregation 的新 `maxContributions` 字段允许对每个上下文的贡献数进行限制，以及将 Web Locks API 集成到 Shared Storage worklet 中。这些更新提高了测量准确性，为调用方提供了更细粒度的聚合行为控制，并减少了由竞争条件导致的重复上报——这对实现安全、可靠的跨站点测量和基于存储的逻辑的开发者很重要。

## 详细更新

下面的条目对摘要进行了扩展，重点说明了变更内容、高层工作方式以及对开发者的实际用途。

### Allow reading interest groups in Shared Storage Worklet（在 Shared Storage Worklet 中允许读取 interest groups）

#### 新增内容
在 Shared Storage worklet 中新增了一个 `interestGroups()` 方法，该方法返回与 shared storage origin 的所有者相关联的 Protected Audience interest groups，并包含一些附加元数据。

#### 技术细节
公开了一个 worklet 级别的 API 方法，用于枚举 shared storage origin 的 Protected Audience interest groups。该方法在 Shared Storage worklet 的执行上下文中暴露（JavaScript/webapi 层面）。

#### 适用场景
使 Protected Audience 的买方和测量集成在 worklet 环境内对 interest-group 状态有更好的可见性，便于调试、归因和验证由 shared-storage 驱动的逻辑。

#### 参考资料
https://chromestatus.com/feature/5074536530444288

### Private Aggregation API: per-context contribution limits for Shared Storage callers（为 Shared Storage 调用方提供每上下文贡献限制）

#### 新增内容
允许 Shared Storage 调用方通过新字段 `maxContributions` 自定义每个 Private Aggregation 报告的贡献数量。

#### 技术细节
调用方可以设置 `maxContributions` 来覆盖在生成 Private Aggregation 报告时给定上下文的默认贡献计数。这是 Private Aggregation API 草案中面向 webapi 的一个配置选项，见下方链接。

#### 适用场景
对需要控制聚合粒度或限制每个上下文报告大小以平衡隐私、负载大小和下游处理的开发者与测量系统有用。

#### 参考资料
https://issues.chromium.org/issues/376707230
https://chromestatus.com/feature/5189366316793856
https://github.com/patcg-individual-drafts/private-aggregation-api/pull/164/files

### Support Web Locks API in Shared Storage（在 Shared Storage 中支持 Web Locks API）

#### 新增内容
将 Web Locks API 集成到 Shared Storage worklet 中，以防止竞态条件（例如，由并发的 `get()`/`set()` 流导致的跨站点覆盖测量中的重复上报）。

#### 技术细节
在 Shared Storage worklet 执行环境内引入了 `navigator.locks.request` 的可用性，使 worklet 代码可以获取锁并对 `get()`/`set()` 逻辑的关键部分进行串行化，以避免重复或不一致状态。

#### 适用场景
有助于需要在并发任务之间协调更新的测量和以存储为主的工作负载——改善正确性，减少在应用层为锁定模式编写零散解决方案的需求。

#### 参考资料
https://issues.chromium.org/issues/373899210
https://chromestatus.com/feature/5133950203461632

文件已保存至：digest_markdown/webplatform/storage/chrome-134-stable-en.md
