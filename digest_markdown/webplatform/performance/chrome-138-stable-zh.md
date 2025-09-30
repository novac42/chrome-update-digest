# 区域摘要

Chrome 138 (stable) 引入了针对预渲染和缓存控制的重点改进，直接影响页面加载策略和资源生命周期管理。最重要的更改允许开发者通过 Clear-Site-Data 清除 prefetch 和 prerender 缓存，并通过新的 target_hint 字段为导航推测提供更细粒度的提示。这些更新推动了 Web 平台发展，使网站能够对后台抓取/预渲染产生的工件进行确定性控制，并提高预渲染激活的准确性。之所以重要，是因为它们帮助团队在保持可预测的资源和隐私行为的同时优化感知性能。

## 详细更新

下面是 Chrome 138 中与上文摘要相关的 Performance 专项更改。

### Add prefetchCache and prerenderCache to Clear-Site-Data header（向 Clear-Site-Data 头添加 prefetchCache 和 prerenderCache）

#### 新增内容
Two new values for the Clear-Site-Data header let developers target clearing the prerender and prefetch caches: "prefetchCache" and "prerenderCache".

#### 技术细节
这些是 Clear Site Data 规范中定义的用于 Clear-Site-Data 头的附加缓存指令值。站点发送该头时，将指示浏览器清除指定的缓存（现在包括 prefetch 和 prerender 缓存），从而实现更精确的资源清理。

#### 适用场景
- 在身份验证更改或涉及隐私的操作后，使预抓取或预渲染的资源失效。
- 确保在重大状态更改后不会激活陈旧的预渲染页面。
- 为用于优化感知加载时间的激进 prefetch/prerender 策略提供更好的生命周期控制。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=398149359 — 跟踪问题 #398149359
- https://chromestatus.com/feature/5110263659667456 — ChromeStatus.com 条目
- https://w3c.github.io/webappsec-clear-site-data/#grammardef-cache-directive — 规范

### Speculation rules: target_hint field（用于指示激活目标的提示）

#### 新增内容
Speculation rules syntax is extended to allow a target_hint field that provides a hint indicating the target navigable where a prerendered page will eventually be activated (e.g., `_blank`).

#### 技术细节
target_hint 是 nav-speculation rules 语法中的仅提示指令。它向浏览器传达预期的激活目标，以便预渲染决策和激活路径能更好地与开发者意图对齐。

#### 适用场景
- 当链接预期在新的浏览上下文中打开（如 `_blank`）时，提高预渲染激活的准确性。
- 通过使 speculation rules 与预期的导航目标一致，减少浪费性的预渲染。
- 帮助开发者将预渲染与在特定目标或窗口中打开页面的 UI 模式协调起来。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40234240 — 跟踪问题 #40234240
- https://chromestatus.com/feature/5084493854924800 — ChromeStatus.com 条目
- https://wicg.github.io/nav-speculation/speculation-rules.html#speculation-rule-target-hint — 规范

已保存到：digest_markdown/webplatform/Performance/chrome-138-stable-en.md