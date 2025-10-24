# Chrome 135 HTML-DOM 更新领域摘要（稳定版）

## 领域摘要

Chrome 135 针对 HTML-DOM 层引入了有针对性的增强，重点提升无障碍性以及与现代网页支付流程的集成。本次发布的主要主题是声明式 UI 行为和简化的支付发起方式，这使开发者能够构建更易访问的界面，并更高效地集成支付生态系统。为按钮元素新增的属性以及对支付相关链接关系的支持，代表了迈向更健壮、互操作性更强且更易用的 Web 平台的重要一步。这些更新意义重大，因为它们减少了对自定义脚本的需求，促进了最佳实践，并为 Web 应用带来了更丰富的浏览器原生能力。

## 详细更新

本次发布为 HTML-DOM 领域带来了两项值得关注的功能，均旨在通过原生浏览器支持简化开发并提升用户体验。

### Invoker Commands; the command and commandfor attributes（命令调用者；command 和 commandfor 属性）

#### 新增内容
`<button>` 元素上的 `command` 和 `commandfor` 属性允许开发者以声明方式为按钮分配行为，从而提升无障碍性并减少对 JavaScript 事件处理器的依赖。

#### 技术细节
通过指定 `command` 和 `commandfor` 属性，按钮可以直接关联到特定操作或元素，使浏览器能够原生处理激活逻辑。这种方式符合 HTML 规范，确保了跨浏览器的一致行为，同时也便于辅助技术理解按钮的用途。

#### 适用场景
- 创建无需自定义脚本的无障碍工具栏或对话框控件
- 为交互元素确保一致的键盘和辅助技术支持
- 简化复杂 UI 组件的标记结构

#### 参考资料
- [跟踪 bug #1490919](https://issues.chromium.org/issues/1490919)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5142517058371584)
- [规范](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-commandfor)

### Link `rel=facilitated-payment` to support push payments（Link `rel=facilitated-payment` 支持推送支付）

#### 新增内容
对 `<link rel="facilitated-payment" href="...">` 的支持，使网页能够标示待处理的推送支付，允许浏览器通知已注册的支付客户端。

#### 技术细节
当页面包含 `<link rel="facilitated-payment">` 时，浏览器会将其视为提示，调用能够处理推送支付的支付处理程序。该机制利用 HTML link 元素，并与 Payment Handler API 集成，实现了直接从 DOM 发起支付流程的简化方式。

#### 适用场景
- 电商网站提示用户通过已注册的支付应用完成支付
- 利用浏览器原生支付通知，减少结账流程中的阻力
- 实现与第三方支付提供商的无缝集成

#### 参考资料
- [跟踪 bug #1477049](https://issues.chromium.org/issues/1477049)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5198846820352000)