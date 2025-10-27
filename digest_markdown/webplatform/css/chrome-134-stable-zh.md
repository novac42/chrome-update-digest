## 领域摘要

Chrome 134 引入了 CSS 高亮继承，改变了像 `::selection` 和 `::highlight` 这样的高亮伪类如何继承属性。主要趋势是通过遵循伪高亮链而不是元素链来澄清伪高亮的级联语义。这使得高亮样式更可预测，减少了作者的变通手段，并使行为与不断演进的 CSS Pseudo-Elements 规范保持一致。开发者应预期在 shadow DOM 和 composed trees 中获得更一致的选区/高亮样式。

## 详细更新

下面的条目扩展了摘要并解释了对开发者的实际影响。

### CSS highlight inheritance（CSS 高亮继承）

#### 新增内容
通过 CSS 高亮继承，CSS 高亮伪类（例如 `::selection` 和 `::highlight`）通过伪高亮链而不是元素链继承它们的属性，从而为高亮提供了更直观的继承模型。

#### 技术细节
继承现在遵循 CSS Pseudo-Elements level 4 草案中描述的 "highlight cascade"：高亮形成它们自己的级联链，因此高亮伪类的计算值来源于该链中的高亮祖先，而不是主机元素的祖先。这使得对高亮伪元素的样式属性传递与规范的伪高亮链语义一致。

#### 适用场景
- 在 shadow DOM 边界和组合组件中编写一致的 `::selection` 或 `::highlight` 样式。
- 在为嵌套组件内部的高亮设置样式时减少对 CSS 特异性变通方法的需求。
- 对检查或覆盖选区/高亮样式的工具来说，计算样式行为更可预测。

#### 参考资料
- ChromeStatus.com entry: https://chromestatus.com/feature/5090853643354112
- Spec: https://drafts.csswg.org/css-pseudo-4/#highlight-cascade

## 领域专长

- css: 澄清了高亮伪类的级联/继承语义；使 UA 行为与 CSS Pseudo-Elements spec 保持一致。
- webapi: 影响通过 DOM/style API 暴露的伪元素的计算样式检索和样式交互。
- graphics-webgpu: 对渲染管线（rendering pipelines）没有直接影响；样式更改仅在绘制差异改变图层时可能影响 GPU 合成输入。
- javascript: `getComputedStyle` 和涉及高亮的动态样式调整将反映新的继承模型。
- security-privacy: 直接影响最小；选区样式仍然是仅限 UI 的问题，但一致性减少了意外可见性变化。
- performance: 简化作者样式，可能减少由变通手段引发的强制样式重计算。
- multimedia: 对媒体播放或编解码器没有实质性影响。
- devices: 无设备 API 影响。
- pwa-service-worker: 无直接关联。
- webassembly: 不受影响。
- deprecations: 无弃用；这是一个与规范对齐的规范性行为更改。