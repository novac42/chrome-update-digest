digest_markdown/webplatform/Security-Privacy/chrome-138-stable-en.md

## 区域摘要

Chrome 138 的安全与隐私更新侧重于通过引入 Integrity-Policy header 来增强脚本完整性保障。对开发者的主要影响是为在站点范围内要求 Subresource Integrity (SRI) 验证脚本提供了一种标准化方式。这推进了 Web 平台，使其能够更有力地防御被篡改或意外的脚本资源，并支持集中式策略执行。此类更新重要的原因在于它们降低了供应链和第三方脚本的风险，并简化了 Web 应用的合规性与审计工作。

## 详细更新

此版本中的单一安全与隐私变更收紧了站点如何为脚本资源强制执行 SRI。以下为功能细节和直接参考资料。

### Integrity Policy for scripts（用于脚本的完整性策略）

#### 新增内容
Subresource Integrity (SRI) 已允许开发者验证加载的资源是否与预期内容匹配。Integrity-Policy header 提供了一种机制，使开发者能够要求对脚本进行 SRI 验证。

#### 技术细节
该功能引入了 Integrity-Policy HTTP header（按规范），允许站点运营者声明对脚本子资源的 SRI 验证要求。若存在该策略，浏览器的加载行为将受其影响，按照规范中定义的策略规则强制执行完整性检查。

#### 适用场景
- 在整个站点范围内强制执行 SRI，以确保所有加载的脚本都经过完整性检查。
- 通过要求完整性验证来降低被破坏的 CDN 或第三方脚本注入带来的风险。
- 通过 HTTP header 集中脚本完整性要求，从而简化安全审计和合规性工作。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5104518463627264
- 规范: https://w3c.github.io/webappsec-csp/#integrityPolicy