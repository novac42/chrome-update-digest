```markdown
# Chrome 135 多媒体领域摘要

## 领域摘要

Chrome 135 在多媒体领域带来了显著增强，扩展了 Web Speech API 的能力。本次发布的核心主题是提升语音识别工作流中音频输入源的灵活性。对开发者影响最大的是，现在可以将任意 MediaStreamTrack 作为语音识别的输入，而不仅限于默认麦克风。这一进步使多媒体应用更加丰富和灵活，并使 Web 平台在音频处理方面更符合现代用户和开发者的期望。这些更新意义重大，因为它们为无障碍、媒体处理和 Web 实时通信等新场景提供了可能。

## 详细更新

本次发布聚焦于一项重要功能，拓宽了基于 Web 的语音识别输入选项，为开发者带来更大的控制力和集成可能性。

### Add MediaStreamTrack support to the Web Speech API（为 Web Speech API 增加 MediaStreamTrack 支持）

#### 新增内容
开发者现在可以将任意 MediaStreamTrack 作为 Web Speech API 的音频源，而不再局限于用户的默认麦克风。

#### 技术细节
此前，Web Speech API 仅支持从默认麦克风获取音频。此次更新后，开发者可以将 MediaStreamTrack（如屏幕捕获音频、远程对等连接音频或经过处理的音频流）直接传递给 API 进行语音识别。该功能通过扩展 API 的输入处理以接受 MediaStreamTrack 对象实现，与其他现代 Web 媒体 API 保持一致。

#### 适用场景
- 支持对屏幕录制或远程流音频进行语音识别。
- 在语音识别前应用自定义音频处理（如降噪、音效）。
- 支持音频源不是用户麦克风的无障碍场景。
- 集成到混合多路音频源的会议或协作应用中。

#### 参考资料
- [ChromeStatus.com 项目条目](https://chromestatus.com/feature/5178378197139456)
- [规范](https://wicg.github.io/speech-api)
```