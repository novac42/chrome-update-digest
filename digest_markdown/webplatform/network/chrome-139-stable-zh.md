## 领域摘要

Chrome 139（稳定版）通过限制客户端头部中的标识面和强化 Windows 上的 TCP 暂时端口分配，提升了网络领域的隐私性和鲁棒性。对开发者影响最大的更改是减少完整 Accept-Language 列表的暴露（影响服务器端的语言检测和指纹识别）以及对临时 TCP 端口进行随机化（影响连接重用特性和临时端口的可预测性）。这些更新共同推动平台采用以隐私为先的默认设置，同时提高网络栈的弹性。这些更改很重要，因为它们改变了服务器能从请求推断的信息，并可能影响受影响 Windows 版本上的网络诊断和连接行为。

## 详细更新

Below are the Network-area changes in Chrome 139 that follow from the summary above.

### Reduce fingerprinting in Accept-Language header information（减少 Accept-Language 头信息中的指纹识别）

#### 新增内容
Chrome 减少了 `Accept-Language` 头和 `navigator.languages` 暴露的信息：不再在每个 HTTP 请求中发送用户完整的首选语言列表，而仅发送用户的首选语言。

#### 技术细节
此更改限制了 `Accept-Language` 头的值字符串和 `navigator.languages`，以减少被动指纹识别可用的表面。该行为适用于 HTTP 请求头和 `navigator.languages` API。

#### 适用场景
- 服务器端的本地化和内容协商每次请求只会看到首选语言；开发者应确保回退逻辑和显式语言协商保持健壮。
- 减少分析或反欺诈启发式中被动指纹识别的向量。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/1306905)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

### Randomize TCP port allocation on Windows（在 Windows 上随机化 TCP 端口分配）

#### 新增内容
Chrome 在大约 2020 年及以后的 Windows 版本上启用了随机化的 TCP 端口分配，前提是快速端口重用不会导致重用超时失败。

#### 技术细节
该发布将临时 TCP 端口随机化，以避免由可预测分配引起的冲突模式（发行说明将生日问题列为快速端口重用冲突的来源）。这一更改针对那些端口重用时序对随机化分配是安全的 Windows 发行版。

#### 适用场景
- 加强网络栈对临时端口可预测性的抗性，提高隐私性，并使某些指纹识别或探测技术不那么可靠。
- 可能改变诊断时观察到的连接重用特性；假定端口序列确定性的网络工具和测试应予以审查。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/40744069)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

领域特定说明（网络视角）
- 安全-隐私：两个功能都减少了指纹识别表面并增加网络标识符的不可预测性。
- 性能：端口随机化可能影响临时端口重用模式和对时序敏感的连接行为；请测试负载和连接重试逻辑。
- pwa-service-worker / webapi：减少 `Accept-Language` 暴露适用于来源于 service workers 的请求，并影响客户端的语言检测 APIs。
- 弃用：依赖完整 `Accept-Language` 列表的服务器端本地化应提供显式偏好机制或回退策略。