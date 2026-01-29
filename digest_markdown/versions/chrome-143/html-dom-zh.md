---
layout: default
title: html-dom-zh
---

## 领域摘要

Chrome 143 放宽了 JavaScript DOM API 验证，使 HTML 解析器接受的元素和属性名称也能被脚本创建时接受。这减少了解析 HTML 和 DOM 创建节点之间令人惊讶的不匹配，使 DOM API 更加宽容和一致。对于开发者而言，此更改降低了以编程方式创建以前验证失败的元素/属性时的摩擦。总体而言，它推进了平台的一致性和解析与脚本路径之间的互操作性。

## 详细更新

以下单个更新扩展了摘要，并解释了对以 DOM 为中心的开发的实际影响。

### Allow more characters in JavaScript DOM APIs

#### 新增内容
JavaScript DOM API 现在通过放宽验证以匹配 HTML 解析器允许的内容，接受更广泛的元素和属性名称字符集。

#### 技术细节
此更改使 DOM API 验证规则与 HTML 解析器的名称处理保持一致，使解析期间允许的名称在通过脚本接口创建时也被允许。

#### 适用场景
- 以前验证失败的元素和属性的编程创建现在将成功。
- 减少了使用变通方法（例如，通过 innerHTML 构造节点）来表示解析 HTML 中允许的名称的需要。
- 改进了解析生成的 DOM 与脚本生成的 DOM 之间的对等性，简化了开发者对节点创建的推理。

#### 参考资料
- [跟踪错误 #40228234](https://issues.chromium.org/issues/40228234)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/6278918763708416)
- [规范](https://dom.spec.whatwg.org/#namespaces)
