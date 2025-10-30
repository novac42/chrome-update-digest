# 领域摘要

Chrome 142 引入了一项聚焦的安全-隐私更改，通过在显式权限提示后面放置对用户本地网络的 Web 请求来限制这些请求。主要主题是收紧对本地 IP 和回环接口的跨源访问，以减少无意或恶意的本地网络探测。对开发者影响最大的变化是需要为针对本地地址或回环的请求处理新的权限流程。此举通过减少对本地资源和内网主机的静默访问来实现对 Web 平台的安全强化。

## 详细更新

下面是 Chrome 142 中与处理本地网络访问的开发者相关的安全-隐私更新。

### Local network access restrictions（本地网络访问限制）

#### 新增内容
Chrome 142 限制向用户本地网络发起请求的能力，此类请求需通过一个权限提示来授权。

#### 技术细节
本地网络请求是指任何从公共网站到本地 IP 地址或回环接口的请求，或从本地网站（例如内网）到回环的请求。将 Web 发起此类请求的能力置于门控...

#### 适用场景
- 联系本地设备、服务或内网端点的 Web 应用在发起此类请求时会遇到权限提示。  
- 开发者应检测并处理权限被拒绝的场景，在访问本地地址被阻止时呈现清晰的提示或回退方案。

#### 参考资料
- [跟踪错误 #394009026](https://issues.chromium.org/issues/394009026)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5152728072060928)  
- [规范](https://wicg.github.io/local-network-access)

已保存文件：digest_markdown/webplatform/Security-Privacy/chrome-142-stable-en.md