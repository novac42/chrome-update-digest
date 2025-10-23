---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 141 稳定版通过引入 JavaScript Proofreader API，在浏览器中启用 AI 辅助的文本校对，推进端侧 AI。对开发者的主要影响是通过 Origin Trial 门控的能力：基于 AI 语言模型为输入文本提供更正建议。本次更新推动 Web 平台迈向可通过 Web API 访问的原生、标准化文本辅助原语。其价值在于让团队无需依赖临时性扩展或非标准集成即可探索集成的 AI 文本辅助。

## 详细更新

下面是 Chrome 141 稳定版中可用的端侧 AI 功能，并附其状态与规范的指引。

### Proofreader API（校对 API）

#### 新增内容
用于对输入文本进行校对并给出建议更正的 JavaScript API，基于 AI 语言模型。通过 Origin Trial 提供。

#### 技术细节
- API 表面在 Web IDL 中定义（参见规范）。
- 在 Chrome 141 稳定版中通过 Origin Trial 参与并启用。
- 开发通过所链接的跟踪缺陷和 ChromeStatus 条目进行追踪。

#### 适用场景
- 为用户输入的文本提供建议更正。
- 在 Web 编辑器和输入流程中集成 AI 辅助校对。

#### 参考资料
- [对输入文本进行校对并提供建议更正](/blog/proofreader-api-ot)
- [Origin Trial](/origintrials#/register_trial/1988902185437495297)
- [跟踪缺陷 #403313556](https://issues.chromium.org/issues/403313556)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5164677291835392)
- [规范](https://github.com/webmachinelearning/proofreader-api/blob/main/README.md#full-api-surface-in-web-idl)
