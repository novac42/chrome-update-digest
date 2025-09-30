## 领域摘要

Chrome 137 的 Web API 更新强调平台的隐私、安全和开发者诊断。关键更改包括更强的资源和存储分区、用于跨源隔离的文档级隔离策略、Web Crypto 中内置的 Ed25519 支持、基于 HSTS 的跟踪缓解，以及针对无响应页面的更丰富崩溃诊断。这些更新通过收紧隔离边界、扩展加密能力、减少跨站跟踪向量并增强开发者诊断客户端挂起的能力来推进 Web。它们共同降低了 Web 开发者的风险并增强了用户隐私和安全保障。

## 详细更新

以下条目扩展了上文主题，并强调对 Web API 消费者和实现者的实际影响。

### Blob URL Partitioning: Fetching/Navigation（Blob URL 分区：获取/导航）

#### 新增内容
通过 Storage Key（top-level site、frame origin 以及 has-cross-site-ancestor 布尔值）对 Blob URL 访问进行了分区；顶级导航仍仅按 frame origin 分区。

#### 技术细节
Blob URL 访问现在被限定在 Storage Key 边界内，以与 Storage Partitioning 保持一致。这改变了子资源和框架解析 blob URL 的方式，实施每站点/每框架隔离，但顶级导航仍保持仅按 origin 分区。

#### 适用场景
- 防止通过嵌入框架的 blob URL 导致的跨站泄露。
- 帮助依赖 blob URL 进行资源交付的开发者理解跨源解析的变化。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40057646 (Tracking bug #40057646)
- https://chromestatus.com/feature/5037311976488960 (ChromeStatus.com entry)

### Call stacks in crash reports from unresponsive web pages（来自无响应网页的崩溃报告中的调用栈）

#### 新增内容
当页面因长时间运行的 JavaScript（例如无限循环）变为无响应时，Chrome 会捕获并在崩溃/无响应报告中包含 JavaScript 调用栈。

#### 技术细节
该功能在无响应时记录 JS 调用栈并将其包含在上报载荷中，从而支持运行时挂起的根本原因分析。

#### 适用场景
- 改善开发者对性能和活性问题的调试。
- 帮助对客户端无限循环或阻塞计算进行分类和排查。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1445539 (Tracking bug #1445539)
- https://chromestatus.com/feature/5045134925406208 (ChromeStatus.com entry)
- https://w3c.github.io/reporting/#crash-report (Spec)

### Document-Isolation-Policy（文档隔离策略）

#### 新增内容
Document-Isolation-Policy 允许文档为自身启用 crossOriginIsolation（独立于页面 COOP/COEP），并以进程隔离为后盾；在该策略下，非 CORS 的跨源子资源会被不同对待。

#### 技术细节
文档可以在文档级别声明隔离，从而触发进程隔离并根据策略语义改变对跨源非 CORS 子资源的处理方式。

#### 适用场景
- 允许页面在不部署全站 COOP/COEP 的情况下选择使用跨源隔离功能。
- 对需要隔离上下文（例如用于强大能力的 API）而又想避免全站头部更改的开发者有用。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=333029146 (Tracking bug #333029146)
- https://chromestatus.com/feature/5048940296830976 (ChromeStatus.com entry)
- https://wicg.github.io/document-isolation-policy/ (Spec)

### Ed25519 in web cryptography（Web 加密中的 Ed25519）

#### 新增内容
在 Web Cryptography API 中添加对 Curve25519 算法的支持，尤其是 Ed25519 签名算法。

#### 技术细节
Ed25519 的密钥生成、签名与验证通过 WebCrypto API 公开，使 Web 应用可以原生使用 Ed25519 原语。

#### 适用场景
- 用于客户端加密和认证的现代签名方案。
- 使库和应用可以在无需 polyfill 或 WASM 回退的情况下采用 Ed25519。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=1370697 (Tracking bug #1370697)
- https://chromestatus.com/feature/5056122982457344 (ChromeStatus.com entry)
- https://www.rfc-editor.org/rfc/rfc8032.html (Spec)

### HSTS tracking prevention（HSTS 跟踪预防）

#### 新增内容
通过限制 HSTS 缓存的使用来缓解第三方跟踪：仅允许顶级导航进行 HSTS 升级，并阻止对子资源请求的 HSTS 升级。

#### 技术细节
HSTS 升级行为被限制，以便子资源请求不能利用 HSTS 缓存进行跨站跟踪；顶级导航仍然会接收 HSTS 升级。

#### 适用场景
- 降低将 HSTS 状态用作跨站跟踪通道的可行性。
- 对第三方隐私影响关切的 Web 开发者应预期子资源的因 HSTS 导致的跨站重定向将减少。

#### 参考资料
- https://bugs.chromium.org/p/chromium/issues/detail?id=40725781 (Tracking bug #40725781)
- https://chromestatus.com/feature/5065878464307200 (ChromeStatus.com entry)

已保存到: digest_markdown/webplatform/Web API/chrome-137-stable-en.md