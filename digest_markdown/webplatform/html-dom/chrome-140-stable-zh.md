## 区域摘要

Chrome 140 引入了一个小而集中的 HTML‑DOM 增强：在 `ToggleEvent` 接口上新增了一个 `source` 属性。该属性在适用时揭示触发 `ToggleEvent` 的元素，为处理器提供更丰富的事件上下文。对于开发者而言，此更改使得识别发起元素（例如打开 popover 的按钮）更容易，而无需自定义 DOM 遍历或额外属性。通过让内置 DOM 事件更具信息性并减少交互组件的样板代码，这项改进推进了平台发展。

## 详细更新

下面的单一更新直接支持上述摘要。

### `ToggleEvent` source attribute（source 属性）

#### 新增内容
`ToggleEvent` 的 `source` 属性包含触发该 `ToggleEvent` 被派发的元素（如适用）。

#### 技术细节
这为 `ToggleEvent` DOM 接口添加了一个可访问的属性，当存在触发元素时引用该元素。发布说明通过一个示例说明了该行为，该示例涉及通过诸如 `popovertarget` 或 `commandfor` 之类的属性由 `<button>` 元素打开弹出面板的情形。

#### 适用场景
- 弹出面板或可切换 UI 的事件处理器可以检查 `event.source` 以确定哪个控件发起了切换。
- 简化需要区分用户触发的切换与编程触发切换的组件逻辑。
- 减少对基于属性的关联或手动查找元素来定位发起元素的依赖。

#### 参考资料
- https://chromestatus.com/feature/5165304401100800
- https://html.spec.whatwg.org/multipage/interaction.html#the-toggleevent-interface

## 区域专门知识 (HTML-DOM)

- css: 对布局的直接影响最小；在不增加额外 DOM 标记的情况下，便于在控件与被切换的 UI 之间建立更清晰的关联。
- webapi: 通过在 `ToggleEvent` 上添加 `source` 属性扩展了 DOM 事件 API。
- graphics-webgpu: 与 GPU 或 渲染管线 无直接关联。
- javascript: V8 使用者可以在 `ToggleEvent` 处理器中读取 `event.source` 以简化控制流。
- security-privacy: 在事件对象中暴露了元素引用；标准的 same-origin 和 DOM 访问规则继续适用。
- performance: 开销低；在常见的切换处理路径中避免了额外的 DOM 查询。
- multimedia: 与编解码器/流媒体无关。
- devices: 无直接设备 API 影响。
- pwa-service-worker: 对 service worker 行为无直接影响。
- webassembly: 对 WASM 运行时无直接影响。
- deprecations: 未报告任何弃用影响。 

已保存到：digest_markdown/webplatform/HTML-DOM/chrome-140-stable-en.md