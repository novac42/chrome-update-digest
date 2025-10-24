# Chrome 支付领域摘要 – Chrome 135 稳定版

## 1. 领域摘要

Chrome 135 在支付领域引入了一项显著增强，重点在于简化 Web 应用的推送支付流程。主要内容是通过新的 HTML 链接关系，提升浏览器对待处理支付直接通知已注册支付客户端的支持。此更新使开发者能够打造更无缝、集成度更高的支付体验，减少用户操作阻力，加快交易流程。通过提升 Web 内容与支付处理程序之间的互操作性，Chrome 持续强化 Web 平台在安全高效数字支付方面的能力。

## 详细更新

以下是 Chrome 135 在支付领域引入的新功能的详细说明。

### Link `rel=facilitated-payment` to support push payments（支持推送支付的 Link）

#### 新增内容

Chrome 现已支持 `<link rel="facilitated-payment" href="...">` 元素，该元素作为浏览器通知已注册支付客户端有待处理推送支付的提示。

#### 技术细节

此功能允许 Web 开发者在 HTML 中包含 `<link rel="facilitated-payment" href="...">` 标签。当该标签存在时，浏览器会将其解释为发起推送支付的意图，并主动通知已注册此类事件的支付客户端。该机制利用 HTML DOM 和支付处理程序基础设施，使 Web 内容能够以更直接、标准化的方式触发支付流程。

#### 适用场景

- 电商网站可在用户进入结账页时，提示支付应用或钱包准备交易，减少操作步骤和等待时间。
- 金融服务提供商可提供更流畅的推送支付体验，提高转化率和用户满意度。
- 开发者受益于标准化、声明式的支付通知集成方式，无需编写自定义 JavaScript 逻辑。

#### 参考资料

- [跟踪 bug #1477049](https://issues.chromium.org/issues/1477049)
- [ChromeStatus.com 项目条目](https://chromestatus.com/feature/5198846820352000)