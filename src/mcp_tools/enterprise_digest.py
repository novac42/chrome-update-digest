"""
Enterprise Digest Tool
Generates enterprise-focused Chrome digest from processed release notes
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
from fastmcp import Context


class EnterpriseDigestTool:
    """Tool for generating enterprise Chrome digests"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.processed_path = base_path / "upstream_docs" / "processed_releasenotes" / "processed_forenterprise"
        self.prompt_path = base_path / "prompts" / "enterprise-update-prompt-en.md"
    
    async def _load_prompt_from_resource(self, ctx: Context) -> str:
        """从MCP resource读取enterprise prompt"""
        try:
            # 通过context访问resource而不是直接读取文件
            prompt_resource = await ctx.read_resource("enterprise-prompt")
            # FastMCP返回字符串
            if isinstance(prompt_resource, str):
                return prompt_resource
            else:
                return str(prompt_resource)
        except Exception as e:
            # Fallback to file system if resource fails
            return self._load_prompt_template()
    
    async def _safe_sample_with_retry(self, ctx: Context, messages: str, system_prompt: str, 
                                     max_retries: int = 3, timeout: int = 60) -> str:
        """带重试机制的安全sampling调用"""
        import os
        
        # Get max tokens from environment variable with reasonable default
        max_tokens = int(os.getenv("ENTERPRISE_MAX_TOKENS", "12000"))
        
        for attempt in range(max_retries):
            try:
                # 使用asyncio.wait_for添加超时
                response = await asyncio.wait_for(
                    ctx.sample(
                        messages=messages,
                        system_prompt=system_prompt,
                        model_preferences=["claude-4-sonnet", "gpt5"],
                        temperature=0.7,
                        max_tokens=max_tokens
                    ),
                    timeout=timeout
                )
                
                # FastMCP返回字符串
                if isinstance(response, str):
                    return response
                else:
                    return str(response)
                
            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 指数退避
                    print(f"Sampling timeout, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise Exception("Sampling timed out after all retries")
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Sampling failed: {e}, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise Exception(f"Sampling failed after all retries: {str(e)}")
        
        # This should never be reached, but added for type safety
        raise Exception("Unexpected end of retry loop")
    
    async def _save_digest_to_file(self, content: str, version: Optional[int], channel: str = "stable") -> str:
        """保存digest内容到文件"""
        # 确保输出目录存在
        output_dir = self.base_path / "digest_markdown" / "enterprise"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 构建文件名 - channel后缀是可选的
        if version is None:
            raise ValueError("Version is required for file naming")
        
        # 构建文件名，始终包含channel后缀
        output_path = output_dir / f"digest-chrome-{version}-enterprise-{channel}.md"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return str(output_path)
        except Exception as e:
            raise Exception(f"Failed to save digest to file: {str(e)}")
    
    async def generate_digest_with_sampling(self, ctx: Context, arguments: dict) -> str:
        """使用FastMCP sampling生成enterprise digest"""
        version = arguments.get("version")
        channel = arguments.get("channel", "stable")
        focus_area = arguments.get("focus_area", "all")
        custom_instruction = arguments.get("custom_instruction", "")
        
        try:
            # 从resource读取prompt
            enterprise_prompt = await self._load_prompt_from_resource(ctx)
            
            # 读取数据文件
            processed_data = self._load_processed_data(version)
            
            if not processed_data:
                return json.dumps({
                    "success": False,
                    "error": f"No processed enterprise data found for Chrome {version if version else 'any version'} {channel} channel. This specific channel needs to be processed separately. Do NOT use other channels as alternatives.",
                    "version": version,
                    "channel": channel,
                    "note": f"To process {channel} channel, run: python src/processors/clean_data_pipeline.py --version {version} --channel {channel} --with-yaml"
                })
            
            # 构建用于LLM的内容
            formatted_content = self._format_content_for_llm(
                processed_data, version, focus_area, custom_instruction
            )
            
            # 调用LLM生成digest - 使用详细的system prompt确保严格遵循格式
            system_prompt = """You are a Chrome Update Analyzer specializing in enterprise features. You must STRICTLY follow the provided prompt template format and requirements.

CRITICAL REQUIREMENTS:
1. Follow the EXACT document structure specified in the prompt
2. Use Simplified Chinese for content descriptions, English for headings
3. Use the specified title format with ** markers, not # headers
4. Include ALL required sections as specified in the template
5. Follow the specific markdown formatting rules
6. Never invent your own section structure - use only what's specified in the prompt

CRITICAL CHANNEL RULES:
7. NEVER suggest checking a different channel (beta/dev/canary) when stable is unavailable
8. Each channel (stable, beta, dev) contains DIFFERENT content and release dates - they are NOT interchangeable
9. If requested channel data doesn't exist, only report that channel needs processing - do NOT offer other channels as alternatives

Your task is to analyze the provided Chrome release notes and create a digest that follows the prompt template EXACTLY. Do not deviate from the specified format, structure, or language requirements."""
            
            # 将完整prompt和数据作为user message发送
            full_user_message = f"{enterprise_prompt}\n\n{formatted_content}"
            
            digest_content = await self._safe_sample_with_retry(
                ctx, full_user_message, system_prompt
            )
            
            # 保存到文件
            output_path = await self._save_digest_to_file(digest_content, version, channel)
            
            return json.dumps({
                "success": True,
                "version": version,
                "channel": channel,
                "focus_area": focus_area,
                "output_path": output_path,
                "content_preview": digest_content[:500] + "..." if len(digest_content) > 500 else digest_content,
                "total_length": len(digest_content)
            })
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e),
                "version": version,
                "channel": channel
            })
    
    def _format_content_for_llm(self, data: Dict[str, str], version: Optional[int] = None, 
                               focus_area: str = "all", custom_instruction: str = "") -> str:
        """格式化内容用于LLM处理"""
        content_parts = []
        
        # 强制指示格式要求 
        content_parts.append("MANDATORY FORMAT REQUIREMENTS:")
        content_parts.append("1. Title must use ** format: **Chrome Enterprise Update Watch: Chrome [version]**")
        content_parts.append("2. Use EXACT section structure from prompt:")
        content_parts.append("   # Highlights")
        content_parts.append("   ## Productivity Highlights") 
        content_parts.append("   ## Mobile Enterprise Security Highlights")
        content_parts.append("   ## Mobile Management Highlights")
        content_parts.append("   # Updates by Area")
        content_parts.append("   ## User Productivity Updates on Chrome Desktop")
        content_parts.append("   ### Current Stable Version (Chrome [version])")
        content_parts.append("3. Write content descriptions in Simplified Chinese")
        content_parts.append("4. Keep headings in English")
        content_parts.append("5. If no updates for a section, write '无更新'")
        content_parts.append("")
        
        # 添加版本信息
        if version:
            content_parts.append(f"TARGET VERSION: Chrome {version}")
        
        # 添加焦点区域
        if focus_area != "all":
            focus_descriptions = {
                "productivity": "Focus on user productivity features and workflow improvements",
                "security": "Focus on security enhancements and compliance features", 
                "management": "Focus on enterprise management and policy features"
            }
            content_parts.append(f"FOCUS AREA: {focus_descriptions.get(focus_area, focus_area)}")
        
        # 添加自定义指令
        if custom_instruction:
            content_parts.append(f"ADDITIONAL INSTRUCTIONS: {custom_instruction}")
        
        content_parts.append("\n" + "="*50 + " PROCESSED DATA " + "="*50)
        
        # 添加所有数据文件内容
        for filename, content in data.items():
            content_parts.append(f"\n### FILE: {filename}")
            content_parts.append("-" * 40)
            content_parts.append(content)
            content_parts.append("")
        
        return "\n".join(content_parts)
    
    async def generate_digest(self, arguments: dict) -> str:
        """Generate enterprise digest based on arguments (backward compatibility)"""
        version = arguments.get("version")
        focus_area = arguments.get("focus_area", "all")
        custom_instruction = arguments.get("custom_instruction", "")
        
        # Load the prompt template
        prompt_template = self._load_prompt_template()
        
        # Find and load relevant processed data
        processed_data = self._load_processed_data(version)
        
        if not processed_data:
            return f"No processed enterprise data found for Chrome {version if version else 'any version'}"
        
        # Construct the final prompt
        final_prompt = self._construct_prompt(
            prompt_template,
            processed_data,
            version,
            focus_area,
            custom_instruction
        )
        
        # Generate digest (in real implementation, this would call an LLM)
        digest = self._generate_digest_content(
            final_prompt,
            processed_data,
            version,
            focus_area
        )
        
        return digest
    
    def _load_prompt_template(self) -> str:
        """Load the enterprise prompt template"""
        if self.prompt_path.exists():
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Fallback template
            return """# Chrome Enterprise Update Analyzer
Generate an enterprise-focused digest based on the processed release notes.
Focus on: productivity, security, and management features."""
    
    def _load_processed_data(self, version: Optional[int]) -> Dict[str, str]:
        """Load processed enterprise data"""
        data = {}
        
        if not self.processed_path.exists():
            return data
        
        # Load main processed files
        for file in self.processed_path.glob("*.md"):
            if version:
                # Check if file matches the version
                if f"{version}-" in file.name:
                    with open(file, 'r', encoding='utf-8') as f:
                        data[file.name] = f.read()
            else:
                # Load all available versions
                with open(file, 'r', encoding='utf-8') as f:
                    data[file.name] = f.read()
        
        # Load profile reports if available
        profile_reports_path = self.processed_path / "profile_reports"
        if profile_reports_path.exists():
            for file in profile_reports_path.glob("*.md"):
                if version:
                    if f"chrome-{version}-" in file.name:
                        with open(file, 'r', encoding='utf-8') as f:
                            data[f"profile_reports/{file.name}"] = f.read()
                else:
                    with open(file, 'r', encoding='utf-8') as f:
                        data[f"profile_reports/{file.name}"] = f.read()
        
        return data
    
    def _construct_prompt(self, template: str, data: Dict[str, str], 
                         version: Optional[int], focus_area: str, 
                         custom_instruction: str) -> str:
        """Construct the final prompt for digest generation"""
        prompt_parts = [template]
        
        # Add context about available data
        prompt_parts.append("\n\n## Available Processed Data:")
        for filename in data.keys():
            prompt_parts.append(f"- {filename}")
        
        # Add specific instructions based on parameters
        if version:
            prompt_parts.append(f"\n## Focus Version: Chrome {version}")
        
        if focus_area != "all":
            focus_mapping = {
                "productivity": "User productivity features and enhancements",
                "security": "Security and privacy improvements",
                "management": "Device and policy management features"
            }
            prompt_parts.append(f"\n## Primary Focus Area: {focus_mapping.get(focus_area, focus_area)}")
        
        if custom_instruction:
            prompt_parts.append(f"\n## Additional Instructions:\n{custom_instruction}")
        
        # Add data content
        prompt_parts.append("\n\n## Processed Release Notes Content:")
        for filename, content in data.items():
            prompt_parts.append(f"\n\n### {filename}")
            prompt_parts.append(content)
        
        return "\n".join(prompt_parts)
    
    def _generate_digest_content(self, prompt: str, data: Dict[str, str], 
                                version: Optional[int], focus_area: str) -> str:
        """Generate the actual digest content"""
        # This is a placeholder implementation
        # In a real implementation, this would call an LLM API
        
        # For now, return a structured summary based on available data
        digest_parts = []
        
        # Title
        if version:
            digest_parts.append(f"# Chrome Enterprise Update Watch: Chrome {version}")
        else:
            digest_parts.append("# Chrome Enterprise Update Watch: Multi-Version Summary")
        
        # Highlights section
        digest_parts.append("\n## Highlights")
        
        if focus_area in ["productivity", "all"]:
            digest_parts.append("\n### Productivity Highlights")
            digest_parts.append("- [Generated productivity highlights based on processed data]")
        
        if focus_area in ["security", "all"]:
            digest_parts.append("\n### Mobile Enterprise Security Highlights")
            digest_parts.append("- [Generated security highlights based on processed data]")
        
        if focus_area in ["management", "all"]:
            digest_parts.append("\n### Mobile Management Highlights")
            digest_parts.append("- [Generated management highlights based on processed data]")
        
        # Updates by Area section
        digest_parts.append("\n## Updates by Area")
        
        # Add sections based on available data
        for filename in data.keys():
            if "organized_chromechanges" in filename:
                digest_parts.append(f"\n### Based on {filename}")
                digest_parts.append("- [Extracted key updates from this file]")
        
        # Version comparison if multiple versions
        if len(data) > 1:
            digest_parts.append("\n## Version Comparison Context")
            digest_parts.append("[Analysis of trends across versions]")
        
        # Note about placeholder
        digest_parts.append("\n\n---")
        digest_parts.append("*Note: This is a placeholder digest. In production, this would be generated by an LLM based on the prompt and processed data.*")
        
        return "\n".join(digest_parts)
