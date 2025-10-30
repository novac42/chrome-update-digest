---
layout: default
title: chrome-142-zh
---

## 领域摘要

Chrome 142 引入了一项针对性的安全更改，通过在发起本地网络请求时增加权限提示，限制 web 来源对用户本地网络的请求。主要趋势是更严格地控制跨来源对本地和环回 IP 的访问，以减少对设备的无意探测和信息泄露。对开发者而言，最重要的变化是来自公共站点到本地 IP（以及来自本地站点到环回）的请求现在可能需要明确的用户许可，这会影响设备发现、管理控制台和基于局域网的集成。此举通过规范本地网络访问的用户同意语义并使浏览器行为与 WICG 的 local-network-access 规范保持一致，推动了 Web 平台的发展。

## 详细更新

Below are the specific Network-area updates and what development teams should plan for based on the summary above.

### Local network access restrictions（本地网络访问限制）

#### 新增内容
Chrome 142 限制对用户本地网络和环回地址发起请求的能力；此类请求现在需要先经过权限提示。

#### 技术细节
“本地网络请求”被定义为：从公共网站到本地 IP 地址或环回的任何请求，或从本地网站（例如内联网）到环回的请求。浏览器在允许这些跨边界请求之前会向用户展示权限提示。该行为遵循 WICG 的 "local-network-access" 规范；有关实现进度，请参见跟踪和状态链接。

#### 适用场景
- 发现或控制局域网设备（IoT、打印机、摄像头）的 Web 应用必须处理被拒绝权限的情况，并提供后备的用户体验或替代连接流程。  
- 依赖环回访问的内联网和管理工具应检测并呈现权限请求，并记录所需的用户操作。  
- 在测试和 CI 环境中模拟本地设备交互可能需要更改配置以授予权限，或使用允许本地网络访问的策略运行。  

#### 参考资料
- [跟踪错误 #394009026](https://issues.chromium.org/issues/394009026)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5152728072060928)  
- [规范](https://wicg.github.io/local-network-access)
