## 领域摘要

Chrome 143 (stable) 引入了一个面向 Isolated Web Apps (IWA) 的 Web Smart Card API。其核心目标是通过授予 IWA 对主机操作系统上的 PC/SC 堆栈和读卡器驱动程序的访问权限，使智能卡（PC/SC）应用能够迁移到 Web 平台。管理员可以控制该 API 的可用性（源内容已被截断，详见省略部分）。此更新通过连接本地智能卡硬件与以 Web 部署的隔离应用，推进了平台发展，改进了硬件支持的认证和企业迁移路径的选项。

## 详细更新

下面列出基于上述摘要的 isolated-web-apps 更改。

### Web Smart Card API for Isolated Web Apps（面向隔离 Web 应用）

#### 新增内容
- 使智能卡（PC/SC）应用能够迁移到面向 Isolated Web Apps 的 Web 平台，提供对主机操作系统上的 PC/SC 实现和读卡器驱动的访问。

#### 技术细节
- 仅对 Isolated Web Apps (IWA) 可用。  
- 授予 IWA 访问主机操作系统上存在的 PC/SC 实现和读卡器驱动的权限。  
- 管理员可以控制此 API 的可用性（源内容被截断，不包含完整的管理员配置详细信息）。  

#### 适用场景
- 允许现有的 PC/SC 智能卡应用迁移为以 IWA 运行，同时保持对主机智能卡基础设施的访问。  
- 支持需要直接访问操作系统级智能卡服务的 Web 应用场景，同时不向非隔离上下文暴露该 API。  

#### 参考资料
- [跟踪错误 #1386175](https://issues.chromium.org/issues/1386175)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6411735804674048)  
- [规范](https://wicg.github.io/web-smart-card)

已保存文件: digest_markdown/webplatform/Isolated Web Apps/chrome-143-stable-en.md