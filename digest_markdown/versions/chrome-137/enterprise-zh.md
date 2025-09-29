## Area Summary

Chrome 137 (Enterprise) 侧重于通过为企业托管的浏览器添加 IP 地址收集与上报来改进安全监控。对开发者和管理员影响最大的更改是将本地和远程 IP 提供给 Security Investigation Logs (SIT)，管理员可选择性地允许发送 IP 地址。这推动了平台在事件响应和审计工作流程中的遥测能力改进，同时为企业数据处理提供了管理控制。这些更新重要在于，它们为受管理的环境中的威胁调查和运维故障排查提供了更丰富的信号。

## Detailed Updates

The single Enterprise feature in this release focuses on telemetry and logging enhancements that align with enterprise security and operational needs.

### IP address logging and reporting (IP 地址记录与报告)

#### What's New
Chrome Enterprise 收集并上报本地和远程 IP 地址，并将这些 IP 地址发送到 Security Investigation Logs (SIT)。管理员可选择性地允许发送 IP 地址。

#### Technical Details
- 收集与上报覆盖本地和远程 IP。
- 报告的 IP 数据会转发到现有的 SIT 管道。
- 管理控制允许通过企业策略可选地传输 IP 地址数据（通过策略选择加入）。

#### Use Cases
- 安全监控与事件响应：为 SIT 中的调查提供更丰富的遥测数据。
- 审计与合规：为企业审计提供额外的网络归因数据。
- 故障排查与运营：在受管理部署中为诊断连接或路由问题提供 IP 级别的上下文。

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5110849951309824

## Area-Specific Expertise Notes (Enterprise focus)
- security-privacy: Adds enterprise-controlled IP telemetry to SIT, increasing forensic capability while requiring admin decision on data sharing.
- performance / devices / webapi: Minimal direct platform API changes noted; focus is on telemetry pipelines rather than public web APIs.
- deprecations: No deprecations indicated; assess policy rollout for enterprise compatibility and privacy policies.
- pwa-service-worker, javascript, webassembly, graphics-webgpu, multimedia, css: No direct changes reported in these subdomains for this feature.

Saved to: digest_markdown/webplatform/Enterprise/chrome-137-stable-en.md