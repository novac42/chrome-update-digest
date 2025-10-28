## 领域摘要

Chrome 139 为已编码的 WebRTC 音频帧添加了音量元数据暴露，允许开发者读取传输的已编码音频的逐帧响度。此更改通过 WebRTC encoded transform pipeline 和 `RTCEncodedAudioFrameMetadata` API 将已编码帧的音量暴露出来，提升了可观测性并允许在不解码的情况下基于音量实现功能。这对实时分析、语音活动检测和自适应用户体验有重要影响，同时将处理保留在已编码路径以提高性能。这些更新通过为点对点流中的音频遥测标准化低成本元数据通道，推进了 Web 平台的发展。

## 详细更新

下面是实现上述摘要的详细更改及其对多媒体工程师的实际影响。

### Audio level for RTC encoded frames（已编码 RTC 帧的音量）

#### 新增内容
为通过 RTCPeerConnection 传输并通过 WebRTC encoded transform API 展示的已编码音频帧暴露音量值，允许开发者访问逐帧响度元数据。

#### 技术细节
- 规范定义的元数据字段在 `RTCEncodedAudioFrameMetadata` 上作为 `audioLevel` 属性提供（参见规范链接）。
- 该功能在已编码帧的 encoded-transform pipeline 上运行，因此可以在不完全解码的情况下进行检查，与为分析音量而解码相比可降低 CPU 和延迟。
- 实现集成点：WebRTC encoded transform hooks 和 RTCPeerConnection 的已编码帧路径；与 codec-encoded payloads 及其相关元数据交互。

#### 适用场景
- 在会议 UI 中进行实时语音活动检测和出席指示，无需额外解码。
- 轻量级指标与分析管道，可在发送端/传输端聚合音量直方图或触发事件（例如静音建议、自动增益）。
- 使用音量元数据来优先考虑活跃发言者或触发码率/静音抑制策略的自适应用户体验或网络策略。
- 对于大规模部署的低开销监控以及无需增加解码成本的客户端音频可视化很有用。

#### 安全与隐私说明
- 音量是可能揭示语音活动模式的遥测数据；应视为潜在敏感信息，并遵循用户同意策略和本地隐私法规。
- 在将音量遥测发送到远程服务器时，请考虑 CSP/CORS 及应用层处理；确保适当的用户披露。

#### 参考资料
- [Tracking bug](https://issues.chromium.org/issues/418116079)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5206106602995712)
- [Link](https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-audiolevel)

Save to:
```text
digest_markdown/webplatform/Multimedia/chrome-139-stable-en.md
```