---
layout: default
title: chrome-142-zh
---

## 详细更新

以下条目扩展了摘要中的每项更改，说明技术约束、可能的集成点和开发者适用场景。

### FedCM—Support showing third-party iframe origins in the UI（在 UI 中显示第三方 iframe 来源）

#### 新增内容
FedCM 的 UI 现在可以显示第三方 iframe 的 origin，而不总是显示顶层站点。在嵌入 iframe 真正属于第三方时，这提高了表示的准确性。

#### 技术细节
在 Chrome 142 之前，FedCM 在其 UI 中始终显示顶层站点。此更新检测相关的凭据请求上下文是否为第三方 iframe，并在 FedCM 提示 UI 中暴露该 iframe 的 origin。

#### 适用场景
- 嵌入第三方身份流（例如，跨源认证框架）的站点可以向用户展示实际的 iframe origin，从而提高透明度和用户同意的质量。
- 帮助隐私/安全评审人员和 UX 设计师确保在联邦登录流程中正确显示 origin。

#### 参考资料
- [跟踪错误 #390581529](https://issues.chromium.org/issues/390581529)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5176474637959168)
- [规范](https://github.com/w3c-fedid/FedCM/pull/774)

### Stricter `*+json` MIME token validation for JSON modules（针对 JSON 模块的 MIME 验证更严格）

#### 新增内容
当与 `*+json` 匹配时，Chrome 会拒绝其类型或子类型包含非 HTTP token 代码点（例如空格）的 JSON 模块响应，这使行为与 MIME Sniffing 规范一致。

#### 技术细节
此更改在应用 `*+json` 匹配时强制要求 type/subtype 组件能被解析为有效的 HTTP token。该行为与 MIME Sniffing 规范中的算法一致，并作为 Interop2025 模块重点将 Chrome 与其他引擎对齐。

#### 适用场景
- 提供 JSON 模块的作者应确保 MIME 类型格式正确（无空格或无效 token 字符），以避免 fetch/模块被拒绝。
- 工具和服务器可以加强以发出合规的 MIME 类型，从而防止运行时模块加载失败。

#### 参考资料
- [跟踪错误 #440128360](https://issues.chromium.org/issues/440128360)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5182756304846848)
- [规范](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

### Web Speech API contextual biasing（上下文偏置）

#### 新增内容
网站可以添加和更新识别短语列表，以使语音识别模型偏向特定短语。

#### 技术细节
该 API 在 Web Speech API 的识别接口上暴露了短语列表机制，开发者可以提供上下文短语，底层模型在识别期间会更偏好这些短语。

#### 适用场景
- 面向语音的表单或命令，其中领域特定词汇能提高识别准确率。
- 动态更新短语列表以反映 UI 状态（例如当前播放列表名称或最近搜索词），以减少识别错误。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5225615177023488)
- [规范](https://webaudio.github.io/web-speech-api/#speechreco-phraselist)

### Media session: add reason to `enterpictureinpicture` action details（为 PiP 操作添加原因）

#### 新增内容
Media Session API 的 `enterpictureinpicture` 操作现在在其动作详情中包含 `enterPictureInPictureReason`，用于指示请求 PiP 的原因。

#### 技术细节
在发送到 `enterpictureinpicture` 操作的 MediaSessionActionDetails 中添加了 `enterPictureInPictureReason` 字段。这使得可以区分诸如显式用户操作（例如 UA 提供的按钮）与其他类型请求的触发来源。

#### 适用场景
- 播放器实现可以根据 PiP 是否由用户发起或由脚本/其他流程发起来调整 UI/行为。
- 分析和遥测可以将用户驱动的 PiP 与编程请求区分，以便更好地优化 UX。

#### 参考资料
- [跟踪错误 #446738067](https://issues.chromium.org/issues/446738067)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6415506970116096)
- [规范](https://github.com/w3c/mediasession/pull/362)

保存文件：digest_markdown/webplatform/Web API/chrome-142-stable-en.md
