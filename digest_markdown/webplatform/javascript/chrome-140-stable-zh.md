## 区域摘要

Chrome 140 stable 引入了两项针对 JavaScript 领域的重点更改：在 Uint8Array 与 base64/hex 表示之间的内建转换，以及对 view transition finished promise 定时的调整。Uint8Array 转换功能减少了对自定义二进制 ↔ 文本 编码工具的需求，改善了互操作性和开发者使用便捷性。view transition 定时更改针对由 promise 解析顺序引起的可见闪烁，从而提高了动画的健壮性和感知性能。这两项更新收紧了平台原语，使开发者可以减少对临时解决方法的依赖。

## 详细更新

下面是每项 JavaScript 领域更改的简明、面向开发者的分解说明及其重要性。

### `Uint8Array` to and from base64 and hex（Uint8Array 与 base64/hex 相互转换）

#### 新增内容
新增在 Uint8Array 二进制数据与 base64/hex 文本编码之间进行转换的能力与方法。

#### 技术细节
此功能为二进制 <-> 文本 编码的转换标准化了 API；有关方法具体形状和语义，请参阅语言级规范。

#### 适用场景
- 对二进制数据进行传输或存储编码（例如，嵌入图像、发送紧凑负载）。
- 将 base64/hex 载荷解码为 typed arrays，以便通过 Web APIs（crypto、WebAssembly、fetch 响应处理）进行处理。
- 减少对实用库和自定义编码/解码代码路径的依赖。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/6281131254874112  
- 规范: https://tc39.es/proposal-arraybuffer-base64/spec

### View transition finished promise timing change（finished promise 定时调整以避免动画末端闪烁）

#### 新增内容
已更改 view transition finished promise 的定时，以解决在渲染生命周期步骤内发生 promise 解析并在动画结束处导致可见闪烁的情况。

#### 技术细节
调整针对 finished promise 相对于渲染生命周期何时解析，以确保对完成作出反应的脚本不会在移除 view transition 的视觉帧之后运行，从而避免动画结束时的视觉瑕疵。

#### 适用场景
- 在视图切换流程中获得更平滑的体验，当过渡结束后脚本需要操作 DOM 或样式时尤为重要。
- 为在等待 finished promise 后执行最终布局或清理的框架和库提供可靠的动画终点。
- 减少为避免闪烁而使用脆弱计时技巧或强制重排的需要。

#### 参考资料
- 跟踪 bug #430018991: https://issues.chromium.org/issues/430018991  
- ChromeStatus.com 条目: https://chromestatus.com/feature/5143135809961984

已保存文件路径：digest_markdown/webplatform/JavaScript/chrome-140-stable-en.md