---
layout: default
title: chrome-141-zh
---

## 领域摘要

Chrome 141 的源站试验侧重于安全强化与能力探索：通过权限提示限制对本地网络的请求，并提供临时选择加入以便过渡；由 AI 支持的 Proofreader API；扩展 CSP `script-src`，引入基于哈希的允许列表；以及 WebAssembly 自定义描述符。影响最大的更新是本地网络访问的权限门控和更细粒度的脚本控制，而新 API 扩展了文本辅助与 Wasm 易用性。这些试验让团队在默认行为固化前进行测试、适配并反馈，在更强安全性与有针对性的选择加入式创新之间取得平衡，推动平台前进。

## 详细更新

以下是 Chrome 141 的源站试验，包含简要技术背景、面向开发者的用法与参考资料。

### Local network access restrictions（本地网络访问限制）

#### 新增内容
限制向用户本地网络发起请求的能力，并通过权限提示进行门控。该源站试验在临时基础上允许非安全上下文访问本地网络资源。

#### 技术细节
- 访问本地资源的网络请求受权限门控。
- 源站试验在一段时间内放宽此限制，使非安全上下文可访问。

#### 适用场景
- 在迁移与评估期间，从非安全上下文维持对本地网络的访问。
- 在适配权限门控的本地请求时收集反馈。

#### 参考资料
- [跟踪问题 #394009026](https://issues.chromium.org/issues/394009026)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5152728072060928)
- [规范](https://wicg.github.io/local-network-access)

### Proofreader API（校对 API）

#### 新增内容
用于对输入文本进行校对并给出建议更正的 JavaScript API，由 AI 语言模型提供支持。

#### 技术细节
- 暴露 JavaScript 接口以请求校对并接收建议。
- 通过源站试验提供。

#### 适用场景
- 在产品内为用户输入提供带建议的文本校对。

#### 参考资料
- [跟踪问题 #403313556](https://issues.chromium.org/issues/403313556)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5164677291835392)
- [规范](https://github.com/webmachinelearning/proofreader-api/blob/main/README.md#full-api-surface-in-web-idl)

### Extend CSP `script-src` (also known as `script-src-v2`)

#### 新增内容
为 `script-src` CSP 指令添加新关键字，引入两种基于哈希的允许列表机制：基于 URL 哈希的脚本来源，以及基于 `eval()` 和类 `eval()` 函数内容哈希的允许。

#### 技术细节
- 扩展 `script-src` 以支持基于 URL 哈希与基于 eval 内容哈希的允许列表。
- 有时称为“script-src-v2”。

#### 适用场景
- 通过 URL 哈希对脚本进行允许列表控制。
- 通过内容哈希允许 `eval()` 及类似内容。

#### 参考资料
- [跟踪问题 #392657736](https://issues.chromium.org/issues/392657736)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5196368819519488)
- [规范](https://github.com/w3c/webappsec-csp/pull/784)

### WebAssembly custom descriptors（WebAssembly 自定义描述符）

#### 新增内容
允许 WebAssembly 在新的“自定义描述符”对象中更高效地存储与源级类型关联的数据，并可为该类型的 WebAssembly 对象配置原型。由此可在 WebAssembly 对象的原型链上安装方法。

#### 技术细节
- 引入自定义描述符对象，以便将数据与源级类型关联。
- 支持为相应的 WebAssembly 对象配置原型。

#### 适用场景
- 通过原型附加特定类型的行为与方法。
- 更高效地处理与源级类型关联的数据。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6024844719947776)
- [规范](https://github.com/WebAssembly/custom-descriptors/blob/main/proposals/custom-descriptors/Overview.md)
