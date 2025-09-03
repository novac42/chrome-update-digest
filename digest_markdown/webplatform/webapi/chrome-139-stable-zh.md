````markdown
digest_markdown/webplatform/Web API/chrome-139-stable-zh.md

---

# Chrome 更新分析器 – Web API 区域摘要  
**Chrome 版本：** 139（稳定版）

---

## 1. 执行摘要

Chrome 139 为 Web API 领域带来了多项重要更新，包括针对多源应用扩展的 Web 应用清单能力、更严格且符合规范的 JSON MIME 类型检测、增强的 WebGPU 特性报告，以及更细粒度的崩溃报告端点。这些变更共同提升了互操作性、开发者控制力和平台可靠性。

---

## 2. 关键影响

### 技术影响

- **现有实现：**  
  - Web 应用现在可在多个源之间统一体验，需要更新清单并进行源关联。
  - JSON 数据处理更加健壮且符合标准，可能影响旧有 MIME 类型的使用。
  - WebGPU 应用获得更清晰的特性/限制自省能力，提升跨设备兼容性。
  - 崩溃报告可更高效地收集，减少噪音并改善诊断。

- **新能力：**  
  - 通过清单 `scope_extensions` 实现多源 Web 应用部署。
  - 按 WHATWG 规范准确检测所有有效的 JSON MIME 类型。
  - 可编程验证 WebGPU 核心特性支持情况。
  - 针对特定端点的崩溃报告投递。

- **技术债务考量：**  
  - 依赖非标准 JSON MIME 类型的旧代码可能需要更新。
  - WebGPU 应用应审查特性检测逻辑。
  - 崩溃报告集成可能需要调整端点配置。

---

## 3. 风险评估

### 关键风险

- **破坏性更改：**  
  - 更严格的 JSON MIME 类型检测可能导致依赖不合规类型的集成出现故障。

- **安全考量：**  
  - 多源 Web 应用必须确保正确的源关联，以防止伪造或权限提升。
  - 崩溃报告端点需安全管理，避免数据泄露。

### 中等风险

- **弃用：**  
  - 对非标准 JSON MIME 类型的隐式支持已被弃用。
  - 默认崩溃报告端点在针对性诊断方面可能不再适用。

- **性能影响：**  
  - 极小；主要变更在于 API 行为和报告粒度。

---

## 4. 推荐措施

### 立即行动

- 检查 Web 应用清单以支持多源，并根据需要添加 `scope_extensions`。
- 审查 API 中的 JSON MIME 类型使用，更新任何不合规类型。
- 更新崩溃报告集成，使用专用的 `crash-reporting` 端点。

### 短期规划

- 重构 WebGPU 特性检测逻辑，利用 `core-features-and-limits`。
- 监控因更严格 MIME 类型检测引发的问题，并处理旧数据源。
- 验证多源 Web 应用的源关联。

### 长期策略

- 规划所有 Web API 向严格 MIME 类型合规迁移。
- 扩展多源 Web 应用策略，实现统一用户体验。
- 投资于利用新端点控制的健壮崩溃报告与诊断基础设施。
- 跟踪 WebGPU 规范后续发展，确保未来兼容性。

---

## 5. 特性分析

---

### Web app scope extensions（Web 应用范围扩展）

**影响级别：** 🟡 重要

**变更内容：**  
Web 应用清单新增 `scope_extensions` 字段，使 Web 应用可将范围扩展至其他源。控制多个子域或顶级域的站点现在可作为单一 Web 应用呈现，前提是所列源通过 `.well-known` 文件确认关联。

**意义：**  
促进多源 Web 应用的无缝体验，减少碎片化，提升相关域的用户参与度。

**实施指南：**
- 更新清单，针对相关源添加 `scope_extensions`。
- 确保每个源托管所需的 `.well-known` 关联文件。
- 审查扩展范围带来的安全影响。

**参考资料：**
- [Tracking bug #detail?id=1250011](https://issues.chromium.org/issues/detail?id=1250011)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5746537956114432)
- [Spec](https://github.com/WICG/manifest-incubations/pull/113)

---

### Specification-compliant JSON MIME type detection（规范兼容的 JSON MIME 类型检测）

**影响级别：** 🔴 关键

**变更内容：**  
Chrome 现已根据 WHATWG mimesniff 规范识别所有有效的 JSON MIME 类型，包括任何以 `+json` 结尾的子类型，以及 `application/json` 和 `text/json`。这确保依赖 JSON 检测的 Web API 行为一致。

**意义：**  
提升互操作性和标准兼容性，但可能导致使用非标准 MIME 类型的旧集成出现故障。

**实施指南：**
- 检查所有 API 端点和数据源，确保 JSON MIME 类型合规。
- 更新任何使用弃用或非标准 MIME 类型的端点。
- 测试集成，确保与更严格检测兼容。

**参考资料：**
- [ChromeStatus.com entry](https://chromestatus.com/feature/5470594816278528)
- [Spec](https://mimesniff.spec.whatwg.org/#json-mime-type)

---

### WebGPU `core-features-and-limits`

**影响级别：** 🟡 重要

**变更内容：**  
WebGPU 适配器和设备现已公开规范核心特性和限制的支持情况，开发者可编程验证兼容性。

**意义：**  
支持 GPU 加速应用的健壮特性检测与降级策略，提升在多样硬件上的可靠性。

**实施指南：**
- 更新 WebGPU 初始化逻辑，检查 `core-features-and-limits`。
- 对不支持的设备实现降级或警告机制。
- 关注规范变更，及时适配新增特性。

**参考资料：**
- [Tracking bug #418025721](https://issues.chromium.org/issues/418025721)
- [ChromeStatus.com entry](https://chromestatus.com/feature/4744775089258496)
- [Spec](https://gpuweb.github.io/gpuweb/#core-features-and-limits)

---

### Crash Reporting API: Specify `crash-reporting` to receive only crash reports（崩溃报告 API：指定 `crash-reporting` 仅接收崩溃报告）

**影响级别：** 🟢 可选优化

**变更内容：**  
开发者现在可指定 `crash-reporting` 端点，仅接收崩溃报告，而非默认端点聚合的多种报告类型。可为针对性崩溃诊断提供独立 URL。

**意义：**  
提升崩溃分析的信噪比，实现更聚焦和可操作的诊断。

**实施指南：**
- 更新崩溃报告配置，使用专用端点。
- 确保端点安全及隐私合规。
- 监控崩溃报告投递的完整性。

**参考资料：**
- [Tracking bug #414723480](https://issues.chromium.org/issues/414723480)
- [ChromeStatus.com entry](https://chromestatus.com/feature/5129218731802624)
- [Spec](https://wicg.github.io/crash-reporting/#crash-reports-delivery-priority)

---

**摘要结束**
````