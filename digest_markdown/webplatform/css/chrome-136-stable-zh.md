## 领域摘要

Chrome 136 在颜色管理、隐私和现代语法处理方面推进了 CSS。主要更改包括 HDR 亮度控制（`dynamic-range-limit`）、标准化的打印颜色控制（未加前缀的 `print-color-adjust`）、更严格的 `:visited` 样式隔离以防止历史泄露、将 `attr()` 的 string 类型重命名为 `raw-string`，以及对 `var()` 回退值更宽松的类型处理。这些更新增强了开发者对渲染的控制、与演进中的规范对齐，并减少了隐私和互操作性问题。对团队而言，这意味着为符合规范进行少量代码更新，并为打印、HDR 和自定义属性回退提供更清晰的选项。

## 详细更新

下面是 Chrome 136 中 CSS 领域的更改，附带简明的技术背景和以开发者为中心的适用场景。

### The dynamic-range-limit property (动态范围亮度限制)

#### 新增内容
允许页面限制 HDR 内容的最大亮度。

#### 技术细节
提供一个 CSS 属性以在每页范围内约束 HDR 亮度暴露（参见规范链接）。

#### 适用场景
对 HDR 图片/视频的感知亮度进行控制，以匹配站点设计或无障碍需求。

#### 参考资料
https://bugs.chromium.org/p/chromium/issues/detail?id=1470298  
https://chromestatus.com/feature/5023877486493696  
https://www.w3.org/TR/css-color-hdr/#dynamic-range-limit

### Partition :visited links history (分割 :visited 链接历史)

#### 新增内容
为消除用户浏览历史泄露，只有当锚点元素此前由此顶级站点和框架源点击过时，才会以 `:visited` 进行样式化。对于“self-links”有例外：指向站点自身页面的链接，即便未被点击，也可以被样式化为 `:visited`…

#### 技术细节
该行为更改通过按顶级站点和框架源对 `:visited` 样式进行分区，以减少跨源的历史推断。

#### 适用场景
防止站点推断跨站点链接的访问状态；开发者不应依赖 `:visited` 来实现跨源的用户体验差异。

#### 参考资料
https://bugs.chromium.org/p/chromium/issues/detail?id=1448609  
https://chromestatus.com/feature/5029851625472000  
https://www.w3.org/TR/css-pseudo-4/#visited-pseudo

### Unprefixed print-color-adjust (未加前缀的 print-color-adjust)

#### 新增内容
`print-color-adjust` 属性允许你调整打印网页中的颜色。这与 Chrome 已支持的 `-webkit-print-color-adjust` 相同，但采用了标准化名称。带 `-webkit-` 前缀的版本不会被移除。

#### 技术细节
在现有带 `-webkit-` 前缀的实现旁添加未加前缀的标准名称以符合规范。

#### 适用场景
在需要打印颜色保真时使用标准化的 `print-color-adjust`；在需要兼容性时保留 `-webkit-print-color-adjust`。

#### 参考资料
https://developer.mozilla.org/docs/Web/CSS/print-color-adjust  
https://bugs.chromium.org/p/chromium/issues/detail?id=376381169  
https://chromestatus.com/feature/5090690412953600  
https://www.w3.org/TR/css-color-adjust-1/#print-color-adjust

### Rename string attr() type to raw-string (将 string attr() 类型重命名为 raw-string)

#### 新增内容
CSS 工作组已决定将 `string` `attr()` 类型替换为 `raw-string`。因此从 Chrome 136 起，`attr(data-foo string)` 变为 `attr(data-foo raw-string)`。

#### 技术细节
在 `attr()` 类型注释中进行语法级别的重命名以遵循更新后的规范命名。

#### 适用场景
将现有的 `attr(... string)` 用法更新为 `attr(... raw-string)`，以符合规范并确保向前兼容。

#### 参考资料
https://bugs.chromium.org/p/chromium/issues/detail?id=400981738  
https://chromestatus.com/feature/5110654344216576  
https://www.w3.org/TR/css-values-5/#attr-notation

### Type-agnostic var() fallback (与类型无关的 var() 回退)

#### 新增内容
`var()` 函数的回退部分不再针对所引用的自定义属性的类型进行校验。

#### 技术细节
根据规范决定，`var(--prop, fallback)` 不再强制 `--prop` 与回退表达式之间的类型匹配。

#### 适用场景
允许为自定义属性提供更灵活的回退，而无需精确匹配类型；简化更具弹性的主题系统和渐进增强策略。

#### 参考资料
https://bugs.chromium.org/p/chromium/issues/detail?id=372475301  
https://chromestatus.com/feature/5049845796618240

已保存到：digest_markdown/webplatform/CSS/chrome-136-stable-en.md