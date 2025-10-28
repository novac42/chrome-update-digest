---
layout: default
title: chrome-133-zh
---

## 详细更新

以下是上述弃用项的简要列表，包含简明的技术背景和实用的迁移说明。

### Deprecate WebGPU limit `maxInterStageShaderComponents`（弃用）

#### 新增内容
`maxInterStageShaderComponents` 限制已被弃用；Chrome 计划在 Chrome 135 中移除它。弃用的原因是它与 `maxInterStageShaderVariables` 的冗余以及公告中提到的其他因素。

#### 技术细节
此次弃用移除了一项重叠的 GPU 功能限制，该限制用于控制在着色器阶段之间传递的数据。实现应改为依赖剩余的 `maxInterStageShaderVariables` 限制及规范的 WebGPU 限制。移除后运行时将不再报告或强制执行这个独立限制。

#### 适用场景
- 着色器作者和引擎开发者应审查阶段间数据的使用，并将任何引用 `maxInterStageShaderComponents` 的检查或回退迁移到基于变量的规范限制上。
- 图形测试套件应停止断言已弃用的限制，并针对剩余限制验证行为。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/4853767735083008)

### Remove `<link rel=prefetch>` five-minute rule（移除）

#### 新增内容
Chrome 不再对预取资源应用忽略缓存语义的五分钟例外。预取现在会立即遵循正常的 HTTP 缓存语义。

#### 技术细节
此前，为避免重新获取，预取资源在首次使用的五分钟内，`max-age` 和 `no-cache` 指令会被临时覆盖。该例外现已移除；浏览器在首次使用时将根据标准 HTTP 语义遵守 cache-control 头。

#### 适用场景
- 依赖预取绕过服务器 cache-control 以实现短期复用的开发者应更新策略以尊重缓存头（例如，调整服务端 cache-control，或使用 service workers 以获得更多控制）。
- 性能工具和审计应更新，以反映预取不再提供临时缓存覆盖。

#### 参考资料
- [跟踪 Bug #40232065](https://issues.chromium.org/issues/40232065)
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5087526916718592)

### Remove Chrome Welcome page triggering with initial prefs first run tabs（移除）

#### 新增内容
在 `initial_preferences` 文件的 `first_run_tabs` 属性中包含 chrome://welcome 将不再触发 Welcome 页面。此行为被移除，因为 Welcome 页面与桌面首运行体验重复。

#### 技术细节
initial preferences 中的 `first_run_tabs` 钩子此前允许管理员或安装程序在首次运行时打开 chrome://welcome；该钩子现在对该 URL 将被忽略。该更改影响桌面平台的首次运行流程，并简化产品层的入门触发。

#### 适用场景
- 依赖通过 initial preferences 注入 chrome://welcome 的管理员或 OEM 应移除该自定义，并使用受支持的首运行体验配置机制。
- 更新任何期望通过 `first_run_tabs` 打开 Welcome 页面的自动化或供应脚本。

#### 参考资料
- [ChromeStatus.com 条目](https://chromestatus.com/feature/5118328941838336)
- [知识共享署名 4.0 许可证](https://creativecommons.org/licenses/by/4.0/)
- [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0)
- [Google 开发者网站政策](https://developers.google.com/site-policies)

保存此摘要的文件路径：
digest_markdown/webplatform/Deprecations/chrome-133-stable-en.md
