---
layout: default
title: chrome-138-zh
---

## 领域摘要

Chrome 138 在安全-隐私方面的更新集中在通过引入 Integrity-Policy 机制来加强脚本完整性保障。对开发者影响最大的是一种由服务器控制的方式，用于断言脚本已通过 Subresource-Integrity (SRI) 验证，从而弥补 SRI 可能未被一致应用的漏洞。此举推动了 Web 平台的发展，使脚本加载的完整性要求可被强制执行，降低了供应链篡改和意外脚本替换的风险。这些更新的重要性在于为团队提供了一种可部署的策略工具，以在不修改各个 <script> 标签的情况下提高脚本的基线安全性。

## 详细更新

Below are the Security-Privacy changes relevant to developers and security engineers, focused on enforceable script integrity.

### Integrity Policy for scripts（脚本完整性策略）

#### 新增内容
Subresource-Integrity (SRI) enables developers to verify that loaded assets match expected content. The Integrity-Policy header gives developers the ability to assert that scripts are validated using SRI.

#### 技术细节
- 该功能引入了由服务器发送的策略（Integrity-Policy 响应头），用于指示获取到的脚本应附带 SRI 元数据的要求或期望。
- 实现细节和响应头的精确定义在 webappsec 与 CSP 相关的规范中规定（见 参考资料）。请参考该规范和 ChromeStatus 条目以获取兼容性和部署说明。

#### 适用场景
- 在敏感页面（支付、认证）的所有脚本上强制应用 SRI，而无需修改每个 <script> 标签。
- 通过将完整性验证作为可部署的策略，降低被攻破的 CDN 或注入脚本修改导致的风险。
- 通过提供基于单一响应头的完整性要求断言，便于审计和自动化检查。

#### 参考资料
- ChromeStatus.com 条目：https://chromestatus.com/feature/5104518463627264
- 规范：https://w3c.github.io/webappsec-csp/#integrityPolicy

保存到：digest_markdown/webplatform/Security-Privacy/chrome-138-stable-en.md
