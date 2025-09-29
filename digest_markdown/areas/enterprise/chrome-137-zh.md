---
layout: default
title: chrome-137-zh
---

### 1. Area Summary

Chrome 137 for Enterprise 侧重于为受管环境改进网络遥测，具体通过收集并报告本地和远程 IP 地址以辅助安全调查。对开发者和管理员影响最大的是将 IP 地址记录并可选地发送到 Security Investigation Logs (SIT)，以增强事件响应与取证。本次更新通过向企业安全工具暴露更丰富的运行信号来推进平台，同时为管理员引入配置与隐私方面的考量。团队应评估集成、保留和策略设置，以负责任地利用该遥测。

## Detailed Updates

Below are the Enterprise-specific changes in this release and their practical implications for developers and administrators.

### IP address logging and reporting

#### What's New
Chrome Enterprise collects and reports local and remote IP addresses and sends those IP addresses to the Security Investigation Logs (SIT). In addition, Chrome Enterprise will allow admins to optionally send the IP addresses...

#### Technical Details
- 浏览器捕获本地和远程 IP 地址信息，作为其企业遥测的一部分，并将该数据转发到 SIT。
- 管理员有可选控制以启用将 IP 地址发送到 SIT；这意味着报告行为由管理员可配置的策略或设置来管理。
- 该功能提高了企业调查与监控工具可用的安全日志的详细程度与准确性。

#### Use Cases
- 需要对可疑活动进行网络端点归属的事件响应与取证调查。
- 通过将 SIT 导出与 SIEMs 和集中安全工具集成，以将浏览器事件与网络日志关联。
- 在需要了解客户端网络上下文的合规与审计工作流程中（受组织隐私规则约束）。

#### References
- ChromeStatus.com entry: https://chromestatus.com/feature/5110849951309824
