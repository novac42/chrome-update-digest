## 领域摘要

Chrome 139 通过添加富表现力的形状控制、改进的字体处理和更健全的值求值语义来继续推进 CSS。面向开发者的关键更改包括 corner shaping (superellipse/squircle)、CSS custom functions，以及改进的字体描述符（`font-width` 和 `@font-face` 的 `font-feature-settings`）。这些更新使视觉设计和排版更可预测且更强大，而较小的修复（`var()`/`attr()` 短路、过渡延续、滚动锚定）则减少了边缘案例故障。总体而言，它们推动平台朝向更丰富、对动画友好且符合规范的样式原语发展。

## 详细更新

下面的列表对上文摘要进行了扩展，提供每个 Chrome 139 中 CSS 领域功能的简明、面向开发者的说明。

### Short-circuiting `var()` and `attr()`

#### 新增内容
当未采用回退值时，`var()` 和 `attr()` 在评估该回退值时不会扫描循环。

#### 技术细节
评估会更早短路，从而在直接使用回退值时避免不必要的循环检测。

#### 适用场景
减少意外的循环错误并提高基于自定义属性和属性值的可靠性。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/6212939656462336

### Support `font-feature-settings` descriptor in `@font-face` rule

#### 新增内容
根据 CSS Fonts Level 4，在 `@font-face` 内添加了对基于字符串的 `font-feature-settings` 描述符的支持。

#### 技术细节
接受字符串语法；按规范，非法/未识别的 OpenType 特性标签将被忽略。不支持非标准或二进制形式。

#### 适用场景
允许字体作者和开发者在 `@font-face` 加载时声明 OpenType 特性偏好，改进排版控制。

#### 参考资料
- 跟踪 bug #40398871: https://issues.chromium.org/issues/40398871
- ChromeStatus.com 条目: https://chromestatus.com/feature/5102801981800448
- 规范: https://www.w3.org/TR/css-fonts-4/#font-rend-desc

### CSS custom functions

#### 新增内容
引入自定义函数，可从自定义属性、参数和条件计算值（类似 mixin 的行为）。

#### 技术细节
自定义函数遵循 CSS mixins/custom functions 草案，并在 Chromium 中跟踪。

#### 适用场景
在无需 JS 的情况下，为复杂主题和组件库提供可复用、参数化的样式逻辑。

#### 参考资料
- 跟踪 bug #325504770: https://issues.chromium.org/issues/325504770
- ChromeStatus.com 条目: https://chromestatus.com/feature/5179721933651968
- 规范草案: https://drafts.csswg.org/css-mixins-1/#defining-custom-functions

### Continue running transitions when switching to initial transition value

#### 新增内容
即使 `transition-*` 属性更改为初始值，活动过渡仍会继续先前的动画状态。

#### 技术细节
过渡属性的更改仅影响新启动的过渡；根据规范，现有的活动过渡将保留其先前参数。

#### 适用场景
避免在切换过渡定义时出现突兀的动画中断，改善动态样式更改期间的动画稳定性。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5194501932711936
- 规范: https://www.w3.org/TR/css-transitions-1/#starting

### Corner shaping (`corner-shape`, `superellipse`, `squircle`)（角部成形）

#### 新增内容
添加了角部成形原语，可将角曲率表达为超椭圆，使得可以实现 squircle、凹口、挖槽以及角形的动画变形。

#### 技术细节
新属性接受形状描述（superellipse 参数）并与现有的边框/角模型集成，以渲染非圆形角。

#### 适用场景
创建更平滑、由设计驱动的角部，并在无需复杂 SVG 或遮罩解决方案的情况下实现角形之间的动画过渡。

#### 参考资料
- 跟踪 bug #393145930: https://issues.chromium.org/issues/393145930
- ChromeStatus.com 条目: https://chromestatus.com/feature/5357329815699456
- 规范草案: https://drafts.csswg.org/css-borders-4/#corner-shaping

### Add `font-width` property and descriptor and make `font-stretch` a legacy alias

#### 新增内容
Chrome 识别 `font-width` 作为标准属性/描述符；`font-stretch` 现在是遗留别名。

#### 技术细节
通过推广 `font-width` 用于宽度/condensed/expanded 字体轴，Chrome 与规范和其他浏览器保持一致。

#### 适用场景
在 CSS 和 `@font-face` 中使用 `font-width` 以针对可变字体的宽度轴，实现跨浏览器的排版一致性。

#### 参考资料
- 跟踪 bug #356670472: https://issues.chromium.org/issues/356670472
- ChromeStatus.com 条目: https://chromestatus.com/feature/5190141555245056

### Support async attribute for SVG `<script>` element

#### 新增内容
在 SVG 脚本元素（SVGScriptElement）上实现了 `async` 属性，使其行为与 HTMLScriptElement 匹配。

#### 技术细节
根据 SVG 2.0 接口定义，SVG 中的脚本可以异步执行。

#### 适用场景
允许包含外部或内联脚本的 SVG 进行异步执行，从而改善性能和响应性。

#### 参考资料
- 跟踪 bug #40067618: https://issues.chromium.org/issues/40067618
- ChromeStatus.com 条目: https://chromestatus.com/feature/6114615389585408
- 规范: https://svgwg.org/svg2-draft/interact.html#ScriptElement:~:text=%E2%80%98script%E2%80%99%20element-,SVG%202%20Requirement%3A,Consider%20allowing%20async/defer%20on%20%E2%80%98script%E2%80%99.,-Resolution%3A

### The `request-close` invoker command

#### 新增内容
向对话框处理添加 `requestClose()` 调用器命令行为，以便可以一致地触发和拦截取消事件。

#### 技术细节
对话框现在将编程关闭请求映射到与用户操作相同的取消/关闭请求路径，从而可以通过事件处理程序进行阻止。

#### 适用场景
允许开发者在输入和编程场景中一致地拦截并阻止对话框关闭。

#### 参考资料
- 跟踪 bug #400647849: https://issues.chromium.org/issues/400647849
- ChromeStatus.com 条目: https://chromestatus.com/feature/5592399713402880
- 规范: https://html.spec.whatwg.org/multipage/form-elements.html#attr-button-command-request-close-state

### Scroll anchoring priority candidate fix

#### 新增内容
修改了滚动锚定：优先候选被用作常规锚点选择算法的作用域/根，而不是自动成为锚点。

#### 技术细节
算法现在在该作用域内选择最深的在屏元素作为锚点，改变了锚点选择行为。

#### 适用场景
在增量内容更改和图像加载期间减少错误跳动并提高布局稳定性。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/5070370113323008

已保存文件路径:
digest_markdown/webplatform/CSS/chrome-139-stable-en.md