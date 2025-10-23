---
layout: default
title: 领域摘要
---

# 领域摘要

Chrome 141（稳定版）为 WebAssembly 带来一项聚焦改进：自定义描述符。该功能使与源级类型关联的数据能够更高效地存储，并允许为相应的 WebAssembly 对象配置原型，从而可以在这些原型上安装方法。在 JavaScript 中对 WebAssembly 类型与行为进行建模时，它提升了易用性与表达力，从而推动 Web 平台前进。通过源站试用提供，为开发者提供评估按类型数据与方法暴露模式的机会。

## 详细更新

围绕 WebAssembly 类型建模的效率与易用性，本次版本新增：

### WebAssembly custom descriptors（自定义描述符）

#### 新增内容
- 允许 WebAssembly 将与源级类型关联的数据更高效地存储在新的“自定义描述符”对象中。
- 允许为该源级类型的 WebAssembly 对象配置原型，从而可在 WebAssembly 对象的原型上安装方法。
- 通过源站试用提供。

#### 技术细节
- 引入承载与某个源级类型关联数据的自定义描述符对象。
- 这些描述符可为该类型的 WebAssembly 对象指定原型，支持在该原型上安装方法。

#### 适用场景
- 通过已配置的原型为 WebAssembly 对象附加特定于类型的方法。
- 更高效地组织与访问按类型的元数据。

#### 参考资料
- ChromeStatus.com 条目: https://chromestatus.com/feature/6024844719947776
- 规范: https://github.com/WebAssembly/custom-descriptors/blob/main/proposals/custom-descriptors/Overview.md
