---
layout: default
title: Chrome 135 领域摘要：Origin Trials
---

# Chrome 135 领域摘要：Origin Trials

## 1. 领域摘要

Chrome 135 推出了多项具有影响力的 Origin Trials，提升了安全性、用户交互和性能。本次发布的主要主题包括加强对网页资源的信任、实现更安全的设备绑定会话、改进用户参与机制，以及通过高级预渲染提示优化导航。这些功能为开发者提供了新的工具，帮助构建更安全、更具交互性和高性能的应用。这些更新尤为重要，因为它们解决了资源完整性、会话安全和无缝用户体验等关键需求，同时允许开发者在更广泛采用前进行实验和反馈。

## 2. 详细更新

以下是 Chrome 135 推出的主要 Origin Trial 功能，每项都为开发者带来了独特的优势和技术进步。

### Device bound session credentials（设备绑定会话凭据）

#### 新增内容
使网站能够将会话安全地绑定到单一设备，确保会话续期和认证与设备专属凭据相关联。

#### 技术细节
浏览器会根据服务器请求定期续期会话，并提供设备唯一私钥的持有证明。该机制通过防止跨设备的会话劫持，提升了会话安全性。

#### 适用场景
- 敏感应用的安全认证（如银行、企业门户）
- 降低会话被盗或重放攻击的风险
- 实现基于设备的访问控制

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/3911939226324697089)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5140168270413824)
- [规范](https://w3c.github.io/webappsec-dbsc)

---

### Interest invokers（兴趣触发器）

#### 新增内容
为 `<button>` 和 `<a>` 元素引入 `interesttarget` 属性，允许开发者定义“兴趣”行为，在用户对这些元素表现出兴趣时触发相应操作。

#### 技术细节
通过添加 `interesttarget` 属性，开发者可指定目标元素和动作（如显示弹窗或预览），这些动作会在用户表现出兴趣（而不仅仅是点击）时被触发。

#### 适用场景
- 提升可访问性和用户参与度
- 实现更丰富的 UI 交互（如预览、工具提示）
- 改进 Web 应用中的导航和可发现性

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/813462682693795841)
- [跟踪问题 #326681249](https://issues.chromium.org/issues/326681249)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4530756656562176)
- [规范](https://github.com/whatwg/html/pull/11006)

---

### Signature-based integrity（基于签名的完整性）

#### 新增内容
提供一种通过数字签名验证网页资源来源的机制，允许开发者要求浏览器检查资源是否由受信任服务器签名。

#### 技术细节
服务器使用 Ed25519 密钥对对响应进行签名，浏览器在使用资源前验证签名。该机制为第三方依赖的信任建立了技术基础，并缓解了供应链风险。

#### 适用场景
- 确保关键脚本和资源的完整性
- 防止恶意或被篡改的依赖
- 更安全地使用第三方资源

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2704974526189404161)
- [跟踪问题 #375224898](https://issues.chromium.org/issues/375224898)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5032324620877824)
- [规范](https://wicg.github.io/signature-based-sri)

---

### Speculation rules: target_hint field（推测规则：target_hint 字段）

#### 新增内容
扩展推测规则语法，新增 `target_hint` 字段，允许开发者为预渲染页面指定预期的可导航目标。

#### 技术细节
`target_hint` 字段可提供提示（如 `_blank`），指示预渲染页面将被激活的位置，从而实现更高效、具备上下文感知的预渲染策略。

#### 适用场景
- 通过为特定目标预加载页面优化导航性能
- 提升用户体验，实现更快的页面切换
- 支持单页应用中的高级导航模式

#### 参考资料
- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/1858297796243750913)
- [跟踪问题 #40234240](https://issues.chromium.org/issues/40234240)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5162540351094784)
- [规范](https://wicg.github.io/nav-speculation/speculation-rules.html)
