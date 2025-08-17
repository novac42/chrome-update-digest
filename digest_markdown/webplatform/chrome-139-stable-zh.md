---
layout: default
title: Chrome 139 全领域更新分析（Stable）
---

```markdown
# Chrome 139 全领域更新分析（Stable）

---

## 1. 执行摘要

Chrome 139 带来了 Web 平台在 CSS、WebGPU、Web API、安全隐私、性能、设备支持、PWA、WebAssembly 及弃用领域的多项重要更新。此次版本聚焦于 CSS 现代化（如 corner-shape、custom functions）、WebGPU 兼容性与核心能力提升、Web API 扩展（如 Prompt API、extendedLifetime SharedWorker）、安全隐私强化（如 Accept-Language 指纹缩减、window.name 清理）、性能优化（如 soft-navigation 性能指标、Android 后台冻结加速）以及一系列弃用和兼容性调整。开发者需关注新特性带来的能力提升，同时注意弃用项和安全模型变化对现有实现的影响。

---

## 2. 关键影响

#### 技术影响

- **现有实现影响**：部分弃用（如 macOS 11 支持、Purpose: prefetch header、ISO-2022-JP 自动检测）需及时调整兼容策略。window.name、Accept-Language 等隐私相关变更可能影响跨站点数据流和追踪逻辑。
- **新功能可用性**：CSS corner-shape、custom functions、WebGPU compatibility mode、Prompt API、on-device Web Speech API、extendedLifetime SharedWorker、soft-navigation 性能指标等为开发者带来更强的表现力和性能优化空间。
- **技术债务考虑**：弃用项和安全策略调整需提前排查依赖，及时迁移和适配，避免未来版本中断或安全风险。

---

## 3. 风险评估

**关键风险**：

- 破坏性更改：macOS 11 停止支持、ISO-2022-JP 自动检测移除、Purpose: prefetch header 弃用，可能导致旧系统或依赖相关特性的应用无法正常运行。
- 安全考虑：window.name 清理、Accept-Language 指纹缩减、CSP worker 错误事件规范化，提升安全性但可能影响部分依赖旧行为的业务逻辑。

**中等风险**：

- 弃用：Purpose: prefetch header、macOS 11、ISO-2022-JP 自动检测，需关注兼容性和用户体验。
- 性能影响：Android 后台冻结加速、full-frame-rate render blocking、WebXR depth sensing 性能提升，需评估对现有性能监控和资源调度的影响。

---

## 4. 建议行动

#### 立即行动

- 检查并适配 macOS 11 停止支持、Purpose: prefetch header、ISO-2022-JP 自动检测移除等弃用项。
- 审查 window.name、Accept-Language、CSP worker 行为变更对业务逻辑和安全策略的影响。
- 评估并试用 CSS 新特性（如 corner-shape、custom functions）、WebGPU compatibility mode、Prompt API、on-device Web Speech API 等新能力。

#### 短期规划

- 跟进 WebGPU、WebXR、Web API 相关新特性和性能指标，优化前端架构和用户体验。
- 监控弃用项的后续影响，逐步迁移依赖旧特性的代码。
- 关注安全隐私策略变化，完善数据流和追踪合规性。

#### 长期战略

- 持续关注 WebGPU、WebAssembly、PWA、AI API 等前沿能力，规划技术升级和创新应用。
- 建立自动化兼容性检测和安全审计流程，降低未来平台变更带来的风险。
- 推动团队对 CSS、Web API、性能优化等新规范的学习和实践。

---

## 5. 功能分析

### Short-circuiting `var()` and `attr()`

**影响级别**：🟡 重要

**变更内容**：
`var()` 和 `attr()` 在未使用 fallback 时，不再检查 fallback 是否存在循环引用，从而提升性能和一致性。

**重要性**：
优化 CSS 变量和属性函数的性能，减少不必要的循环检测，提升渲染效率。

**实施指南**：
- 可放心使用 `var()` 和 `attr()`，无需担心 fallback 未用时的循环引用性能损耗。
- 检查依赖复杂 CSS 变量链的场景，确保行为符合预期。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/6212939656462336)

---

### Support `font-feature-settings` descriptor in `@font-face` rule

**影响级别**：🟡 重要

**变更内容**：
`@font-face` 规则支持 string-based 语法的 `font-feature-settings`，无效或未识别的 feature tag 将被忽略。

**重要性**：
提升 OpenType 字体特性控制能力，增强排版灵活性，符合 CSS Fonts Level 4 规范。

**实施指南**：
- 推荐在 `@font-face` 中使用标准 `font-feature-settings` 字符串语法。
- 避免使用非标准或二进制形式。

**参考资料**：
[Tracking bug #40398871](https://issues.chromium.org/issues/40398871) | [ChromeStatus.com entry](https://chromestatus.com/feature/5102801981800448) | [Spec](https://www.w3.org/TR/css-fonts-4/#font-rend-desc)

---

### CSS custom functions

**影响级别**：🔴 关键

**变更内容**：
引入 CSS custom functions，可基于参数、条件和其他自定义属性动态返回值，提升样式表达力。

**重要性**：
极大增强 CSS 动态性和复用性，为复杂主题和组件库开发提供新范式。

**实施指南**：
- 探索使用 custom functions 替代部分 JS 动态样式逻辑。
- 关注规范和兼容性进展，逐步引入到样式体系。

**参考资料**：
[Tracking bug #325504770](https://issues.chromium.org/issues/325504770) | [ChromeStatus.com entry](https://chromestatus.com/feature/5179721933651968) | [Spec](https://drafts.csswg.org/css-mixins-1/#defining-custom-functions)

---

### Continue running transitions when switching to initial transition value

**影响级别**：🟡 重要

**变更内容**：
transition 相关属性变更时，仅影响新启动的 transition，已激活的 transition 动画将继续运行，行为与 Safari、Firefox 保持一致。

**重要性**：
提升跨浏览器一致性，避免 transition 被意外中断。

**实施指南**：
- 检查依赖 transition 动画的交互，确保动画不会被 transition 属性变更意外终止。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/5194501932711936) | [Spec](https://www.w3.org/TR/css-transitions-1/#starting)

---

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)

**影响级别**：🔴 关键

**变更内容**：
支持 `corner-shape`、`superellipse`、`squircle` 等新属性，实现更丰富的角样式和动画。

**重要性**：
极大提升 UI 设计表现力，支持现代流行的圆角、凹口、squircle 等形状。

**实施指南**：
- 在设计系统和组件库中引入 `corner-shape`，实现更具辨识度的界面风格。
- 结合动画实现角形态的动态过渡。

**参考资料**：
[Tracking bug #393145930](https://issues.chromium.org/issues/393145930) | [ChromeStatus.com entry](https://chromestatus.com/feature/5357329815699456) | [Spec](https://drafts.csswg.org/css-borders-4/#corner-shaping)

---

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

**影响级别**：🟡 重要

**变更内容**：
新增 `font-width` 属性，`font-stretch` 成为 legacy alias，与规范和其他浏览器保持一致。

**重要性**：
提升字体宽度控制的标准化和兼容性。

**实施指南**：
- 推荐使用 `font-width`，逐步淘汰 `font-stretch`。

**参考资料**：
[Tracking bug #356670472](https://issues.chromium.org/issues/356670472) | [ChromeStatus.com entry](https://chromestatus.com/feature/5190141555245056)

---

### Support async attribute for SVG `<script>` element

**影响级别**：🟡 重要

**变更内容**：
SVG `<script>` 元素支持 `async` 属性，实现异步脚本加载与执行。

**重要性**：
提升 SVG 应用性能和响应速度，增强与 HTML `<script>` 行为一致性。

**实施指南**：
- 在 SVG 中使用 `async` 优化脚本加载。
- 检查依赖 SVG 脚本执行顺序的逻辑。

**参考资料**：
[Tracking bug #40067618](https://issues.chromium.org/issues/40067618) | [ChromeStatus.com entry](https://chromestatus.com/feature/6114615389585408) | [Spec](https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A)

---

### The `request-close` invoker command

**影响级别**：🟡 重要

**变更内容**：
为 declarative invoker commands API 增加 `request-close` 命令，统一对话框关闭行为。

**重要性**：
提升对话框交互的可控性和一致性，便于拦截和处理关闭事件。

**实施指南**：
- 使用 `request-close` 统一处理对话框关闭逻辑。
- 结合 cancel 事件实现自定义关闭拦截。

**参考资料**：
[Tracking bug #400647849](https://issues.chromium.org/issues/400647849) | [ChromeStatus.com entry](https://chromestatus.com/feature/5592399713402880) | [Spec](https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state)

---

### Scroll anchoring priority candidate fix

**影响级别**：🟡 重要

**变更内容**：
优化 scroll anchoring 算法，优先选择最深的可见元素作为 anchor，提升滚动体验。

**重要性**：
减少滚动跳动，提升页面稳定性。

**实施指南**：
- 检查依赖 scroll anchoring 的页面布局，确保滚动行为符合预期。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/5070370113323008)

---

### WebXR depth sensing performance improvements

**影响级别**：🟡 重要

**变更内容**：
WebXR depth sensing 支持自定义深度缓冲区行为，提升性能和灵活性。

**重要性**：
增强 XR 应用的实时性和资源利用效率。

**实施指南**：
- 在 XR 应用中根据场景选择 raw/smooth depth buffer。
- 利用新 API 优化深度数据处理。

**参考资料**：
[Tracking bug #410607163](https://issues.chromium.org/issues/410607163) | [ChromeStatus.com entry](https://chromestatus.com/feature/5074096916004864) | [Spec](https://immersive-web.github.io/depth-sensing)

---

### Allow more characters in JavaScript DOM APIs

**影响级别**：🟡 重要

**变更内容**：
JavaScript DOM API 创建元素和属性时，字符校验放宽，与 HTML 解析器一致。

**重要性**：
提升一致性，减少因字符限制导致的兼容性问题。

**实施指南**：
- 可放心使用更广泛的字符集创建 DOM 元素和属性。

**参考资料**：
[Tracking bug #40228234](https://issues.chromium.org/issues/40228234) | [ChromeStatus.com entry](https://chromestatus.com/feature/6278918763708416) | [Spec](https://dom.spec.whatwg.org/#namespaces)

---

### WebGPU: 3D texture support for BC and ASTC compressed formats

**影响级别**：🟡 重要

**变更内容**：
WebGPU 支持 BC 和 ASTC 压缩格式的 3D 纹理。

**重要性**：
提升 3D 图形渲染效率，支持更多高质量纹理格式。

**实施指南**：
- 在 WebGPU 应用中使用新格式提升渲染质量和性能。

**参考资料**：
[Tracking bug #342840940](https://issues.chromium.org/issues/342840940) | [ChromeStatus.com entry](https://chromestatus.com/feature/5080855386783744) | [Spec](https://gpuweb.github.io/gpuweb/#texture-compression-bc-sliced-3d)

---

### Detailed WebGPU Updates

**影响级别**：🟢 可选

**变更内容**：
WebGPU 相关详细更新，涵盖开发者博客和官方文档。

**重要性**：
便于开发者获取最新 WebGPU 生态和最佳实践。

**实施指南**：
- 关注官方博客和文档，及时了解 WebGPU 进展。

**参考资料**：
[Chrome for Developers](https://developer.chrome.com/) | [Blog](https://developer.chrome.com/blog)

---

### Enable the feature

**影响级别**：🟢 可选

**变更内容**：
WebGPU compatibility mode 可通过实验性功能或 origin trial 启用。

**重要性**：
便于开发者提前适配和测试兼容模式。

**实施指南**：
- 在开发环境开启实验性功能，参与 origin trial 进行线上测试。

**参考资料**：
[WebGPU compatibility mode](https://chromestatus.com/feature/6436406437871616)

---

### The `securePaymentConfirmationAvailability` API

**影响级别**：🟡 重要

**变更内容**：
新增 API 检查 Secure Payment Confirmation (SPC) 是否可用，简化支付流程判断。

**重要性**：
提升支付流程用户体验和开发效率。

**实施指南**：
- 在支付流程前使用该 API 判断 SPC 可用性，优化分支逻辑。

**参考资料**：
[Tracking bug #40258712](https://issues.chromium.org/issues/40258712) | [ChromeStatus.com entry](https://chromestatus.com/feature/5165040614768640) | [Spec](https://github.com/w3c/secure-payment-confirmation/pull/285)

---

### Secure Payment Confirmation: Browser Bound Keys

**影响级别**：🟡 重要

**变更内容**：
SPC 增加浏览器绑定密钥，私钥不跨设备同步，满足支付设备绑定要求。

**重要性**：
提升支付安全性，满足合规需求。

**实施指南**：
- 检查支付流程对密钥管理的依赖，确保兼容新安全策略。

**参考资料**：
[Tracking bug #377278827](https://issues.chromium.org/issues/377278827) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106102997614592) | [Spec](https://w3c.github.io/secure-payment-confirmation/#sctn-browser-bound-key-store)

---

### On-device Web Speech API

**影响级别**：🔴 关键

**变更内容**：
Web Speech API 支持本地语音识别，音频和转录数据无需上传第三方服务。

**重要性**：
极大提升隐私保护和响应速度，适用于对数据敏感的场景。

**实施指南**：
- 优先使用 on-device 模式，提升语音应用隐私和性能。
- 检查多语言和资源安装提示逻辑。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/6090916291674112) | [Spec](https://webaudio.github.io/web-speech-api)

---

### Clear window name for cross-site navigations that switches browsing context group

**影响级别**：🔴 关键

**变更内容**：
跨站点切换 browsing context group 时清空 `window.name`，防止信息泄露和追踪。

**重要性**：
强化隐私保护，减少跨站点追踪风险。

**实施指南**：
- 检查依赖 `window.name` 跨站传递数据的逻辑，及时迁移到更安全的方案。

**参考资料**：
[Tracking bug #1090128](https://issues.chromium.org/issues/1090128) | [ChromeStatus.com entry](https://chromestatus.com/feature/5962406356320256) | [Spec](https://html.spec.whatwg.org/multipage/browsing-the-web.html#resetBCName)

---

### Reduce fingerprinting in Accept-Language header information

**影响级别**：🔴 关键

**变更内容**：
`Accept-Language` header 仅发送首选语言，减少指纹信息暴露。

**重要性**：
显著提升用户隐私，降低被追踪风险。

**实施指南**：
- 检查依赖多语言 header 的后端逻辑，确保兼容单一语言场景。

**参考资料**：
[Tracking bug #1306905](https://issues.chromium.org/issues/1306905) | [ChromeStatus.com entry](https://chromestatus.com/feature/5188040623390720)

---

### Randomize TCP port allocation on Windows

**影响级别**：🟡 重要

**变更内容**：
Windows 平台 TCP 端口分配采用随机化，提升安全性，减少端口重用攻击风险。

**重要性**：
增强网络安全，降低端口预测攻击可能。

**实施指南**：
- 关注网络服务端口分配策略，评估对现有连接管理的影响。

**参考资料**：
[Tracking bug #40744069](https://issues.chromium.org/issues/40744069) | [ChromeStatus.com entry](https://chromestatus.com/feature/5106900286570496)

---

### Faster background freezing on Android

**影响级别**：🟡 重要

**变更内容**：
Android 后台页面冻结时间从 5 分钟缩短至 1 分钟。

**重要性**：
提升移动端资源利用率，减少后台耗电。

**实施指南**：
- 检查依赖后台长时间运行的逻辑，优化任务调度。

**参考资料**：
[Tracking bug #435623337](https://issues.chromium.org/issues/435623337) | [ChromeStatus.com entry](https://chromestatus.com/feature/5386725031149568)

---

### Fire error event for Content Security Policy (CSP) blocked worker

**影响级别**：🟡 重要

**变更内容**：
CSP 阻止 worker 时，异步触发 error 事件而非抛出异常，符合规范。

**重要性**：
提升安全一致性，便于统一错误处理。

**实施指南**：
- 检查 worker 创建异常处理逻辑，适配 error 事件。

**参考资料**：
[Tracking bug #41285169](https://issues.chromium.org/issues/41285169) | [ChromeStatus.com entry](https://chromestatus.com/feature/5177205656911872) | [Spec](https://www.w3.org/TR/CSP3/#fetch-integration)

---

### Audio level for RTC encoded frames

**影响级别**：🟢 可选

**变更内容**：
WebRTC encoded transform 可获取编码帧的音频电平。

**重要性**：
便于音频流质量监控和自适应处理。

**实施指南**：
- 在实时通信应用中利用该特性优化音量检测和反馈。

**参考资料**：
[Tracking bug #418116079](https://issues.chromium.org/issues/418116079) | [ChromeStatus.com entry](https://chromestatus.com/feature/5206106602995712) | [Spec](https://w3c.github.io/webrtc-encoded-transform/#dom-rtcencodedaudioframemetadata-audiolevel)

---

### Web app scope extensions

**影响级别**：🟡 重要

**变更内容**：
Web app manifest 支持 `scope_extensions` 字段，可扩展应用作用域至其他域名。

**重要性**：
便于多域名统一为单一 Web 应用，提升用户体验。

**实施指南**：
- 配置 `.well-known/web-app-origin-association` 文件，确保域名关联。

**参考资料**：
[Tracking bug #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011) | [ChromeStatus.com entry](https://chromestatus.com/feature/5746537956114432) | [Spec](https://github.com/WICG/manifest-incubations/pull/113)

---

### Specification-compliant JSON MIME type detection

**影响级别**：🟡 重要

**变更内容**：
JSON MIME type 检测符合 WHATWG mimesniff 规范，支持 `+json` 子类型。

**重要性**：
提升 API 兼容性，减少因 MIME type 检测不一致导致的问题。

**实施指南**：
- 后端返回 JSON 时确保 MIME type 合规。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528) | [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

---

### WebGPU `core-features-and-limits`

**影响级别**：🟡 重要

**变更内容**：
WebGPU adapter/device 支持核心特性和限制，符合规范。

**重要性**：
便于开发者判断设备能力，提升跨平台一致性。

**实施指南**：
- 检查 WebGPU 应用对核心特性的依赖，提升兼容性。

**参考资料**：
[Tracking bug #418025721](https://issues.chromium.org/issues/418025721) | [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496) | [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

---

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports

**影响级别**：🟡 重要

**变更内容**：
Crash Reporting API 支持指定 `crash-reporting` endpoint，仅接收崩溃报告。

**重要性**：
便于分流和专门处理崩溃数据。

**实施指南**：
- 配置专用 endpoint 接收崩溃报告，优化监控体系。

**参考资料**：
[Tracking bug #414723480](https://issues.chromium.org/issues/414723480) | [ChromeStatus.com entry](https://chromestatus.com/feature/5129218731802624) | [Spec](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)

---

### Prompt API

**影响级别**：🔴 关键

**变更内容**：
引入 Prompt API，支持文本、图片、音频等多模态 AI 交互，支持结构化输出和 Chrome 扩展集成。

**重要性**：
为 Web 应用带来原生 AI 能力，极大拓展创新场景。

**实施指南**：
- 参与 origin trial，探索 AI 驱动的 Web 应用新模式。
- 关注企业策略对模型下载的影响。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/2533837740349325313) | [Tracking bug #417530643](https://issues.chromium.org/issues/417530643) | [ChromeStatus.com entry](https://chromestatus.com/feature/5134603979063296)

---

### Extended lifetime shared workers

**影响级别**：🟡 重要

**变更内容**：
`SharedWorker` 构造器新增 `extendedLifetime: true`，可在无客户端时保持 worker 存活。

**重要性**：
便于实现复杂异步任务，无需依赖 service worker。

**实施指南**：
- 参与 origin trial，评估异步任务场景下的应用价值。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3056255297124302849) | [Tracking bug #400473072](https://issues.chromium.org/issues/400473072) | [ChromeStatus.com entry](https://chromestatus.com/feature/5138641357373440)

---

### `SoftNavigation` performance entry

**影响级别**：🟡 重要

**变更内容**：
暴露 soft navigation 性能指标，包括 `soft-navigation` 和 `interaction-contentful-paint`。

**重要性**：
便于监控 SPA/MPA 软导航性能，提升用户体验。

**实施指南**：
- 参与 origin trial，集成新性能指标到监控体系。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials#/view_trial/21392098230009857) | [Tracking bug #1338390](https://issues.chromium.org/issues/1338390) | [ChromeStatus.com entry](https://chromestatus.com/feature/5144837209194496) | [Spec](https://wicg.github.io/soft-navigations)

---

### Web Authentication immediate mediation

**影响级别**：🟡 重要

**变更内容**：
`navigator.credentials.get()` 支持 immediate mediation，若有可用凭据立即弹窗，否则直接拒绝。

**重要性**：
优化登录流程，提升用户体验。

**实施指南**：
- 在认证流程中利用 immediate mediation 提升自动化和交互效率。

**参考资料**：
[Tracking bug #408002783](https://issues.chromium.org/issues/408002783) | [ChromeStatus.com entry](https://chromestatus.com/feature/5164322780872704) | [Spec](https://github.com/w3c/webauthn/pull/2291)

---

### Full frame rate render blocking attribute

**影响级别**：🟡 重要

**变更内容**：
新增 full-frame-rate render blocking token，阻塞渲染时降低帧率，为加载保留更多资源。

**重要性**：
提升页面加载性能，优化资源分配。

**实施指南**：
- 参与 origin trial，评估对复杂页面加载性能的提升效果。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/3578672853899280385) | [Tracking bug #397832388](https://issues.chromium.org/issues/397832388) | [ChromeStatus.com entry](https://chromestatus.com/feature/5207202081800192)

---

### WebGPU compatibility mode

**影响级别**：🔴 关键

**变更内容**：
WebGPU compatibility mode 支持 OpenGL、Direct3D11 等旧图形 API，扩展 WebGPU 应用覆盖面。

**重要性**：
极大提升 WebGPU 应用的设备兼容性，降低硬件门槛。

**实施指南**：
- 参与 origin trial，测试兼容模式下的应用表现。
- 关注兼容性约束，优化跨平台体验。

**参考资料**：
[Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/1489002626799370241) | [Tracking bug #40266903](https://issues.chromium.org/issues/40266903) | [ChromeStatus.com entry](https://chromestatus.com/feature/6436406437871616) | [Spec](https://github.com/gpuweb/gpuweb/blob/main/proposals/compatibility-mode.md)

---

### Stop sending Purpose: prefetch header from prefetches and prerenders

**影响级别**：🟡 重要

**变更内容**：
prefetch/prerender 不再发送 Purpose: prefetch header，改用 Sec-Purpose，逐步移除旧 header。

**重要性**：
提升规范一致性，减少冗余 header。

**实施指南**：
- 检查后端对 Purpose: prefetch header 的依赖，及时切换到 Sec-Purpose。

**参考资料**：
[Tracking bug #420724819](https://issues.chromium.org/issues/420724819) | [ChromeStatus.com entry](https://chromestatus.com/feature/5088012836536320) | [Spec](https://wicg.github.io/nav-speculation/prerendering.html#interaction-with-fetch)

---

### Remove support for macOS 11

**影响级别**：🔴 关键

**变更内容**：
Chrome 139 起不再支持 macOS 11，需升级至 macOS 12+。

**重要性**：
影响所有 macOS 11 用户，需及时升级系统或调整支持策略。

**实施指南**：
- 通知用户和 IT 部门升级 macOS。
- 检查自动化测试和部署环境的系统版本。

**参考资料**：
[ChromeStatus.com entry](https://chromestatus.com/feature/4504090090143744)

---

### Remove auto-detection of `ISO-2022-JP` charset in HTML

**影响级别**：🟡 重要

**变更内容**：
移除 HTML 中对 `ISO-2022-JP` 字符集的自动检测，提升安全性。

**重要性**：
减少安全风险，提升与 Safari 等浏览器一致性。

**实施指南**：
- 检查是否有依赖该自动检测的旧内容，及时调整编码声明。

**参考资料**：
[known security issues](https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/) | [Tracking bug #40089450](https://issues.chromium.org/issues/40089450) | [ChromeStatus.com entry](https://chromestatus.com/feature/6576566521561088) | [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/) | [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0) | [Google Developers Site Policies](https://developers.google.com/site-policies)

---
```
