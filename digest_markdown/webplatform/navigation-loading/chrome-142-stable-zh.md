## 领域摘要

Chrome 142 的 Navigation-Loading 更新聚焦于在同源且由渲染器发起的导航中保留粘性用户激活。对开发者影响最大的是：在导航到另一个同源页面后，用户激活状态会被保留，从而解决了例如自动聚焦时虚拟键盘不弹出等阻碍问题。此举通过降低需要先前用户激活的导航后交互的摩擦，推动 Web 平台的发展。该更改重要在于它恢复了开发者对跨同源导航中无缝交互行为的预期。

## 详细更新

以下是 Chrome 142 中 Navigation-Loading 更改的详细说明。

### Sticky user activation across same-origin renderer-initiated navigations（跨同源由渲染器发起的导航下的粘性用户激活）

#### 新增内容
此功能在页面导航到另一个同源页面后保留粘性用户激活状态。

#### 技术细节
适用于由渲染器发起的同源导航；浏览器将在导航后的文档中保留粘性用户激活标志，以便依赖先前激活的行为得以继续。

#### 适用场景
- 支持诸如在被导航到的页面中自动聚焦时显示虚拟键盘等场景。  
- 解除依赖跨同源导航保留用户激活的开发者工作流阻碍。

#### 参考资料
- [跟踪错误 #433729626](https://issues.chromium.org/issues/433729626)  
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5078337520926720)  
- [规范](https://github.com/whatwg/html/pull/11454)