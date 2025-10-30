## 领域摘要

Chrome 142 通过在匹配 `*+json` 时强制更严格的 MIME 令牌规则，收紧了对 JSON 模块导入的校验。此更改会拒绝 MIME 类型的 type 或 subtype 包含非 HTTP 令牌代码点（例如空格）的 JSON 模块脚本响应，从而改善与其他引擎的互操作性并使 Chrome 与 MIME Sniffing 规范保持一致。对开发者而言，最显著的影响是，配置错误的服务器发送格式不正确的 MIME 类型将导致 JSON 模块导入失败，促使修复服务器头。总体上，这提升了平台一致性并减少了模块加载行为的歧义。

## 详细更新

本节将摘要扩展为面向 JavaScript 开发者和平台工程师的可操作细节。

### Stricter `*+json` MIME token validation for JSON modules（针对 JSON 模块的 `*+json` MIME 令牌更严格校验）

#### 新增内容
Chrome 现在在匹配 `*+json` 时，如果 MIME 类型的 type 或 subtype 包含非 HTTP 令牌代码点，就会拒绝作为 JSON 模块脚本的响应。这使得 JSON 模块的 MIME 处理更严格并符合规范。

#### 技术细节
在匹配 `*+json` 模式时，浏览器会验证 type 和 subtype 是否由有效的 HTTP 令牌代码点组成。如果任一部分包含无效字符（例如空格），响应将被视为 JSON 模块脚本时拒绝。此行为遵循 MIME Sniffing 规范，并使 Chrome 在 Interop2025 modules 计划下与其他引擎保持一致。

#### 适用场景
- 通过拒绝格式错误的 MIME 类型，确保跨浏览器的一致模块导入行为。  
- 有助于及早暴露服务器配置错误：开发者应确保服务器的 `Content-Type` 头在 type/subtype 中使用有效的令牌字符。  
- 提高交付 JSON 模块的系统的安全性和互操作性。

#### 参考资料
- [跟踪错误 #440128360](https://issues.chromium.org/issues/440128360)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5182756304846848)  
- [MIME Sniffing 规范](https://mimesniff.spec.whatwg.org/#parse-a-mime-type)

保存为： digest_markdown/webplatform/JavaScript/chrome-142-stable-en.md