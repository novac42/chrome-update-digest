## 领域摘要

Chrome 143 的 CSS 更新专注于为开发者提供更精细、更确定的布局、背景定位和排版控制，同时标准化 Web 应用的更新行为。最具影响力的变化是针对锚点定位元素的锚定回退容器查询（anchored fallback container queries）和侧相对（side-relative）背景定位长属性，它们改进了响应式和系留式布局。`font-language-override` 的添加使多语言排版的 OpenType 语言行为更加精确。这些更新通过扩展响应式布局原语和排版控制，以及使应用更新行为更可预测，推动了平台的发展。

## 详细更新

以下条目在上述摘要基础上提供了简洁的、以开发者为中心的详细信息和参考资料。

### CSS anchored fallback container queries

#### 新增内容
引入 `@container anchored(fallback)` 以根据应用的 `position-try-fallbacks` 对锚点定位元素的后代进行样式设置。

#### 技术细节
启用作用域限定于锚定元素的容器查询，使样式能够响应锚点和锚定元素的回退定位行为。

#### 适用场景
根据运行时使用的回退定位，对锚定元素的系留、动画或布局进行样式设置。

#### 参考资料
- [跟踪错误 #417621241](https://issues.chromium.org/issues/417621241)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5177580990496768)
- [规范](https://drafts.csswg.org/css-anchor-position-2/#anchored-container-queries)

### Side-relative syntax for `background-position-x/y` longhands

#### 新增内容
为背景图像定位定义侧相对语法，允许相对于边缘而非固定值指定位置。

#### 技术细节
提供更灵活的响应式背景定位机制，可适应窗口或框架尺寸；该特性也应用于相关的带供应商前缀的长属性。

#### 适用场景
需要相对于元素边缘对齐的响应式背景放置，无需为不同视口尺寸重新计算固定偏移量。

#### 参考资料
- [跟踪错误 #40468636](https://issues.chromium.org/issues/40468636)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5073321259565056)
- [规范](https://drafts.csswg.org/css-backgrounds-4/#background-position-longhands)

### Implement CSS property `font-language-override`

#### 新增内容
添加对 `font-language-override` CSS 属性的支持，通过四字符语言标签覆盖用于 OpenType 字形替换的系统语言。

#### 技术细节
该属性允许作者在 CSS 中直接指定语言标签以影响 OpenType 替换，提供样式表级别对特定语言排版特性的控制。

#### 适用场景
对多语言内容进行细粒度排版控制，确保跨平台的字形选择和整形一致性。

#### 参考资料
- [跟踪错误 #41170551](https://issues.chromium.org/issues/41170551)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5149766073843712)
- [规范](https://www.w3.org/TR/css-fonts-4/#font-language-override-prop)

### Web App Manifest: specify update eligibility

#### 新增内容
添加在 Web App Manifest 中指定更新资格算法的方法，使更新适用性更加确定。

#### 技术细节
清单级别的设置使开发者能够控制更新是否以及何时应用于现有安装，从而能够移除_更新检查节流_。

#### 适用场景
为已安装的 Web 应用提供可预测的更新推出，开发者需要对更新时机和资格进行确定性控制。

#### 参考资料
- [跟踪错误 #403253129](https://issues.chromium.org/issues/403253129)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5148463647686656)
