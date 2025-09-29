Area Summary

Chrome 139 (stable) Network 更新侧重于隐私强化和传输层鲁棒性。此版本减少了通过 Accept-Language 暴露的客户端识别信息，并在受支持的 Windows 版本上引入了随机化的 TCP 短暂端口分配。此类更改主要推动 Web 隐私和连接可靠性，要求开发者与服务器容忍更不精细的语言信号并预期更高的端口熵。更改重要，因为它们减少了指纹识别面并缓解了可能影响连接建立的端口重用冲突。

## Detailed Updates

The following Network-specific items from Chrome 139 are summarized with practical implications for developers and operations teams.

### Reduce fingerprinting in Accept-Language header information (减少 Accept-Language 指纹识别信息)

#### What's New
Reduces the amount of information the `Accept-Language` header value string exposes in HTTP requests and in `navigator.languages`. Instead of sending a full list of the user's preferred languages on every HTTP request using the `Accept-Language` header, Chrome only sends the user's most preferred la...

#### Technical Details
The change truncates the language signal sent from the browser to servers and to the `navigator.languages` API surface, limiting the data available for cross-site fingerprinting and server-side inference.

#### Use Cases
- Privacy-sensitive web apps and analytics should expect less granular per-request language data.
- Server-side content negotiation relying on full language lists must adapt to receiving only the top-preferred language.

#### References
- 跟踪 bug #1306905 — https://issues.chromium.org/issues/1306905
- ChromeStatus.com entry — https://chromestatus.com/feature/5188040623390720

### Randomize TCP port allocation on Windows (在 Windows 上随机化 TCP 端口分配)

#### What's New
Enables TCP port randomization on versions of Windows (2020 or later) where port re-use issues are not expected to occur too rapidly, addressing allocation predictability and reuse-related failures.

#### Technical Details
The launch randomizes ephemeral TCP port selection to reduce collisions and the likelihood of rejections caused by rapid port re-use. The rollout targets Windows releases where the risk of problematic fast re-use (a manifestation of the Birthday problem) is low.

#### Use Cases
- Servers and clients should see fewer transient connection failures due to port re-use collisions on supported Windows versions.
- Network debugging and NAT/firewall rules should account for increased ephemeral port entropy.

#### References
- 跟踪 bug #40744069 — https://issues.chromium.org/issues/40744069
- ChromeStatus.com entry — https://chromestatus.com/feature/5106900286570496

Area-Specific Expertise (Network implications)

- css: 本次发布无直接影响；样式/布局行为不受这些 Network 更改影响。
- webapi: `navigator.languages` 暴露减少；读取此 API 的 Web 应用将收到更少的数据。
- graphics-webgpu: 与这些 Network 项目无关。
- javascript: 检查 `navigator.languages` 的客户端脚本应能处理更短的语言列表。
- security-privacy: 主要受益方——减少指纹识别面并增加传输层不可预测性。
- performance: TCP 端口随机化可提升连接可靠性，但可能影响假定端口可预测的诊断。
- multimedia: 媒体流堆栈应能适应短暂端口行为；无编解码器更改。
- devices: 无直接设备 API 影响。
- pwa-service-worker: Service worker 应继续工作；accept-language 更改可能影响本地化的 fetch 响应。
- webassembly: 无直接影响。
- 弃用: 在此数据中未宣布 Network 的弃用。

Save path

```text
digest_markdown/webplatform/Network/chrome-139-stable-en.md
```