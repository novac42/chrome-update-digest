---
layout: default
title: identity-zh
---

## 领域摘要

Chrome 136 通过改进联邦登录 UI 和启用将密码迁移到 passkeys 的 WebAuthn 流程来推进 Identity 领域。FedCM 的更改允许在一次 `get()` 调用中在同一对话框中展示多个身份提供者，并在被动模式中移除 “add another account” 流程。WebAuthn 条件性创建（passkey 升级）允许网站将现有的密码凭据升级为 passkeys，从而简化迁移。这些更新减少了认证摩擦，帮助开发者将用户转向更强、更抗钓鱼的凭证。

## 详细更新

下面的条目扩展了摘要内容，并解释了对开发者的实际影响与技术细节。

### FedCM updates（FedCM 更新）

#### 新增内容
FedCM 可以在同一对话框中展示多个身份提供者，当所有提供者在单个 `get()` 调用中返回时。Chrome 136 还在 FedCM 被动模式中移除了对 “add another account” 的支持。

#### 技术细节
- 单个 FedCM `get()` 调用可以包含多个提供者，因此浏览器 UI 可以将它们一起显示。
- 通过移除 “add another account” 流程，收紧了被动模式的行为（详细信息和理由见关联的跟踪 bug）。

#### 适用场景
- 支持多个联邦 IdP 的网站可以呈现统一的选择 UI，而无需多次往返。
- 简化实现多提供者的注册/登录流程，减少用户体验碎片化。

#### 参考资料
- 跟踪 bug #1348262: https://bugs.chromium.org/p/chromium/issues/detail?id=1348262
- ChromeStatus.com 条目: https://chromestatus.com/feature/5049732142194688
- 规范: https://fedidcg.github.io/FedCM/

### Web authentication conditional create (passkey upgrades)（条件性创建：passkey 升级）

#### 新增内容
WebAuthn 条件性创建请求使网站能够将现有的密码凭据升级为 passkeys。

#### 技术细节
- 条件性创建是一种 WebAuthn mediation 模式，允许用户代理在上下文中提供验证器创建，从而启用从密码到 passkeys 的凭据升级流程（参见跟踪 bug 和规范链接）。

#### 适用场景
- 以较低的用户摩擦逐步将用户账户从基于密码的认证迁移到 passkeys。
- 在账户设置或登录流程中实现，当检测到密码凭据时提示用户创建 passkey。

#### 参考资料
- 跟踪 bug #377758786: https://bugs.chromium.org/p/chromium/issues/detail?id=377758786
- ChromeStatus.com 条目: https://chromestatus.com/feature/5097871013068800
- 规范: https://w3c.github.io/webauthn/#enum-credentialmediationrequirement
