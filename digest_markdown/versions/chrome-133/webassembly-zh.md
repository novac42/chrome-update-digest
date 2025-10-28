---
layout: default
title: webassembly-zh
---

## 领域摘要

Chrome 133 通过采纳 Memory64 提案推进了 WebAssembly 的支持，该提案将线性内存扩展到超过 $2^{32}$ 的大小。该更改并不引入新的指令；而是将现有的内存和表指令扩展为接受 64 位索引。对于开发者而言，这使得需要非常大线性内存的 WebAssembly 模块成为可能，并减小了先前可寻址内存的硬限制。此更新使平台更成熟，可用于浏览器中运行的高内存工作负载和数据密集型大型应用。

## 详细更新

以下是 Memory64 更新的具体细节以及对 WebAssembly 开发者的影响。

### WebAssembly Memory64（支持 64 位索引）

#### 新增内容
Memory64 提案增加了对超过 $2^{32}$ 大小的线性 WebAssembly 内存的支持。不引入新指令；现有的内存和表指令被扩展以允许 64 位索引。

#### 技术细节
- 现有的 WebAssembly 内存和表操作被扩展以接受 64 位索引，而不是添加新的操作码。
- 该更改属于 WebAssembly 提案 "memory64"，并通过所引用的 ChromeStatus 条目在 Chrome 中进行跟踪。
- 相关运行时和嵌入层（WASM 运行时、浏览器引擎）必须支持对线性内存和表的 64 位寻址，才能将此能力暴露给模块。

#### 适用场景
- 需要非常大线性内存的模块（大数据集、内存数据库、科学/工程工作负载）可以突破先前的 32 位索引限制。
- 在 WebAssembly 与高内存图形或计算管线之间互操作的场景，可能从扩展的地址空间中受益。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5070065734516736)
- [规范](https://github.com/WebAssembly/memory64/blob/main/proposals/memory64/Overview.md)

文件已保存到: digest_markdown/webplatform/WebAssembly/chrome-133-stable-en.md
