# Chrome 144 Stable - 弃用和移除

## 领域摘要

Chrome 144 标志着隐私沙盒计划的重大转变，弃用并移除了三个关键的隐私沙盒 API：Private Aggregation、Shared Storage 和 Protected Audience。随着 Chrome 宣布维持当前对第三方 Cookie 的处理方式，这些最初为无 Cookie 未来设计的 API 正在被逐步淘汰。此外，Chrome 144 通过弃用 XML 解析中外部加载的实体来解决安全问题，这减少了同步网络请求和潜在的攻击向量。这些变化反映了 Chrome 在隐私和安全方面不断演进的方法，同时为开发者简化了平台。

## 详细更新

Chrome 144 的弃用重点是通过移除不再符合 Chrome 第三方 Cookie 策略的隐私沙盒 API 来精简 Web 平台，同时解决 XML 安全问题。

### Deprecate and remove: Private Aggregation API

#### 新增内容

Private Aggregation API 旨在以保护隐私的方式测量跨站点聚合数据，现已从 Chrome 中弃用并移除。此 API 是原始隐私沙盒愿景的一部分，用于构建没有第三方 Cookie 的 Web。

#### 技术细节

Private Aggregation API 仅通过 Shared Storage 和 Protected Audience API 公开。由于这两个父 API 也正在被弃用，因此开发者无需针对 Private Aggregation 采取额外操作。随着依赖 API 的移除，该 API 会自动移除。

#### 重要性

随着 Chrome 维持其当前对第三方 Cookie 的处理方式，Privacy Aggregation API 不再服务于其预期目的。移除该 API 简化了平台，并消除了在生态系统中将保持未使用状态的 API。

#### 参考资料

- [ChromeStatus.com 条目](https://chromestatus.com/feature/4683382919397376)
- [规范](https://patcg-individual-drafts.github.io/private-aggregation-api)

### Deprecate and Remove: Shared Storage API

#### 新增内容

Shared Storage API 支持不按第一方站点分区的存储，现已被弃用并移除。此 API 旨在作为后第三方 Cookie 时代 Web 的隐私保护存储机制。

#### 技术细节

Shared Storage 提供未分区的存储能力，同时通过有限的输出通道维护隐私保证。然而，由于第三方 Cookie 仍然可用，该 API 的原始用例在当前 Chrome 架构中不再适用。

#### 迁移路径

使用 Shared Storage 的开发者应过渡回适合其用例的标准存储机制，例如第一方 Cookie、localStorage 或 IndexedDB，具体取决于其分区要求。

#### 参考资料

- [跟踪错误 #462465887](https://issues.chromium.org/issues/462465887)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5076349064708096)
- [规范](https://wicg.github.io/shared-storage)

### Deprecate and Remove Protected Audience

#### 新增内容

Protected Audience API（前身为 FLEDGE）提供基于兴趣组的广告投放，无需第三方 Cookie 或跨站点跟踪，现已从 Chrome 中弃用并移除。

#### 技术细节

Protected Audience 支持基于兴趣组的设备端广告竞价，允许广告商在保护用户隐私的同时触达相关受众。该 API 包括加入兴趣组、运行竞价和在隔离上下文中渲染广告的组件。

#### 对开发者的影响

为广告用例实现了 Protected Audience 的开发者应在第三方 Cookie 继续可用的背景下评估替代方法。移除时间表遵循 Chrome 的隐私沙盒功能状态页面。

#### 参考资料

- [ChromeStatus.com 条目](https://chromestatus.com/feature/6552486106234880)
- [规范](https://wicg.github.io/turtledove)

### Externally loaded entities in XML parsing

#### 新增内容

Chrome 正在弃用在不使用 XSLT 的 XML 文档中加载外部实体定义的功能。这移除了在解析期间同步获取外部 XML 实体和 DTD 的行为。

#### 技术细节

目前，Chrome 在特定情况下同步获取外部 XML 实体或 DTD，例如在 DOCTYPE 语句中定义外部实体时，或当 DOCTYPE 使用 SYSTEM 关键字指向外部 DTD 时。XML 规范不要求非验证处理器读取外部实体，这使 Chrome 能够灵活地移除此行为。

#### 安全和性能优势

移除外部实体加载消除了 XML 解析期间的同步网络请求，降低了安全风险（如 XML 外部实体攻击）和性能开销。使用 XSLT 的文档将继续支持转换处理所需的外部实体。

#### 迁移指南

开发者应在 XML 文档中内联必要的实体定义，而不是依赖外部引用。对于需要外部定义的复杂场景，请考虑预处理 XML 文档或迁移到基于 JSON 的数据格式。

#### 参考资料

- [跟踪错误 #455813733](https://issues.chromium.org/issues/455813733)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6734457763659776)
- [规范](https://www.w3.org/TR/xml/#proc-types)
