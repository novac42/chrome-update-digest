---
layout: default
title: chrome-137-zh
---

## 领域摘要

Chrome 137 (stable) 针对企业的重点是增强安全监控和事件响应。该版本新增收集和报告本地和远程 IP 地址，并将这些地址转发到 Security Investigation Logs (SIT)。管理员被提示可以选择是否发送 IP 地址相关的控制。这些更新加强了企业在调查和集中安全工具方面的可见性。

## 详细更新

下面是对上述摘要的企业领域更改的详细说明。

### IP address logging and reporting (IP 地址记录和报告)

#### 新增内容
Chrome Enterprise 正在通过收集并报告本地和远程 IP 地址并将这些 IP 地址发送到 Security Investigation Logs (SIT)，来增强安全监控和事件响应能力。此外，Chrome Enterprise 将允许管理员可选择性地发送 IP 地址...

#### 技术细节
- 发布说明指出，Chrome 将收集本地和远程 IP 地址，并将其报告到 SIT。
- 说明还指出存在一个管理员选项，可用于选择性地发送 IP 地址（详见参考资料以获取完整细节）。

#### 适用场景
- 通过在集中日志中呈现网络级指标，改善企业安全监控和事件响应。
- 使使用 SIT 的组织能够在调查中将浏览器活动与 IP 级数据关联。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5110849951309824

保存路径: digest_markdown/webplatform/Enterprise/chrome-137-stable-en.md
