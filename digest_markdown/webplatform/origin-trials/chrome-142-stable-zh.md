# 领域摘要

Chrome 142 (stable) 引入了针对 Device Bound Session Credentials 的 Origin Trial，这是一种由服务器驱动的机制，用于将 Web 会话绑定到单一设备。该 Origin Trial 聚焦于更强的会话安全性：浏览器能够证明持有设备特定的 private key，并按服务器安排定期续期会话。对于开发者，这使得按设备的会话保证成为可能，可减少会话被窃取的风险并提升账户安全，而无需管理复杂的客户端密码学。该更新通过标准化一种对服务器友好的 proof-of-possession 流程并与现有会话架构集成，推动了 Web 平台的发展。

## 详细更新

此版本的单个 origin-trial 特性为需要设备绑定会话语义的开发者提供了一个专注的安全原语。

### Device Bound Session Credentials（设备绑定会话凭证）

#### 新增内容
一种机制，允许服务器将会话安全地绑定到单一设备。浏览器按服务器请求定期续期会话，并提供对 private key 的持有证明。

#### 技术细节
- 会话与设备特定的 private key 绑定；在续期时浏览器会证明其对该私钥的持有。
- 续期由服务器驱动并定期进行，使服务器能够在验证设备持有的同时控制会话生命周期。
- 该能力通过 Chrome 142 的 Origin Trial 提供（重要性：中等）。

#### 适用场景
- 为每个设备强制使用会话令牌以提高保证（例如：敏感账户操作）。
- 通过在续期时要求设备绑定的持有证明来降低被窃取的会话令牌的风险。
- 与服务器端会话管理集成，以按计划撤销或轮换设备绑定的凭证。

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials#/view_trial/3357996472158126081)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5140168270413824)  
- [规范](https://w3c.github.io/webappsec-dbsc)  
- [知识共享署名 4.0 许可证](https://creativecommons.org/licenses/by/4.0/)  
- [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0)  
- [Google Developers 站点政策](https://developers.google.com/site-policies)