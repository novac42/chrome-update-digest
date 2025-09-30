---
layout: default
title: chrome-139-zh
---

## 详细更新

以下条目说明了 Chrome 139 中针对 HTML-DOM 的具体更改及其对开发者的影响。

### Allow more characters in JavaScript DOM APIs（允许在 JavaScript DOM API 中使用更多字符）

#### 新增内容
用于创建元素和属性的 JavaScript DOM API 所执行的验证已被放宽，使允许的字符和名称集合与 HTML 解析器接受的内容更一致。

#### 技术细节
此更改调整了 DOM API 的验证逻辑，以与解析器行为和 DOM 规范中关于名称/命名空间的处理一致。实现与跟踪记录在 Chromium 问题跟踪器和 ChromeStatus 中。有关命名空间和名称处理的权威规则，请参阅规范。

#### 适用场景
- 动态合成元素或属性的库和框架在使用非标准或非 ASCII 名称时将减少失败情况。
- 本地化和 i18n 场景中，元素/属性名称可能包含更广字符范围时将更可靠。
- 在动态生成 DOM 节点时，减少对编码或回退策略的需求。

#### 参考资料
- 跟踪问题 #40228234 - https://issues.chromium.org/issues/40228234
- ChromeStatus.com 条目 - https://chromestatus.com/feature/6278918763708416
- 规范 - https://dom.spec.whatwg.org/#namespaces

## 领域特定专业知识（HTML-DOM 影响）

- css: 更广的允许名称可能影响按名称匹配元素/属性的创作和工具；确保选择器生成/转义能处理扩展的名称形式。
- webapi: DOM creation APIs (e.g., element/attribute constructors) 将接受更广的字符集；审查先前对名称进行消毒或拒绝的代码。
- graphics-webgpu: 对 GPU 渲染管线无直接影响；但用于呈现控件的动态生成 DOM 可能更灵活。
- javascript: 在调用 DOM API 创建具有非标准名称的节点时运行时异常减少；所需的 polyfill 更少。
- security-privacy: 放宽验证时应审查与 CSP 或消毒器的任何交互——确保应用层验证仍然适当。
- performance: 消除了某些防御性逻辑和用于清理名称的往返操作，可能简化 DOM 构造路径。
- multimedia: 对媒体 API 无直接更改，但用于元数据的动态创建属性名称将更为宽松。
- devices: 对硬件 API 无直接影响；DOM 命名放宽不会改变能力曝光。
- pwa-service-worker: 服务工作者生成的 DOM 快照或序列化策略可能需要更少的名称混淆。
- webassembly: 生成操纵 DOM 的 JS 的 WASM 模块将受益于更少的名称验证边缘情况。
- deprecations: 这不是弃用；这是互操作性改进。请检查仍然强制更严格验证的旧用户代理的兼容性。

保存路径:
```text
digest_markdown/webplatform/HTML-DOM/chrome-139-stable-en.md
