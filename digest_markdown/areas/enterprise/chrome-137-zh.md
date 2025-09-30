---
layout: default
title: chrome-137-zh
---

## 详细更新

下列为上述摘要所述的 Enterprise 区域更改。

### IP address logging and reporting（IP 地址记录与上报）

#### 新增内容
Chrome Enterprise 收集并报告本地和远程 IP 地址，并将这些 IP 地址发送到 Security Investigation Logs (SIT)。管理员可以可选择启用发送 IP 地址。

#### 技术细节
Chrome 捕获网络端点信息（本地和远程 IP）并将该数据包含在供企业安全工具使用的 SIT 条目中。提供了管理员控制，组织可以选择是否将 IP 地址数据作为其调查日志的一部分进行转发。

#### 适用场景
- 安全监控与事件响应：通过网络上下文丰富告警，以更快进行根本原因分析。
- 取证调查：在 SIT 中跨事件关联端点 IP。
- 管理策略控制：允许组织在遥测实用性与隐私/合规需求之间进行权衡。

#### 参考资料
- https://chromestatus.com/feature/5110849951309824
