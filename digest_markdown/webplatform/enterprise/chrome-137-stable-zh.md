## 领域摘要

Chrome 137（stable）引入针对 Enterprise 的定向遥测增强，重点在于网络可见性：Chrome Enterprise 将收集并报告本地和远程 IP 地址以改进安全监控。对开发者和 IT 团队影响最大的更改是将这些 IP 地址集成到 Security Investigation Logs (SIT)，从而增强事件响应和取证关联。此类更新通过提高可审计性并在安全调查中提供更丰富的上下文，推进了企业场景下的 Web 平台。团队应据此评估日志、保留和隐私实践。

## 详细更新

本次发布的唯一 Enterprise 功能加强了面向企业客户和安全团队的与网络相关的遥测。

### IP address logging and reporting（IP 地址记录与报告）

#### 新增内容
Chrome Enterprise 收集并报告本地和远程 IP 地址，并将这些 IP 地址发送到 Security Investigation Logs (SIT)。管理员将可以选择将 IP 地址数据作为该能力的一部分发送的选项。

#### 技术细节
- 收集的数据包括与相关浏览器活动关联的本地和远程 IP 地址，并会转发到 SIT 以供企业安全调查。
- 管理员将有一个选择加入机制以启用发送 IP 地址数据（详细信息和控制请参考官方链接）。

#### 适用场景
- 安全调查与事件响应：将浏览器事件与网络端点关联。
- 审计与取证：为 SIT 条目添加网络上下文，以改进根因分析。
- 企业监控：用浏览器收集的 IP 数据丰富现有的安全遥测，以加快检测速度。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5110849951309824