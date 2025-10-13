# 领域摘要

Chrome 141 的性能更新聚焦于调优桌面端的导航推测行为，使 prefetch 和 prerender 的时机更贴近真实用户意图。主要更改细化了“eager”积极性等级：现在会在悬停时间短于“moderate”时触发，而不再与“immediate”相同。这样在链接悬停交互中，在响应性与何时开始推测性工作之间取得更细腻的平衡。对开发者而言，这意味着对 prefetch/prerender 的启动时机有更可预测、实用的控制，从而改善由悬停触发的导航的真实感知性能。

## 详细更新

此版本细化了桌面端中 speculation rules 将用户悬停意图转化为可执行 prefetch/prerender 时机的方式，更清晰地区分了不同积极性等级。

### Speculation rules: desktop "eager" eagerness improvements（桌面端“eager”积极性改进）

#### 新增内容
- 在桌面端，当用户悬停链接的时间短于“moderate”的悬停阈值时，“eager” speculation rules 现在会启动 prefetch 和 prerender。
- 之前，“eager”的行为与“immediate”相同，会尽早启动。

#### 技术细节
- “eager”的触发条件从“尽可能早”调整为一个悬停时长阈值，该阈值短于“moderate”。
- 这在“immediate”“eager”“moderate”之间形成了明确差异，使推测开始时机与桌面端的悬停意图更加贴合。

#### 适用场景
- 为悬停驱动的导航启用“更早但非即时”的推测操作，在保持与完全“immediate”行为区分的同时提升响应性。
- 为通过鼠标悬停交互的桌面用户提供 prefetch/prerender 启动时机的更精细控制。

#### 参考资料
- https://chromestatus.com/feature/5113430155591680
- https://wicg.github.io/nav-speculation/speculation-rules.html#:~:text=early%20as%20possible.-,%22moderate%22,balance%20between%20%22eager%22%20and%20%22conservative%22.,-%22conservative%22