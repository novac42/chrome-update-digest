# Chrome 143 Origin Trials

## 领域摘要

Chrome 143 引入了两个重要的 origin trial，扩展了 Web 平台在凭证管理和应用安装方面的能力。Digital Credentials API 获得了颁发支持，使颁发机构能够通过本地凭证管理系统将数字凭证安全地提供到用户钱包中。Web Install API 首次亮相，为网站提供了以编程方式从自己的源或跨源安装 Web 应用的能力，推进了超越传统手动流程的安装体验。这两个特性都代表了在桥接 Web 和本地平台能力方面的重要步骤，同时通过 origin trial 计划维护安全和隐私标准。

## 详细更新

这些 origin trial 支持了以前在 Web 平台上不可用的凭证颁发和应用安装的新模式。

### Digital Credentials API (issuance support)（数字凭证 API（颁发支持））

#### 新增内容

此特性使大学、政府机构或银行等颁发网站能够安全地直接启动数字凭证到用户移动钱包应用的供应流程。该 API 提供了从 Web 向本地凭证存储系统颁发凭证的标准化方式。

#### 技术细节

该实现利用特定于平台的凭证管理系统进行安全存储。在 Android 上，它使用 Android `IdentityCredential` CredMan 系统（Credential Manager），提供系统级凭证存储和管理。在桌面平台上，该特性通过 CTAP（Client to Authenticator Protocol）使用跨设备方法，类似于 Digital Credentials 呈现的工作方式。这种架构确保凭证被安全颁发，同时保持跨不同设备类型和操作系统的兼容性。

#### 适用场景

此 API 支持数字身份和凭证的关键用例：
- 大学可以直接向学生设备颁发数字学生证和文凭
- 政府机构可以提供数字驾驶执照、国民身份证和其他官方文件
- 银行和金融机构可以颁发数字支付凭证、账户访问令牌和验证凭证
- 医疗保健提供者可以分发数字健康卡和疫苗接种记录

该 API 标准化了以前分散的专有凭证颁发机制，使开发者更容易构建跨平台凭证解决方案。

#### 参考资料

- [Origin Trial](https://developer.chrome.com/origintrials/#/register_trial/385620718093598721)
- [跟踪错误 #378330032](https://issues.chromium.org/issues/378330032)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5099333963874304)
- [规范](https://w3c-fedid.github.io/digital-credentials)

### Web Install API

#### 新增内容

Web Install API 为网站提供了以编程方式安装 Web 应用的能力。调用时，API 可以根据提供的参数将调用网站本身或来自不同源的另一个站点作为 Web 应用安装。这代表了 Web 应用安装能力的重大进步。

#### 技术细节

该 API 使用新的安装能力扩展了现有的 Web 应用清单规范。该特性支持同源和跨源安装场景，允许灵活的安装模式。当网站调用 API 时，它会以编程方式触发浏览器的 Web 应用安装流程，而不需要用户手动发现和使用特定于浏览器的安装 UI。该 API 尊重所有现有的 Web 应用清单配置和安全策略，确保编程安装保持与手动安装相同的安全保证。

#### 适用场景

此 API 支持几个重要的安装模式：
- 应用商店和目录站点可以从其他源安装 Web 应用，创建 Web 原生应用分发平台
- 网站可以提供突出的"安装应用"按钮，直接触发安装，无需用户查找浏览器菜单
- 渐进式 Web 应用入门流程可以在用户旅程的最佳时刻以编程方式安装应用
- 相关 Web 应用之间的交叉推广成为可能，其中一个应用可以推荐并安装另一个应用

该 API 对于改善 Web 应用的可发现性和减少安装过程中的摩擦特别有价值，这一直是 PWA 采用的关键挑战。

#### 参考资料

- [Origin Trial](https://developer.chrome.com/origintrials/#/view_trial/2367204554136616961)
- [跟踪错误 #333795265](https://issues.chromium.org/issues/333795265)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5183481574850560)
- [规范](https://github.com/w3c/manifest/pull/1175)
