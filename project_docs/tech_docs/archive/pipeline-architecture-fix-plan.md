# MCP Server & Pipeline优化计划

**分析日期**: 2025年7月24日  
**问题**: 当前代码实现与预期的pipeline架构不一致  
**影响**: HTML生成包含占位符而非实际内容  
**目标**: 升级为基于FastMCP的现代化MCP服务器架构，集成sampling和resource管理

## 正确的Pipeline架构

### 数据流向
```
upstream_docs/processed_releasenotes/ 
    ↓ (LLM处理 + Prompt)
digest_markdown/ 
    ↓ (Markdown转HTML)
digest_html/
```

### 组件职责

1. **FastMCP Server架构**:
   - **框架**: 使用FastMCP替代传统MCP实现
   - **Sampling集成**: 基于 https://gofastmcp.com/servers/sampling 的LLM调用
   - **Resource管理**: Prompts作为MCP resources进行管理和读取
   - **工具注册**: 统一的工具注册和管理机制

2. **EnterpriseDigestTool & WebplatformDigestTool**:
   - **输入**: `upstream_docs/processed_releasenotes/`
   - **处理**: 使用FastMCP client + Sampling + Prompt resources生成digest
   - **输出**: 保存到 `digest_markdown/`
   - **Prompt来源**: 通过 `mcp.resource` 读取 `prompts/` 目录下的prompt文件

3. **MergedDigestHtmlTool**:
   - **输入**: `digest_markdown/` (已生成的digest文件)
   - **处理**: 纯markdown到HTML转换
   - **输出**: `digest_html/`

4. **Prompt Resource管理**:
   - **Enterprise Prompt**: `prompts/enterprise-update-prompt-en.md`
   - **Webplatform Prompt**: `prompts/chrome-update-analyzer-prompt-webplatform.md`
   - **Profile Keywords**: `prompts/profile-keywords.txt`
   - **访问方式**: 通过MCP resource API统一读取

## 代码检查发现 (2025-07-24)

### 实际代码状态与计划对比

**重要发现**: 通过检查发现 `digest_markdown/` 目录下确实存在真实的digest文件（如 `digest-chrome-138-enterprise.md`），内容是实际的LLM生成结果而非占位符。这表明：

1. **存在外部生成方式**: 真实的digest内容可能通过外部脚本或手动方式生成，而非通过当前的MCP工具
2. **代码与实际脱节**: 当前的工具代码返回占位符文本，与实际存在的真实文件不符
3. **工具缺少保存功能**: 所有digest工具都缺少将生成内容保存到文件的逻辑

### MCP服务器工具注册状态

✅ **MCP服务器实现完整**: `mcp_server.py` 已正确注册所有工具：
- `enterprise-digest` - 企业digest生成
- `webplatform-digest` - Web平台digest生成  
- `split-features-by-heading` - 功能分割
- `merged-digest-html` - 合并HTML生成

✅ **HTML转换器实现完整**: `src/convert_md2html.py` 包含完整的markdown到HTML转换逻辑：
- 章节解析 (`parse_chapters`)
- 内容处理 (`process_content`) 
- 卡片包装 (`wrap_h3_in_cards`)
- 链接处理和模板渲染

### 修复优先级调整

基于代码检查结果，需要调整修复优先级：

**最高优先级**:
1. **添加文件保存功能** - 所有digest工具都缺少保存逻辑
2. **集成真实LLM调用** - 替换占位符文本
3. **重构MergedDigestHtmlTool** - 直接读取已生成的digest文件

## 当前实现问题

### 1. EnterpriseDigestTool 问题
- ✅ **数据源路径**: 修复为 `upstream_docs/processed_releasenotes/processed_forenterprise/`
- ✅ **输出路径**: 添加 `digest_markdown/enterprise/`
- ❌ **LLM调用**: `_generate_digest_content()` 返回占位符文本，缺少真实的MCP client调用 (注：实际存在真实digest文件，可能通过外部方式生成)
- ❌ **文件保存**: 需要在工具内添加自动保存逻辑（目前工具不包含保存功能）

### 2. WebplatformDigestTool 问题  

- ✅ **数据源路径**: 修复为 `upstream_docs/processed_releasenotes/processed_forwebplatform/`
- ✅ **输出路径**: 添加 `digest_markdown/webplatform/`
- ❌ **LLM调用**: `_generate_digest_content()` 返回占位符文本，缺少真实的MCP client调用 (注：实际存在真实digest文件，可能通过外部方式生成)
- ❌ **文件保存**: 需要在工具内添加自动保存逻辑（目前工具不包含保存功能）

### 3. MergedDigestHtmlTool 问题

- ❌ **职责混乱**: 当前试图调用digest工具生成内容，应该直接读取已生成的digest文件
- ❌ **数据源错误**: 应该读取 `digest_markdown/` 而不是调用其他工具
- ❌ **架构违反**: 不应该依赖LLM，应该是纯HTML转换工具

## 修复计划

### 阶段0: FastMCP架构升级 (最高优先级)

#### 0.1 FastMCP Server实现

**新文件**: `fast_mcp_server.py`

**任务**:
- ❌ **安装FastMCP依赖** - 添加fastmcp到requirements.txt
- ❌ **创建FastMCP服务器主文件** - 替代当前的mcp_server.py
- ❌ **集成sampling功能** - 基于 [FastMCP Sampling](https://gofastmcp.com/servers/sampling) 实现LLM调用
- ❌ **配置MCP Resource管理** - 将prompts目录作为resources暴露

**关键实现点**:
```python
# 基于FastMCP的服务器架构
from fastmcp import FastMCP
from fastmcp.resources import FileResource
from fastmcp.sampling import SamplingClient

# Resource配置 - 将prompts作为resources
app.add_resource(
    "enterprise-prompt", 
    FileResource("prompts/enterprise-update-prompt-en.md")
)
app.add_resource(
    "webplatform-prompt", 
    FileResource("prompts/chrome-update-analyzer-prompt-webplatform.md")
)
app.add_resource(
    "profile-keywords", 
    FileResource("prompts/profile-keywords.txt")
)

# Sampling集成
sampling_client = SamplingClient()
```

#### 0.2 Prompt Resource集成

**任务**:
- ❌ **将现有prompt文件注册为MCP resources** - 三个文件需要注册
- ❌ **实现resource读取工具函数** - 统一的prompt读取接口
- ❌ **更新所有digest工具使用resource读取prompts** - 替换硬编码路径

**关键修改点**:
```python
# 替换硬编码路径读取
with open("prompts/enterprise-update-prompt-en.md", "r") as f:
    prompt = f.read()

# 改为resource读取
prompt = await mcp.resource.read("enterprise-prompt")
```

#### 0.3 Sampling集成实现

**任务**:
- ❌ **集成FastMCP sampling客户端** - 替换占位符LLM调用
- ❌ **实现统一的LLM调用接口** - 所有工具共享的sampling方法
- ❌ **添加sampling配置管理** - 模型、温度等参数配置
- ❌ **实现错误处理和重试机制** - 针对sampling调用的错误处理

**关键实现点**:
```python
from fastmcp import FastMCP, Context
from fastmcp.client.sampling import SamplingMessage

# FastMCP服务器初始化
mcp = FastMCP("DigestServer")

# 统一的LLM调用接口
async def call_llm_with_sampling(ctx: Context, prompt: str, content: str, 
                                system_prompt: str = None, 
                                temperature: float = 0.7) -> str:
    """使用FastMCP sampling调用LLM生成digest内容"""
    try:
        # 构建完整的prompt
        full_prompt = f"{prompt}\n\n{content}"
        
        # 调用LLM sampling
        response = await ctx.sample(
            messages=full_prompt,
            system_prompt=system_prompt or "You are an expert technical writer specializing in Chrome browser updates and web platform changes.",
            model_preferences=["claude-4-sonnet", "gpt5"],  # 优先使用Claude Sonnet 4，备选GPT5
            temperature=temperature,
            max_tokens=4000
        )
        
        return response.text
        
    except Exception as e:
        # 错误处理和重试逻辑
        print(f"LLM sampling failed: {e}")
        raise

# 多轮对话的复杂分析（用于需要上下文的digest生成）
async def call_llm_with_context(ctx: Context, prompt: str, content: str, 
                               previous_context: str = None) -> str:
    """使用多轮对话结构进行复杂的digest分析"""
    messages = []
    
    if previous_context:
        messages.extend([
            SamplingMessage(role="user", content=f"Previous context: {previous_context}"),
            SamplingMessage(role="assistant", content="I understand the context. How can I help with the current content?")
        ])
    
    messages.append(SamplingMessage(role="user", content=f"{prompt}\n\n{content}"))
    
    response = await ctx.sample(
        messages=messages,
        system_prompt="You are a Chrome browser expert. Analyze technical changes and create comprehensive digests for different audiences.",
        temperature=0.3,  # 低温度确保一致性
        max_tokens=4000
    )
    
    return response.text
```

### 阶段1: 修复Digest工具的FastMCP集成 (高优先级)

#### 1.1 EnterpriseDigestTool FastMCP集成

**文件**: `src/mcp_tools/enterprise_digest.py`

**任务**:

- ❌ **集成FastMCP sampling客户端** - 替换当前的占位符MCP client调用
- ❌ **使用MCP resource读取enterprise prompt** - 替换硬编码文件读取
- ❌ **实现 `_call_llm_via_sampling()` 方法** - 基于FastMCP sampling的LLM调用
- ❌ **修复 `_generate_digest_content()` 方法使用真实LLM调用** - 集成sampling和resource
- ✅ **添加错误处理和重试机制** - 有基本错误处理框架
- ❌ **确保自动保存到 `digest_markdown/enterprise/`** - 工具本身无保存功能，需要添加

**关键修改点**:
```python
from fastmcp import Context

# 新增: FastMCP resource读取
async def _load_prompt_from_resource(self, ctx: Context) -> str:
    """从MCP resource读取enterprise prompt"""
    # 通过context访问resource而不是直接读取文件
    prompt_resource = await ctx.read_resource("enterprise-prompt")
    return prompt_resource.text

# 新增: FastMCP sampling调用
async def _call_llm_via_sampling(self, ctx: Context, prompt: str, content: str) -> str:
    """使用FastMCP sampling调用LLM"""
    # 构建系统prompt
    system_prompt = """You are an expert technical writer specializing in Chrome browser enterprise features. 
    Create comprehensive, professional digests that help enterprise administrators understand important changes."""
    
    # 使用ctx.sample进行LLM调用
    response = await ctx.sample(
        messages=f"{prompt}\n\n{content}",
        system_prompt=system_prompt,
        model_preferences=["claude-4-sonnet", "gpt5"],
        temperature=0.7,
        max_tokens=4000
    )
    
    return response.text

# 修改: EnterpriseDigestTool工具定义
@mcp.tool
async def enterprise_digest(version: int, channel: str = "stable", 
                          focus_area: str = "all", ctx: Context = None) -> str:
    """Generate enterprise digest using FastMCP sampling and resources"""
    try:
        # 从resource读取prompt
        enterprise_prompt = await _load_prompt_from_resource(ctx)
        
        # 读取数据文件
        data_files = _load_enterprise_data(version, channel)
        formatted_content = _format_content_for_llm(data_files)
        
        # 调用LLM生成digest
        digest_content = await _call_llm_via_sampling(ctx, enterprise_prompt, formatted_content)
        
        # 保存到文件
        output_path = f"digest_markdown/enterprise/digest-chrome-{version}-enterprise.md"
        await _save_digest_to_file(digest_content, output_path)
        
        return json.dumps({
            "success": True,
            "version": version,
            "channel": channel,
            "focus_area": focus_area,
            "output_path": output_path,
            "content_preview": digest_content[:500] + "..."
        })
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })
```

#### 1.2 WebplatformDigestTool FastMCP集成

**文件**: `src/mcp_tools/webplatform_digest.py`

**任务**:

- ❌ **集成FastMCP sampling客户端** - 替换当前的占位符MCP client调用
- ❌ **使用MCP resource读取webplatform prompt** - 替换硬编码文件读取
- ❌ **实现 `_call_llm_via_sampling()` 方法** - 基于FastMCP sampling的LLM调用
- ❌ **修复 `_generate_digest_content()` 方法使用真实LLM调用** - 集成sampling和resource
- ✅ **保持WebGPU merger功能** - WebGPU merger已完整实现
- ✅ **确保自动保存到 `digest_markdown/webplatform/`** - 已有真实digest文件存在

**关键修改点**:
```python
from fastmcp import Context

# 新增: FastMCP resource读取多个prompt文件
async def _load_prompts_from_resources(self, ctx: Context) -> Tuple[str, str]:
    """从MCP resources读取webplatform prompt和profile keywords"""
    # 并行读取多个resource
    webplatform_prompt_resource = await ctx.read_resource("webplatform-prompt")
    profile_keywords_resource = await ctx.read_resource("profile-keywords")
    
    return webplatform_prompt_resource.text, profile_keywords_resource.text

# 修改: WebplatformDigestTool工具定义
@mcp.tool
async def webplatform_digest(version: int, channel: str = "stable", 
                           focus_area: str = "all", ctx: Context = None) -> str:
    """Generate webplatform digest using FastMCP sampling and resources"""
    try:
        # 从resources读取prompts
        webplatform_prompt, profile_keywords = await _load_prompts_from_resources(ctx)
        
        # 读取数据文件（包括WebGPU merger处理）
        data_files = _load_webplatform_data(version, channel)
        formatted_content = _format_content_with_keywords(data_files, profile_keywords)
        
        # 构建针对web平台的系统prompt
        system_prompt = """You are an expert web platform analyst specializing in Chrome browser changes. 
        Focus on web developers' needs and create comprehensive digests about API changes, new features, and deprecations."""
        
        # 调用LLM生成digest
        response = await ctx.sample(
            messages=f"{webplatform_prompt}\n\n{formatted_content}",
            system_prompt=system_prompt,
            model_preferences=["claude-4-sonnet", "gpt5"],
            temperature=0.7,
            max_tokens=4000
        )
        
        digest_content = response.text
        
        # 保存到文件
        output_path = f"digest_markdown/webplatform/digest-chrome-{version}-webplatform-{channel}.md"
        await _save_digest_to_file(digest_content, output_path)
        
        return json.dumps({
            "success": True,
            "version": version,
            "channel": channel,
            "focus_area": focus_area,
            "output_path": output_path,
            "content_preview": digest_content[:500] + "..."
        })
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })
```

### 阶段2: 重构MergedDigestHtmlTool (高优先级)

#### 2.1 简化MergedDigestHtmlTool职责

**文件**: `src/mcp_tools/merged_digest_html.py`

**任务**:

- ❌ **移除对EnterpriseDigestTool和WebplatformDigestTool的依赖** - 当前仍在直接调用这些工具
- ❌ **添加直接读取 `digest_markdown/` 文件的逻辑** - 缺少此功能
- ✅ **简化为纯markdown到HTML转换工具** - HTML转换逻辑已实现
- ❌ **添加文件不存在时的错误处理** - 需要增强错误处理

**关键修改点**:
```python
# 当前错误的做法:
enterprise_content = await self.enterprise_tool.generate_digest(enterprise_args)
webplatform_content = await self.webplatform_tool.generate_digest(webplatform_args)

# 应该改为:
enterprise_content = self._read_digest_file("enterprise", version, channel)
webplatform_content = self._read_digest_file("webplatform", version, channel)
```

#### 2.2 添加Digest文件读取逻辑

**任务**:

- ❌ **实现 `_read_digest_file()` 方法** - 需要新增此方法直接读取markdown文件
- ❌ **添加文件存在性检查** - 需要检查digest文件是否存在
- ❌ **提供清晰的错误信息当digest文件不存在时** - 需要改善错误提示
- ❌ **支持fallback到生成新digest的选项** - 可选功能

### 阶段3: 端到端工作流程 (中优先级)

#### 3.1 创建工作流程协调器
**新文件**: `src/mcp_tools/digest_workflow.py`

**目标**: 提供完整的端到端digest生成工作流程

**功能**:
- [ ] 检查processed_releasenotes是否有新数据
- [ ] 自动调用digest工具生成markdown
- [ ] 自动调用HTML工具生成最终HTML
- [ ] 提供批量处理多个版本的能力

#### 3.2 改进MCP工具注册
**文件**: `mcp_server.py`

**任务**:
- [ ] 添加workflow工具注册
- [ ] 提供端到端的HTML生成工具
- [ ] 保持现有的独立工具访问

### 阶段4: 优化和测试 (低优先级)

#### 4.1 添加测试覆盖
- [ ] 为digest工具添加LLM mock测试
- [ ] 为HTML工具添加markdown处理测试  
- [ ] 添加端到端集成测试

#### 4.2 性能优化
- [ ] 添加digest文件缓存机制  
- [ ] 优化大文件处理
- [ ] 添加并行处理支持

## 实施优先级

### 最高优先级 - FastMCP架构升级

1. **安装和配置FastMCP框架**
2. **实现FastMCP服务器和Resource管理**  
3. **集成Sampling功能用于LLM调用**
4. **将prompts文件注册为MCP resources**

### 立即执行 - 工具升级

1. **升级EnterpriseDigestTool为FastMCP架构**
2. **升级WebplatformDigestTool为FastMCP架构**  
3. **重构MergedDigestHtmlTool去除对digest工具的依赖**

### 然后执行 - 验证和优化

4. **测试完整pipeline流程**
5. **添加错误处理和用户反馈**

### 再执行 - 扩展功能

6. **创建基于FastMCP的工作流程协调器**
7. **优化用户体验和性能**

## 验证标准

修复完成后，系统应该满足：

1. **EnterpriseDigestTool**:
   - 读取 `upstream_docs/processed_releasenotes/processed_forenterprise/138-organized_chromechanges-enterprise.md`
   - 通过LLM生成enterprise digest
   - 保存到 `digest_markdown/enterprise/digest-chrome-138-enterprise.md`

2. **WebplatformDigestTool**:
   - 读取 `upstream_docs/processed_releasenotes/processed_forwebplatform/138-webplatform-with-webgpu.md`
   - 通过LLM生成webplatform digest
   - 保存到 `digest_markdown/webplatform/digest-chrome-138-webplatform-stable.md`

3. **MergedDigestHtmlTool**:
   - 读取 `digest_markdown/enterprise/digest-chrome-138-enterprise.md`
   - 读取 `digest_markdown/webplatform/digest-chrome-138-webplatform-stable.md`
   - 转换为HTML并保存到 `digest_html/chrome-138-merged-digest-stable.html`

4. **最终HTML**:
   - 包含真实的digest内容而不是占位符
   - 正确的章节结构和格式
   - 可用的交互式界面

## 风险评估

- **低风险**: 数据文件结构清晰，架构设计合理
- **中风险**: 需要集成MCP client的LLM调用
- **高风险**: 确保LLM输出的格式符合HTML转换需求

## 相关文件

### 需要创建的文件

- `fast_mcp_server.py` - 新的FastMCP服务器主文件
- `requirements.txt` - 添加fastmcp依赖

### 需要修改的文件

- `src/mcp_tools/enterprise_digest.py` - 升级为FastMCP + sampling + resource
- `src/mcp_tools/webplatform_digest.py` - 升级为FastMCP + sampling + resource
- `src/mcp_tools/merged_digest_html.py` - 重构为纯HTML转换工具

### 数据文件路径

- **输入**: `upstream_docs/processed_releasenotes/`
- **中间产物**: `digest_markdown/`
- **最终输出**: `digest_html/`

### Prompt Resource文件

- `prompts/enterprise-update-prompt-en.md` - Enterprise digest生成prompt
- `prompts/chrome-update-analyzer-prompt-webplatform.md` - Webplatform digest生成prompt
- `prompts/profile-keywords.txt` - Profile特性关键词

### FastMCP配置

- **框架**: FastMCP 2.0.0+ (支持LLM sampling功能)
- **Sampling API**: 基于 `ctx.sample()` 的LLM调用接口
- **Resource管理**: Prompts作为MCP resources通过 `ctx.read_resource()` 访问
- **工具注册**: 使用 `@mcp.tool` 装饰器进行统一工具管理
- **客户端要求**: 客户端必须实现sampling handlers才能支持LLM调用

**完整的FastMCP服务器示例**:
```python
from fastmcp import FastMCP, Context
from pathlib import Path

# 初始化FastMCP服务器
mcp = FastMCP("DigestServer")

# 注册prompt resources
mcp.add_resource(
    "enterprise-prompt",
    uri="file:///prompts/enterprise-update-prompt-en.md",
    name="Enterprise Update Prompt",
    description="Prompt for generating enterprise Chrome digest",
    mimeType="text/markdown"
)

mcp.add_resource(
    "webplatform-prompt", 
    uri="file:///prompts/chrome-update-analyzer-prompt-webplatform.md",
    name="WebPlatform Update Prompt",
    description="Prompt for generating web platform Chrome digest",
    mimeType="text/markdown"
)

mcp.add_resource(
    "profile-keywords",
    uri="file:///prompts/profile-keywords.txt", 
    name="Profile Keywords",
    description="Keywords for identifying profile-related features",
    mimeType="text/plain"
)

# 工具注册将在各个工具文件中使用@mcp.tool装饰器完成

if __name__ == "__main__":
    mcp.run()
```

**依赖要求**:
```txt
fastmcp>=2.0.0
# 其他现有依赖...
```

## 关键TODO清单

### ❌ 最高优先级 - FastMCP架构升级

1. **FastMCP服务器实现**
   - [ ] 安装FastMCP依赖到requirements.txt
   - [ ] 创建fast_mcp_server.py替代mcp_server.py
   - [ ] 集成sampling功能基于 <https://gofastmcp.com/servers/sampling>
   - [ ] 配置MCP Resource管理系统

2. **Prompt Resource管理**
   - [ ] 将enterprise-update-prompt-en.md注册为MCP resource
   - [ ] 将chrome-update-analyzer-prompt-webplatform.md注册为MCP resource
   - [ ] 将profile-keywords.txt注册为MCP resource
   - [ ] 实现统一的resource读取接口

3. **Sampling集成**
   - [ ] 实现基于FastMCP的LLM调用客户端
   - [ ] 配置sampling参数（模型、温度、tokens等）
   - [ ] 添加sampling错误处理和重试机制

### ❌ 高优先级 - 工具升级

1. **EnterpriseDigestTool FastMCP升级**
   - [ ] 集成FastMCP sampling客户端
   - [ ] 使用MCP resource读取enterprise prompt
   - [ ] 实现真实的LLM调用替换占位符文本
   - [ ] 添加自动保存到 `digest_markdown/enterprise/` 的功能

2. **WebplatformDigestTool FastMCP升级**
   - [ ] 集成FastMCP sampling客户端
   - [ ] 使用MCP resource读取webplatform prompt和keywords
   - [ ] 实现真实的LLM调用替换占位符文本
   - [ ] 添加自动保存到 `digest_markdown/webplatform/` 的功能

3. **MergedDigestHtmlTool架构重构**
   - [ ] 移除对digest工具的直接依赖
   - [ ] 实现 `_read_digest_file()` 方法直接读取markdown文件
   - [ ] 添加文件不存在时的清晰错误处理

### ✅ 已完成项目

- ✅ MCP服务器工具注册完整
- ✅ HTML转换器实现完整
- ✅ WebGPU merger功能完整
- ✅ 数据源路径配置正确
- ✅ 输出目录结构正确
- ✅ 真实digest文件存在（通过外部方式生成）

### ❓ 需要调查的问题

- [ ] 验证FastMCP与现有MCP架构的兼容性
- [ ] 确定sampling配置的最佳参数
- [ ] 测试resource读取的性能影响
- [ ] 检查现有digest文件格式是否符合新架构要求

## 下一步行动

1. 首先安装FastMCP并创建新的服务器架构
2. 实现prompt files作为MCP resources的管理
3. 集成sampling功能替换占位符LLM调用
4. 升级EnterpriseDigestTool和WebplatformDigestTool使用FastMCP
5. 重构MergedDigestHtmlTool，使其直接读取digest_markdown文件
6. 测试完整的FastMCP-based pipeline流程
7. 验证生成的HTML包含真实内容
