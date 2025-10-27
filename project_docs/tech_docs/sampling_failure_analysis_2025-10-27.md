# Sampling Failure Analysis - 2025-10-27

## 问题概述

**症状**：MCP工具无法调用sampling，尽管已在MCP client中允许使用client的model

**时间线**：24小时前（commit 667ec39）可以正常工作，当前版本（HEAD: fcba2e8）失效

**影响范围**：`webplatform_digest` 工具及所有依赖LLM sampling的功能

---

## 关键破坏性变更分析

### 🔴 变更1：消息格式转换层（最可能的根本原因）

**文件**：`src/chrome_update_digest/mcp/tools/enhanced_webplatform_digest.py`

**位置**：第656-658行（sampling kwargs构建）

#### 旧代码（667ec39 - 工作版本）
```python
sample_kwargs = {
    "messages": messages,  # 直接传递原始messages
    "system_prompt": system_prompt,
    "temperature": 0.7,
    "max_tokens": max_tokens,
}
```

#### 新代码（fcba2e8 - 失效版本）
```python
sample_kwargs = {
    "messages": self._prepare_sampling_messages(messages),  # 🔴 新增转换层
    "system_prompt": system_prompt,
    "temperature": 0.7,
    "max_tokens": max_tokens,
}
```

#### 影响分析

新增的 `_prepare_sampling_messages()` 方法（第249-295行）执行以下转换：

1. **将字符串包装为 SamplingMessage 对象**：
   ```python
   if isinstance(messages, str):
       return [
           SamplingMessage(
               role="user",
               content=TextContent(type="text", text=messages),
           )
       ]
   ```

2. **将字典转换为 SamplingMessage**：
   ```python
   if isinstance(entry, dict):
       role = entry.get("role", "user")
       content = entry.get("content")
       text_content = self._convert_content_to_text(content)
       if text_content is not None:
           normalized.append(
               SamplingMessage(
                   role=role,
                   content=text_content,
               )
           )
   ```

**潜在问题**：
- FastMCP 2.x的 `Context.sample()` 可能期望原始格式（字符串或字典列表）
- `SamplingMessage` 和 `TextContent` 的序列化可能与MCP client不兼容
- 可能触发Pydantic ValidationError（代码中新增了相关错误处理）

---

### 🔴 变更2：Model Preferences强制类型转换

**位置**：第663-668行

#### 旧代码
```python
if run_preferences:
    sample_kwargs["model_preferences"] = run_preferences
```

#### 新代码
```python
if run_preferences is not None:
    coerced = self._coerce_model_preferences_for_client(run_preferences)
    # FastMCP Context.sample expects model_preferences as str or list[str]
    if isinstance(coerced, str) and coerced:
        sample_kwargs["model_preferences"] = coerced
    elif isinstance(coerced, list) and coerced:
        sample_kwargs["model_preferences"] = coerced
```

#### 新增的coercion逻辑（第75-112行）

```python
def _coerce_model_preferences_for_client(
    self, value: Optional[Union[Dict[str, Any], List[Any], str]]
) -> Optional[Union[str, List[str]]]:
    """Coerce internal model preferences into FastMCP-accepted types."""
    if value is None:
        return None

    if isinstance(value, str):
        return value.strip() or None

    if isinstance(value, list):
        models: List[str] = [str(v).strip() for v in value if str(v).strip()]
        return models or None

    if isinstance(value, dict):
        # Common shapes: {"model": "name"} or {"models": ["a", "b"]}
        model_name = value.get("model")
        if isinstance(model_name, str) and model_name.strip():
            return model_name.strip()
        models_value = value.get("models")
        if isinstance(models_value, list):
            models: List[str] = [str(v).strip() for v in models_value if str(v).strip()]
            if models:
                return models
        # Unknown dict shape – fall back to None so we don't send invalid payloads
        return None

    # Unsupported types are ignored
    return None
```

**潜在问题**：
- 如果 `run_preferences` 是字典但结构不匹配预期，会返回 `None`
- 可能导致原本有效的model preferences被过滤掉
- 没有传递model preferences时，MCP client可能无法正确分配模型

---

### 🔴 变更3：Context.sample调用方式变更

**位置**：第607-616行，第697-700行

#### 旧代码
```python
async with self._semaphore:
    response = await asyncio.wait_for(
        ctx.sample(**sample_kwargs),
        timeout=timeout
    )
```

#### 新代码
```python
sample_fn = getattr(ctx, "sample", None)
if not callable(sample_fn):
    detail = "FastMCP context does not expose a callable sample() method"
    self.telemetry.record_error(
        operation=operation,
        kind="ConfigurationError",
        detail=detail,
        area=context_extra.get("area"),
    )
    raise RuntimeError(detail)

# ... later ...
async with self._semaphore:
    response = await asyncio.wait_for(
        sample_fn(**sample_kwargs),
        timeout=eff_timeout,
    )
```

**潜在问题**：
- 使用 `getattr` 获取sample方法可能改变了方法的绑定上下文
- `sample_fn` 可能失去了某些FastMCP context的内部状态

---

### 🟡 其他相关变更

#### 4. 新增Pydantic ValidationError处理

**位置**：第10-13行，第781-795行

```python
try:  # Optional dependency; guards ValidationError handling
    from pydantic import ValidationError as PydanticValidationError
except Exception:  # pragma: no cover - keep runtime resilient if pydantic missing
    PydanticValidationError = None
```

在异常处理中：
```python
is_validation_error = (
    PydanticValidationError is not None
    and isinstance(e, PydanticValidationError)
)
if is_validation_error:
    payload_preview = self._sampling_payload_preview(sample_kwargs.get("messages", messages))
    self.telemetry.log_event(
        "llm_payload_validation_error",
        {
            "operation": operation,
            "area": context_extra.get("area"),
            "attempt": attempt_number,
            "payload_preview": payload_preview,
        },
    )
```

**意义**：说明开发者已经预见到可能出现Pydantic验证错误，这证实了消息格式转换可能存在问题。

#### 5. 默认并发度降低

**位置**：第66行

```python
# 旧代码
self._max_concurrency: int = int(os.getenv("WEBPLATFORM_MAX_CONCURRENCY", "4"))

# 新代码
self._max_concurrency: int = int(os.getenv("WEBPLATFORM_MAX_CONCURRENCY", "1"))
```

这个变更不太可能直接导致sampling失败，但会影响性能。

---

## 相关Git提交记录

从commit 667ec39到HEAD的主要提交：

1. **fcba2e8** - feat: Update model preferences handling in EnhancedWebplatformDigestTool for FastMCP compatibility
2. **b962ded** - feat: Enhance model preference coercion logic in EnhancedWebplatformDigestTool
3. **a54540c** - feat: Implement model preferences coercion for FastMCP compatibility in EnhancedWebplatformDigestTool
4. **44742d1** - feat: Enhance model preference resolution and timeout handling in EnhancedWebplatformDigestTool
5. **b5d9a59** - Add telemetry and debug logging for MCP sampling
6. **7443149** - feat: Normalize sampling payloads in EnhancedWebplatformDigestTool and update tests for bilingual support
7. **347e8b0** - feat: Update message handling in EnhancedWebplatformDigestTool to support original payloads for sampling (pass original string instead of dict)

**关键发现**：commit 347e8b0的消息提到 "pass original string instead of dict"，但实际上后续的commits又引入了复杂的转换逻辑，这可能是问题的根源。

---

## 修复方案

### 方案1：快速回滚（紧急修复）⭐ 推荐

**优点**：立即恢复功能，风险最低

**步骤**：
```bash
cd /Users/lyzh/Documents/Nova_Projects/chrome-update-digest
git checkout 667ec39 -- src/chrome_update_digest/mcp/tools/enhanced_webplatform_digest.py
```

**缺点**：丢失24小时内的其他改进

---

### 方案2：添加Legacy模式开关（平衡方案）⭐⭐ 推荐

**优点**：保留新功能的同时提供回退选项

**实现**：在 `_safe_sample()` 方法开头添加：

```python
async def _safe_sample(
    self,
    ctx: Context,
    messages: Union[str, Any],
    system_prompt: str,
    debug: bool,
    max_retries: int = 3,
    timeout: int = 120,
    telemetry_context: Optional[Dict[str, Any]] = None,
) -> str:
    """Safe sampling with exponential backoff retry and timeout, plus M2 governance."""
    
    # 🔧 Legacy模式：使用简化的调用方式
    USE_LEGACY_SAMPLING = os.getenv("USE_LEGACY_SAMPLING", "false").lower() == "true"
    
    if USE_LEGACY_SAMPLING:
        sample_kwargs = {
            "messages": messages,  # 不转换，直接传递
            "system_prompt": system_prompt,
            "temperature": 0.7,
            "max_tokens": 60000,
        }
        if self._run_model_preferences:
            sample_kwargs["model_preferences"] = self._run_model_preferences
        
        try:
            response = await asyncio.wait_for(
                ctx.sample(**sample_kwargs),
                timeout=timeout
            )
            return str(response) if not isinstance(response, str) else response
        except Exception as e:
            raise RuntimeError(f"Legacy sampling failed: {e}")
    
    # ... 继续原有逻辑 ...
```

**使用**：
```bash
export USE_LEGACY_SAMPLING=true
```

---

### 方案3：修复消息转换逻辑（根本解决）

**修改1**：在 `_prepare_sampling_messages()` 添加开关

```python
def _prepare_sampling_messages(
    self,
    messages: Union[str, Sequence[Union[str, SamplingMessage, Dict[str, Any]]]],
    normalize: bool = True,  # 添加参数控制
) -> Union[str, Sequence[Union[str, SamplingMessage]]]:
    """Normalize sampling payloads to structures accepted by FastMCP 2.x."""
    
    # 如果禁用normalize，保持原始格式
    if not normalize:
        return messages
    
    # ... 原有转换逻辑 ...
```

**修改2**：在调用处添加环境变量控制

```python
NORMALIZE_MESSAGES = os.getenv("WEBPLATFORM_NORMALIZE_MESSAGES", "false").lower() == "true"

sample_kwargs = {
    "messages": self._prepare_sampling_messages(messages, normalize=NORMALIZE_MESSAGES),
    "system_prompt": system_prompt,
    "temperature": 0.7,
    "max_tokens": max_tokens,
}
```

---

### 方案4：详细诊断模式（调查工具）

**添加诊断日志**：

```python
if debug or os.getenv("WEBPLATFORM_DEBUG_SAMPLING"):
    print("=" * 60)
    print("SAMPLING DEBUG INFO")
    print("=" * 60)
    print(f"Original messages type: {type(messages)}")
    print(f"Original messages (truncated): {str(messages)[:300]}")
    
    prepared = self._prepare_sampling_messages(messages)
    print(f"\nPrepared messages type: {type(prepared)}")
    print(f"Prepared messages (truncated): {str(prepared)[:300]}")
    
    print(f"\nModel preferences (raw): {self._run_model_preferences}")
    if self._run_model_preferences:
        coerced = self._coerce_model_preferences_for_client(self._run_model_preferences)
        print(f"Model preferences (coerced): {coerced}")
    
    print(f"\nSample kwargs keys: {list(sample_kwargs.keys())}")
    print("=" * 60)
```

**使用**：
```bash
export WEBPLATFORM_DEBUG_SAMPLING=true
# 或在tool参数中设置 debug=True
```

---

## 执行建议

### 立即执行（紧急修复）

1. **测试方案2（Legacy模式）**：
   ```bash
   export USE_LEGACY_SAMPLING=true
   # 运行测试
   ```

2. **如果Legacy模式有效**，说明问题确实在新的转换逻辑中

### 后续调查（如果Legacy模式有效）

1. **启用方案4（诊断模式）**，对比两种模式的payload差异
2. **检查FastMCP文档**，确认 `Context.sample()` 期望的消息格式
3. **根据诊断结果决定**：
   - 修复转换逻辑（方案3）
   - 或永久使用Legacy模式

### 后续调查（如果Legacy模式无效）

1. **检查MCP client配置**：确认model permissions设置
2. **检查FastMCP版本兼容性**：可能是FastMCP升级导致的API变化
3. **检查网络/认证问题**：可能是外部因素

---

## 附录：完整Diff统计

```
变更文件: src/chrome_update_digest/mcp/tools/enhanced_webplatform_digest.py
新增行数: ~400 lines
删除行数: ~50 lines
主要变更区域:
- Import statements (+6 lines) - 新增SamplingMessage, TextContent, ValidationError
- _coerce_model_preferences_for_client() (+38 lines) - 新方法
- _prepare_sampling_messages() (+47 lines) - 新方法
- _convert_content_to_text() (+30 lines) - 新方法
- _safe_sample() (~100 lines modified) - 重大重构
- 多个fallback和compatibility wrapper方法 (+150 lines)
```

---

## 结论

**最可能的根本原因**：`_prepare_sampling_messages()` 方法将原始消息转换为 `SamplingMessage` 对象，这个转换与MCP client期望的格式不兼容。

**推荐修复路径**：
1. 立即实施方案2（Legacy模式开关）恢复功能
2. 使用方案4诊断实际的格式差异
3. 根据诊断结果决定是修复转换逻辑还是永久保留Legacy模式

**风险评估**：
- 方案1（回滚）：低风险，立即有效，但丢失其他改进
- 方案2（Legacy开关）：低风险，提供灵活性，推荐首选
- 方案3（修复转换）：中等风险，需要详细测试
- 方案4（诊断）：无风险，用于调查

---

**分析完成时间**：2025-10-27
**分析基准提交**：667ec39 (24小时前) vs fcba2e8 (HEAD)
