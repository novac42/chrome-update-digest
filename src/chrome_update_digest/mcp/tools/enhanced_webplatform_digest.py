"""
Enhanced WebPlatform Digest Tool with deterministic link extraction.
Uses script-based extraction for 100% link accuracy.
"""

import asyncio
import json
import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

try:  # Optional dependency; guards ValidationError handling
    from pydantic import ValidationError as PydanticValidationError
except Exception:  # pragma: no cover - keep runtime resilient if pydantic missing
    PydanticValidationError = None

from fastmcp import Context
from fastmcp.server.context import SamplingMessage, TextContent
from chrome_update_digest.utils.yaml_pipeline import YAMLPipeline
from chrome_update_digest.utils.focus_area_manager import FocusAreaManager
from chrome_update_digest.utils.telemetry import DigestTelemetry
from chrome_update_digest.utils.project_paths import PROJECT_ROOT
from chrome_update_digest.mcp.tools._digest_yaml_cache import DigestYAMLCache
from chrome_update_digest.mcp.tools._digest_generation import DigestGenerationEngine
from chrome_update_digest.mcp.tools._digest_io import DigestIOManager
from chrome_update_digest.mcp.tools._digest_config import DigestRunConfig
from chrome_update_digest.mcp.tools._digest_area_runner import AreaRunner


class EnhancedWebplatformDigestTool:
    """
    Enhanced MCP tool for WebPlatform digest generation.
    
    Key improvements:
    1. Deterministic link extraction (100% accuracy)
    2. YAML intermediate format
    3. Focus area filtering
    4. Tag-based organization
    """
    
    def __init__(self, base_path: Optional[Path] = None):
        """Initialize the enhanced tool."""
        # Use provided base_path or default to repository root
        if base_path is None:
            base_path = PROJECT_ROOT
        self.base_path = base_path
        
        self.yaml_pipeline = YAMLPipeline()
        self.focus_manager = FocusAreaManager(self.base_path / 'config' / 'focus_areas.yaml')
        # Update cache directory to match new structure
        self.cache_dir = self.base_path / 'upstream_docs' / 'processed_releasenotes' / 'processed_forwebplatform'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.yaml_cache = DigestYAMLCache(self.base_path, self.cache_dir, self.yaml_pipeline)
        # Digest output directory
        self.digest_dir = self.base_path / 'digest_markdown' / 'webplatform'
        self.digest_dir.mkdir(parents=True, exist_ok=True)
        # Telemetry recorder for Prometheus metrics and structured events
        self.telemetry = DigestTelemetry(self.base_path)
        self.generation = DigestGenerationEngine(self.base_path, self.focus_manager, self._safe_sample_with_retry)
        self.io = DigestIOManager(self.base_path, self.digest_dir, self.telemetry)
        # Run-scoped configuration (populated for each invocation)
        self._current_run_config: Optional[DigestRunConfig] = None
        # M2: concurrency and rate governance
        self._max_concurrency: int = int(os.getenv("WEBPLATFORM_MAX_CONCURRENCY", "1"))
        self._rate_limit_per_sec: float = float(os.getenv("WEBPLATFORM_RATE_LIMIT", "2"))
        self._failure_cooldown_sec: float = float(os.getenv("WEBPLATFORM_FAILURE_COOLDOWN", "5"))
        self._circuit_breaker_threshold: int = int(os.getenv("WEBPLATFORM_CIRCUIT_THRESHOLD", "3"))
        self._recent_failures: int = 0
        self._last_failure_ts: float = 0.0
        self._semaphore = asyncio.Semaphore(self._max_concurrency)
        self._last_token_ts: float = 0.0

    def _resolve_model_preferences(
        self,
        explicit_preferences: Optional[Union[Dict[str, Any], List[Any], str]],
        explicit_model: Optional[str]
    ) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """Determine the model preference payload for sampling requests.

        Resolution order:
        1) Explicit structured preferences
        2) Explicit model name
        3) WEBPLATFORM_MODEL_PREFERENCES (JSON or shorthand)
        4) WEBPLATFORM_MODEL (shorthand)
        5) WEBPLATFORM_DEFAULT_MODEL (shorthand)
        6) Built-in fallback: copilot/gpt-5-mini
        """
        preference_source: Optional[Union[Dict[str, Any], List[Any], str]] = explicit_preferences

        # Direct model override takes effect only when full preferences are not provided
        if preference_source is None and explicit_model:
            preference_source = {"model": explicit_model}

        # Allow environment configuration in the absence of explicit hints
        if preference_source is None:
            env_payload = os.getenv("WEBPLATFORM_MODEL_PREFERENCES")
            if env_payload:
                preference_source = env_payload
            else:
                env_model = os.getenv("WEBPLATFORM_MODEL")
                if env_model:
                    preference_source = env_model

        normalized = self._normalize_model_preferences(preference_source)

        # Final fallback to ensure a concrete model is always provided to the client
        if normalized is None:
            default_model = os.getenv("WEBPLATFORM_DEFAULT_MODEL", "copilot/gpt-5-mini").strip()
            if default_model:
                normalized = {"model": default_model}

        return normalized

    def _normalize_model_preferences(
        self,
        value: Optional[Union[Dict[str, Any], List[Any], str]]
    ) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """Normalize incoming model preference configuration into dict/list payloads."""
        if value is None:
            return None

        if isinstance(value, str):
            candidate = value.strip()
            if not candidate:
                return None
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                # Treat plain string as shorthand for {"model": "..."}
                return {"model": candidate}
            else:
                return self._normalize_model_preferences(parsed)

        if isinstance(value, dict):
            return value if value else None

        if isinstance(value, list):
            return value if value else None

        # Unsupported types are ignored silently to avoid breaking the run
        return None

    def _sanitize_preparation_notice(self, notice: Dict[str, Any]) -> Dict[str, Any]:
        """Shape regeneration notices into a compact, user-facing payload."""
        if not notice:
            return {}

        sanitized = {
            "step": notice.get("step", "clean_data_pipeline_run"),
            "triggered": bool(notice.get("triggered")),
            "success": bool(notice.get("success")),
            "areas_missing": list(notice.get("areas_missing", [])),
            "message": notice.get("message"),
            "version": notice.get("version"),
            "channel": notice.get("channel"),
        }

        details = notice.get("details")
        if isinstance(details, dict):
            sanitized["details"] = details

        return sanitized

    def _attach_preparation_notice(
        self,
        payload: Dict[str, Any],
        notice: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Attach regeneration notice to outgoing payload if present."""
        if not payload or not notice or not notice.get("triggered"):
            return payload

        payload.setdefault("preparation_steps", []).append(
            self._sanitize_preparation_notice(notice)
        )
        return payload

    def _sampling_payload_preview(
        self,
        messages: Union[str, Sequence[Any]],
        limit: int = 400,
    ) -> str:
        """Return a compact preview of the sampling payload for telemetry."""
        if isinstance(messages, str):
            return messages[:limit]
        try:
            serialized = json.dumps(messages, ensure_ascii=False)
        except Exception:
            serialized = str(messages)
        return serialized[:limit]

    @property
    def _run_model_preferences(self) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """Return model preferences scoped to the active run (if any)."""
        if self._current_run_config:
            return self._current_run_config.model_preferences
        return None

    @contextmanager
    def run_context(self, run_config: DigestRunConfig):
        """Context manager to apply run-scoped configuration safely."""
        previous = self._current_run_config
        self._current_run_config = run_config
        try:
            yield
        finally:
            self._current_run_config = previous

    def _prepare_sampling_messages(
        self,
        messages: Union[str, Sequence[Union[str, SamplingMessage, Dict[str, Any]]]],
    ) -> Union[str, Sequence[Union[str, SamplingMessage]]]:
        """Normalize sampling payloads to structures accepted by FastMCP 2.x."""
        if isinstance(messages, str):
            return [
                SamplingMessage(
                    role="user",
                    content=TextContent(type="text", text=messages),
                )
            ]

        if isinstance(messages, SamplingMessage):
            return [messages]

        if isinstance(messages, Sequence):
            normalized: List[Union[str, SamplingMessage]] = []
            for entry in messages:
                if isinstance(entry, (str, SamplingMessage)):
                    normalized.append(entry)
                    continue

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
                        continue

                    normalized.append(json.dumps(entry, ensure_ascii=False))
                    continue

                normalized.append(str(entry))

            return normalized

        return str(messages)

    def _convert_content_to_text(
        self,
        content: Any,
    ) -> Optional[TextContent]:
        """Convert mixed content payloads into TextContent blocks when possible."""
        if content is None:
            return None

        if isinstance(content, TextContent):
            return content

        if isinstance(content, str):
            return TextContent(type="text", text=content)

        if isinstance(content, dict):
            content_type = content.get("type")
            if content_type in (None, "text"):
                text = content.get("text")
                if isinstance(text, str):
                    return TextContent(type="text", text=text)
            return None

        if isinstance(content, Sequence):
            text_parts: List[str] = []
            for block in content:
                if isinstance(block, str):
                    text_parts.append(block)
                elif isinstance(block, dict):
                    block_type = block.get("type")
                    if block_type in (None, "text") and isinstance(block.get("text"), str):
                        text_parts.append(block["text"])
            if text_parts:
                return TextContent(type="text", text="\n".join(text_parts))

        return None
    
    async def run(
        self,
        ctx: Context,
        version: str = "138",
        channel: str = "stable",
        focus_areas: Optional[str] = None,
        use_cache: bool = True,
        language: Optional[str] = None,
        split_by_area: bool = True,
        target_area: Optional[str] = None,
        debug: bool = False,
        model: Optional[str] = None,
        model_preferences: Optional[Union[Dict[str, Any], List[Any], str]] = None
    ) -> str:
        """
        Generate WebPlatform digest with enhanced extraction.
        
        Args:
            ctx: FastMCP context
            version: Chrome version
            channel: Release channel
            focus_areas: Comma-separated focus areas (e.g., "ai,webgpu,security")
            use_cache: Whether to use cached YAML if available
            language: Output language ("en", "zh", or None for both)
            split_by_area: Whether to generate separate digests for each area (default: True)
            target_area: Specific area to analyze (e.g., "css", "webapi", "security")
            debug: Enable debug output
            model: Optional short-hand to set preferred model (overridden by model_preferences)
            model_preferences: Optional structured model preferences payload passed to ctx.sample
            
        Returns:
            Generated digest in markdown format or JSON with per-area results
        """
        regeneration_notice: Optional[Dict[str, Any]] = None

        try:
            # Parse focus areas
            focus_area_list = []
            if focus_areas:
                focus_area_list = [area.strip() for area in focus_areas.split(',')]
                if debug:
                    print(f"Filtering by focus areas: {focus_area_list}")

            run_config = DigestRunConfig(
                version=version,
                channel=channel,
                language=language,
                split_by_area=split_by_area,
                target_area=target_area,
                model_preferences=self._resolve_model_preferences(
                    explicit_preferences=model_preferences,
                    explicit_model=model,
                ),
                explicit_model=model,
            )
            self._current_run_config = run_config

            if debug:
                if run_config.model_preferences:
                    print(f"Using model preferences: {run_config.model_preferences}")
                else:
                    print("No explicit model preferences provided; deferring to client defaults")
            
            # Step 1: Get or generate YAML data
            yaml_data = await self._get_yaml_data(
                ctx,
                version,
                channel,
                use_cache,
                split_by_area,
                target_area,
                debug,
            )
            regeneration_notice = self.yaml_cache.consume_last_regeneration_notice()
            
            if not yaml_data:
                payload = {
                    "success": False,
                    "error": f"Release notes for Chrome {version} {channel} channel not found. This specific channel needs to be processed separately. Do NOT use other channels as alternatives.",
                    "version": version,
                    "channel": channel,
                    "note": f"To process {channel} channel, run: python src/processors/clean_data_pipeline.py --version {version} --channel {channel} --with-yaml"
                }
                self._attach_preparation_notice(payload, regeneration_notice)
                return json.dumps(payload, ensure_ascii=False)
            
            # Step 2: Apply focus area filtering if specified
            if focus_area_list:
                yaml_data = self.yaml_pipeline.filter_by_focus_areas(
                    yaml_data, focus_area_list
                )
                if debug:
                    filtered_count = len(yaml_data.get('features', []))
                    print(f"Filtered to {filtered_count} features")
            
            # Step 3: Handle per-area generation if split_by_area is True
            if split_by_area:
                return await self._generate_per_area_digests(
                    ctx,
                    yaml_data,
                    version,
                    channel,
                    language,
                    debug,
                    run_config,
                    regeneration_notice,
                )
            
            # Step 4: Generate digest from YAML data with language support
            # Default to generating both languages if not specified
            if run_config.language in (None, 'bilingual'):
                # Generate both EN and ZH versions
                try:
                    digest_en = await self._generate_digest_from_yaml(ctx, yaml_data, 'en', target_area, debug)
                    digest_path_en = await self.io.persist_output(
                        version=version,
                        channel=channel,
                        language='en',
                        content=digest_en,
                        area=target_area,
                        debug=debug,
                    )
                except Exception as e:
                    payload = {
                        "success": False,
                        "error": f"Failed to generate English digest: {str(e)}",
                        "version": version,
                        "channel": channel,
                        "language": "en",
                        "target_area": target_area
                    }
                    self._attach_preparation_notice(payload, regeneration_notice)
                    return json.dumps(payload, ensure_ascii=False)
                
                try:
                    digest_zh = await self._generate_digest_from_yaml(ctx, yaml_data, 'zh', target_area, debug)
                    digest_path_zh = await self.io.persist_output(
                        version=version,
                        channel=channel,
                        language='zh',
                        content=digest_zh,
                        area=target_area,
                        debug=debug,
                    )
                except Exception as e:
                    payload = {
                        "success": False,
                        "error": f"Failed to generate Chinese digest: {str(e)}",
                        "version": version,
                        "channel": channel,
                        "language": "zh",
                        "target_area": target_area
                    }
                    self._attach_preparation_notice(payload, regeneration_notice)
                    return json.dumps(payload, ensure_ascii=False)
                
                # Return structured success response
                payload = {
                    "success": True,
                    "version": version,
                    "channel": channel,
                    "language": "bilingual",
                    "target_area": target_area,
                    "output_paths": {
                        "en": str(digest_path_en),
                        "zh": str(digest_path_zh)
                    },
                    "content_preview": {
                        "en": digest_en[:300] + "..." if len(digest_en) > 300 else digest_en,
                        "zh": digest_zh[:300] + "..." if len(digest_zh) > 300 else digest_zh
                    },
                    "total_length": {
                        "en": len(digest_en),
                        "zh": len(digest_zh)
                    }
                }
                self._attach_preparation_notice(payload, regeneration_notice)
                return json.dumps(payload, ensure_ascii=False)
            else:
                # Single language mode
                digest = await self._generate_digest_from_yaml(ctx, yaml_data, language, target_area, debug)
                
                # Save digest to file with area-based folder structure
                digest_path = await self.io.persist_output(
                    version=version,
                    channel=channel,
                    language=language,
                    content=digest,
                    area=target_area,
                    debug=debug,
                )
                if debug:
                    print(f"Digest saved to: {digest_path}")
                
                # Return structured success response
                payload = {
                    "success": True,
                    "version": version,
                    "channel": channel,
                    "language": language,
                    "target_area": target_area,
                    "output_path": str(digest_path),
                    "content_preview": digest[:500] + "..." if len(digest) > 500 else digest,
                    "total_length": len(digest)
                }
                self._attach_preparation_notice(payload, regeneration_notice)
                return json.dumps(payload, ensure_ascii=False)
            
        except Exception as e:
            # Return structured error response
            payload = {
                "success": False,
                "error": str(e),
                "version": version,
                "channel": channel,
                "language": language,
                "target_area": target_area
            }
            self._attach_preparation_notice(payload, regeneration_notice)
            return json.dumps(payload, ensure_ascii=False)
        finally:
            # Ensure run-scoped config is cleared even if errors occur
            self._current_run_config = None
    
    
    
    
    
    async def _safe_sample_with_retry(
        self,
        ctx: Context,
        messages: str,
        system_prompt: str,
        debug: bool,
        max_retries: int = 3,
        timeout: int = 120,
        telemetry_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Safe sampling with exponential backoff retry and timeout, plus M2 governance.
        
        Args:
            ctx: FastMCP context
            messages: User message as string
            system_prompt: System prompt as separate parameter
            debug: Debug mode
            max_retries: Maximum number of retry attempts
            timeout: Timeout in seconds for each attempt
            telemetry_context: Optional metadata used for telemetry
            
        Returns:
            Generated digest content or raises exception
        """
        import asyncio
        import time

        telemetry_context = telemetry_context or {}
        operation = telemetry_context.get("operation", "llm_sampling")
        context_extra = {
            key: value
            for key, value in telemetry_context.items()
            if key not in {"operation"}
        }
        model_hint = telemetry_context.get("model")
        run_preferences = self._run_model_preferences
        if not model_hint and isinstance(run_preferences, dict):
            model_hint = run_preferences.get("model")

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

        # Allow timeout override from environment
        try:
            env_timeout = os.getenv("WEBPLATFORM_SAMPLING_TIMEOUT")
            eff_timeout = int(env_timeout) if env_timeout else int(timeout)
        except Exception:
            eff_timeout = int(timeout)

        # Fixed max tokens for sampling per server configuration
        max_tokens = 60000

        for attempt in range(max_retries):
            attempt_number = attempt + 1
            attempt_start = time.perf_counter()
            try:
                if debug:
                    print(f"Sampling attempt {attempt_number}/{max_retries}... (max_tokens={max_tokens})")

                # Circuit breaker cooldown when too many recent failures
                if self._recent_failures >= self._circuit_breaker_threshold:
                    since_last = time.perf_counter() - self._last_failure_ts
                    if since_last < self._failure_cooldown_sec:
                        if debug:
                            remaining = self._failure_cooldown_sec - since_last
                            print(
                                "Circuit breaker active; sleeping for "
                                f"{remaining:.2f}s before retry"
                            )
                        await asyncio.sleep(self._failure_cooldown_sec - since_last)

                # Rate limiting between calls
                min_interval = 1.0 / max(1e-6, self._rate_limit_per_sec)
                wait_needed = max(0.0, (self._last_token_ts + min_interval) - time.perf_counter())
                if wait_needed > 0:
                    if debug:
                        print(f"Rate limit enforced; waiting {wait_needed:.2f}s before sampling")
                    await asyncio.sleep(wait_needed)

                sample_kwargs = {
                    "messages": self._prepare_sampling_messages(messages),
                    "system_prompt": system_prompt,
                    "temperature": 0.7,
                    "max_tokens": max_tokens,
                }

                if run_preferences:
                    sample_kwargs["model_preferences"] = run_preferences

                payload_preview = self._sampling_payload_preview(sample_kwargs["messages"])

                self.telemetry.log_event(
                    "llm_sampling_attempt_start",
                    {
                        "operation": operation,
                        "attempt": attempt_number,
                        "model": model_hint,
                        "has_model_preferences": bool(run_preferences),
                        "payload_preview": payload_preview,
                    },
                )

                if debug:
                    print(
                        "Prepared sampling payload preview: "
                        f"{payload_preview}"
                    )
                    if run_preferences:
                        print(
                            "Applying model preferences: "
                            f"{json.dumps(run_preferences, ensure_ascii=False)}"
                        )

                async with self._semaphore:
                    response = await asyncio.wait_for(
                        sample_fn(**sample_kwargs),
                        timeout=eff_timeout,
                    )
                self._last_token_ts = time.perf_counter()
                duration = time.perf_counter() - attempt_start

                if isinstance(response, str):
                    result = response
                elif hasattr(response, 'content'):
                    result = response.content
                elif hasattr(response, 'text'):
                    result = response.text
                else:
                    result = str(response)

                self.telemetry.observe_llm_attempt(
                    operation=operation,
                    attempt=attempt_number,
                    duration_seconds=duration,
                    status="success",
                    model=model_hint,
                    extra={**context_extra, "max_retries": max_retries},
                )
                self.telemetry.log_event(
                    "llm_sampling_attempt_complete",
                    {
                        "operation": operation,
                        "attempt": attempt_number,
                        "status": "success",
                        "duration_ms": round(duration * 1000, 2),
                    },
                )
                if debug:
                    print("Successfully generated digest")
                    if isinstance(result, str):
                        print(
                            "Truncated digest output preview: "
                            f"{result[:200]}"
                        )
                # reset failure window
                self._recent_failures = 0
                return result

            except asyncio.TimeoutError as e:
                duration = time.perf_counter() - attempt_start
                self.telemetry.observe_llm_attempt(
                    operation=operation,
                    attempt=attempt_number,
                    duration_seconds=duration,
                    status="timeout",
                    model=model_hint,
                    extra={**context_extra, "max_retries": max_retries},
                )
                self.telemetry.log_event(
                    "llm_sampling_attempt_complete",
                    {
                        "operation": operation,
                        "attempt": attempt_number,
                        "status": "timeout",
                        "duration_ms": round(duration * 1000, 2),
                        "timeout_seconds": eff_timeout,
                    },
                )
                self._recent_failures += 1
                self._last_failure_ts = time.perf_counter()
                self.telemetry.record_error(
                    operation=operation,
                    kind="TimeoutError",
                    detail=str(e) or "LLM sampling timeout",
                    area=context_extra.get("area"),
                )
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    if debug:
                        print(f"Sampling timeout, retrying in {wait_time}s (attempt {attempt_number}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                raise Exception(f"Sampling timed out after {max_retries} retries")

            except Exception as e:
                duration = time.perf_counter() - attempt_start
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

                self.telemetry.observe_llm_attempt(
                    operation=operation,
                    attempt=attempt_number,
                    duration_seconds=duration,
                    status="error",
                    model=model_hint,
                    extra={**context_extra, "max_retries": max_retries, "error": str(e)[:200]},
                )
                self.telemetry.record_error(
                    operation=operation,
                    kind="ValidationError" if is_validation_error else type(e).__name__,
                    detail=str(e),
                    area=context_extra.get("area"),
                )
                self.telemetry.log_event(
                    "llm_sampling_attempt_complete",
                    {
                        "operation": operation,
                        "attempt": attempt_number,
                        "status": "error",
                        "duration_ms": round(duration * 1000, 2),
                        "error": str(e),
                        "payload_preview": payload_preview,
                    },
                )
                self._recent_failures += 1
                self._last_failure_ts = time.perf_counter()
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    if debug:
                        print(f"Sampling failed: {e}, retrying in {wait_time}s (attempt {attempt_number}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                raise Exception(f"Sampling failed after {max_retries} retries: {str(e)}")
        
        raise Exception("Unexpected end of retry loop")
    
    def _generate_fallback_digest(self, yaml_data: Dict, language: str = 'en') -> str:
        """Generate a basic digest without LLM."""
        version = yaml_data.get('version', 'Unknown')
        date_str = datetime.now().strftime('%Y-%m-%d')
        stats = yaml_data.get('statistics', {})
        total_features = stats.get('total_features', 0)
        total_links = stats.get('total_links', 0)
        
        if language == 'zh':
            lines = [
                f"# Chrome {version} WebPlatform 摘要",
                f"\n*生成日期: {date_str}*",
                "\n## 摘要"
            ]
            lines.append(f"此版本包含 {total_features} 个功能特性和 {total_links} 个参考链接。")
        else:
            lines = [
                f"# Chrome {version} WebPlatform Digest",
                f"\n*Generated: {date_str}*",
                "\n## Summary"
            ]
            lines.append(f"This release includes {total_features} features with {total_links} reference links.")
        
        # Group features by primary tag
        features_by_tag = {}
        for feature in yaml_data.get('features', []):
            tags = feature.get('primary_tags', [])
            if tags:
                tag_name = tags[0].get('name') if isinstance(tags[0], dict) else str(tags[0])
                if tag_name not in features_by_tag:
                    features_by_tag[tag_name] = []
                features_by_tag[tag_name].append(feature)
            else:
                if 'uncategorized' not in features_by_tag:
                    features_by_tag['uncategorized'] = []
                features_by_tag['uncategorized'].append(feature)
        
        # Output features by category
        for tag, features in features_by_tag.items():
            if language == 'zh':
                # Translate common tags to Chinese
                tag_translations = {
                    'css': 'CSS 特性',
                    'webapi': 'Web API',
                    'javascript': 'JavaScript',
                    'graphics-webgpu': '图形与 WebGPU',
                    'security-privacy': '安全与隐私',
                    'performance': '性能优化',
                    'multimedia': '多媒体',
                    'devices': '设备接口',
                    'pwa-service-worker': 'PWA 与 Service Worker',
                    'webassembly': 'WebAssembly',
                    'deprecations': '弃用特性',
                    'uncategorized': '未分类'
                }
                tag_display = tag_translations.get(tag.lower(), tag.title())
            else:
                tag_display = tag.title()
            
            lines.append(f"\n## {tag_display}")
            
            for feature in features:
                lines.append(f"\n### {feature.get('title', 'Untitled')}")
                
                content = feature.get('content', '').strip()
                if content:
                    lines.append(content)
                
                links = feature.get('links', [])
                if links:
                    if language == 'zh':
                        lines.append("\n**参考资料:**")
                    else:
                        lines.append("\n**References:**")
                    for link in links:
                        if isinstance(link, dict):
                            url = link.get('url', '')
                            title = link.get('title', link.get('url', ''))
                            lines.append(f"- [{title}]({url})")
                        else:
                            lines.append(f"- {link}")
        
        # Add match scores if filtered
        if 'applied_filters' in yaml_data:
            if language == 'zh':
                lines.append("\n## 应用的过滤器")
                filters = yaml_data['applied_filters']
                lines.append(f"- 关注领域: {', '.join(filters.get('focus_areas', []))}")
                lines.append(f"- 最低分数: {filters.get('min_score', 0.3)}")
            else:
                lines.append("\n## Applied Filters")
                filters = yaml_data['applied_filters']
                lines.append(f"- Focus Areas: {', '.join(filters.get('focus_areas', []))}")
                lines.append(f"- Minimum Score: {filters.get('min_score', 0.3)}")
        
        return '\n'.join(lines)
    
    async def validate_links(
        self,
        ctx: Context,
        version: str = "138",
        channel: str = "stable"
    ) -> Dict[str, Any]:
        """
        Validate all extracted links.
        
        Args:
            ctx: FastMCP context
            version: Chrome version
            channel: Release channel
            
        Returns:
            Validation report
        """
        yaml_data = await self.yaml_cache.get_yaml_data(
            ctx,
            version,
            channel,
            True,
            False,
            None,
            False,
        )
        
        if not yaml_data:
            return {"error": "Could not load YAML data"}
        
        report = {
            "version": version,
            "channel": channel,
            "total_features": len(yaml_data.get('features', [])),
            "total_links": 0,
            "link_types": {},
            "invalid_links": []
        }
        
        for feature in yaml_data.get('features', []):
            for link in feature.get('links', []):
                if isinstance(link, dict):
                    url = link.get('url', '')
                    link_type = link.get('type', 'other')
                    
                    report['total_links'] += 1
                    report['link_types'][link_type] = report['link_types'].get(link_type, 0) + 1
                    
                    # Basic URL validation
                    if not url.startswith(('http://', 'https://')):
                        report['invalid_links'].append({
                            'feature': feature.get('title', 'Unknown'),
                            'url': url,
                            'reason': 'Invalid URL scheme'
                        })
        
        return report
    
    async def _generate_per_area_digests(
        self,
        ctx: Context,
        yaml_data: Dict,
        version: str,
        channel: str,
        language: Optional[str],
        debug: bool,
        run_config: DigestRunConfig,
        preparation_notice: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate digests for each area separately with parallel processing.
        
        Args:
            ctx: FastMCP context
            yaml_data: Full YAML data with all features
            version: Chrome version
            channel: Release channel
            language: Output language ("en", "zh", or None for bilingual)
            debug: Debug mode
            preparation_notice: Optional information about auto-regenerated inputs
            
        Returns:
            JSON response with status and output paths
        """
        import os
        import time
        from datetime import datetime

        run_started_at = datetime.now()
        run_started_perf = time.perf_counter()
        
        # Determine languages to generate based on run configuration
        languages = run_config.resolved_languages()
        
        # Get all areas from YAML data
        areas = self._get_areas_from_yaml(yaml_data)
        if debug:
            print(f"Found {len(areas)} areas to process: {areas}")
        
        self.telemetry.log_event(
            "per_area_run_context",
            {
                "version": version,
                "channel": channel,
                "languages": languages,
                "area_count": len(areas),
                "started_at": run_started_at.isoformat(),
            },
        )
        
        results = {
            "success": True,
            "mode": "per_area",
            "version": version,
            "channel": channel,
            "language": run_config.language_mode(),
            "languages": languages,
            "areas": areas,
            "outputs": {},
            "errors": {},
            "translation_status": {}
        }
        
        # Initialize progress tracking
        progress_data = {
            "version": version,
            "channel": channel,
            "languages": languages,
            "areas": areas,
            "total_areas": len(areas),
            "completed_areas": 0,
            "per_area": {},
            "started_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Save initial progress
        await self.io.update_progress(progress_data, debug)
        
        # Get concurrency limit from environment
        max_concurrency = int(os.getenv("WEBPLATFORM_MAX_CONCURRENCY", str(self._max_concurrency)))
        if debug:
            print(f"Using parallel processing with max concurrency: {max_concurrency}")
        
        # Create semaphore for concurrency control
        sem = asyncio.Semaphore(max_concurrency)
        # Lock for thread-safe result updates
        lock = asyncio.Lock()
        
        # Define async function to process single area
        async def process_area(area: str) -> None:
            async with sem:  # Control concurrency
                area_start_perf = time.perf_counter()
                area_started_at = datetime.now()
                
                # Normalize area name
                normalized_area = self.focus_manager.normalize_area(area)

                if debug:
                    print(f"\n[{area_started_at.strftime('%H:%M:%S')}] Starting area: {normalized_area}")
                
                self.telemetry.log_event(
                    "area_started",
                    {
                        "area": normalized_area,
                        "original_area": area,
                        "version": version,
                        "channel": channel,
                        "languages": languages,
                    },
                )
                area_status = "success"
                area_error_detail: Optional[str] = None
            
                # Load area-specific YAML; if empty, delegate file generation to AreaRunner and keep telemetry/progress here
                area_yaml = await self.yaml_cache.load_area_yaml(
                    ctx,
                    version,
                    channel,
                    normalized_area,
                    yaml_data,
                    debug,
                )
                if not area_yaml or len(area_yaml.get('features', [])) == 0:
                    if debug:
                        print(f"No features for area {area}, generating fallback via AreaRunner")
                    from chrome_update_digest.mcp.tools._digest_area_runner import AreaRunner
                    rr = await AreaRunner(self).process_one_area(
                        ctx,
                        normalized_area,
                        version,
                        channel,
                        languages,
                        debug,
                        full_yaml=yaml_data,
                    )
                    en_path = rr.get("paths", {}).get("en")
                    zh_path = rr.get("paths", {}).get("zh")
                    fallback_reason = "empty_area"
                    async with lock:
                        results["outputs"][normalized_area] = {"en": str(en_path) if en_path else ""}
                        progress_data["per_area"][area] = {"en": "fallback", "zh": "pending"}
                        await self.io.update_progress(progress_data, debug)
                    if 'zh' in languages and zh_path:
                        async with lock:
                            results["outputs"][normalized_area]["zh"] = str(zh_path)
                            progress_data["per_area"][area]["zh"] = "fallback"
                            await self.io.update_progress(progress_data, debug)
                    
                    area_elapsed = time.perf_counter() - area_start_perf
                    self.telemetry.observe_area_stage(
                        area=normalized_area,
                        stage="area_total",
                        language=None,
                        duration_seconds=area_elapsed,
                        status="fallback",
                        extra={"reason": fallback_reason, "features": 0},
                    )
                    self.telemetry.log_event(
                        "area_completed",
                        {
                            "area": normalized_area,
                            "status": "fallback",
                            "duration_ms": round(area_elapsed * 1000, 2),
                            "reason": fallback_reason,
                        },
                    )
                    
                    async with lock:
                        progress_data["completed_areas"] += 1
                        await self.io.update_progress(progress_data, debug)
                    return
            
                # Update progress to show area is in progress
                feature_count = len(area_yaml.get('features', []))
                async with lock:
                    progress_data["per_area"][area] = {"en": "in_progress", "zh": "pending"}
                    await self.io.update_progress(progress_data, debug)
                
                # Track retry/fallback state for telemetry
                english_retried = False
                english_fallback_used = False
                translation_retried = False
                translation_fallback_used = False
                translation_fallback_reason: Optional[str] = None

                # Generate English digest first (canonical)
                try:
                    if debug:
                        print(f"Generating English digest for {area}")
                    
                    english_stage_start = time.perf_counter()
                    try:
                        english_digest = await self.generation.generate_area_digest(
                            ctx, area_yaml, 'en', normalized_area, debug
                        )
                    except Exception as e:
                        english_duration = time.perf_counter() - english_stage_start
                        self.telemetry.observe_area_stage(
                            area=normalized_area,
                            stage="english_generation",
                            language="en",
                            duration_seconds=english_duration,
                            status="error",
                            extra={"attempt": 1},
                        )
                        self.telemetry.record_error(
                            operation="english_generation",
                            kind=type(e).__name__,
                            detail=str(e),
                            area=normalized_area,
                        )
                        area_status = "error"
                        area_error_detail = str(e)
                        raise
                    else:
                        english_duration = time.perf_counter() - english_stage_start
                        self.telemetry.observe_area_stage(
                            area=normalized_area,
                            stage="english_generation",
                            language="en",
                            duration_seconds=english_duration,
                            status="success",
                            extra={"attempt": 1},
                        )
                    
                    english_retried = False
                    english_fallback_used = False

                    # Validate English digest
                    validation_result = self.generation.validate_digest(english_digest, area_yaml)
                    if not validation_result['valid']:
                        if debug:
                            print(f"Validation failed for {area}: {validation_result['issues']}")
                        # Retry once with corrective prompt
                        english_retried = True
                        retry_start = time.perf_counter()
                        try:
                                english_digest = await self.generation.generate_area_digest(
                                    ctx, area_yaml, 'en', normalized_area, debug,
                                    retry_context=validation_result['issues']
                                )
                        except Exception as e:
                            retry_duration = time.perf_counter() - retry_start
                            self.telemetry.observe_area_stage(
                                area=normalized_area,
                                stage="english_generation",
                                language="en",
                                duration_seconds=retry_duration,
                                status="error",
                                extra={"attempt": 2, "retry": True},
                            )
                            self.telemetry.record_error(
                                operation="english_generation",
                                kind=type(e).__name__,
                                detail=str(e),
                                area=normalized_area,
                            )
                            area_status = "error"
                            area_error_detail = str(e)
                            raise
                        else:
                            retry_duration = time.perf_counter() - retry_start
                            self.telemetry.observe_area_stage(
                                area=normalized_area,
                                stage="english_generation",
                                language="en",
                                duration_seconds=retry_duration,
                                status="success",
                                extra={"attempt": 2, "retry": True},
                            )
                        validation_result = self.generation.validate_digest(english_digest, area_yaml)
                        if not validation_result['valid']:
                            # Generate fallback
                            english_fallback_used = True
                            fallback_start = time.perf_counter()
                            english_digest = self.generation.generate_area_fallback(
                                area_yaml, 'en', normalized_area, "LLM generation failed validation"
                            )
                            fallback_duration = time.perf_counter() - fallback_start
                            self.telemetry.observe_area_stage(
                                area=normalized_area,
                                stage="english_fallback",
                                language="en",
                                duration_seconds=fallback_duration,
                                status="success",
                                extra={"issues": validation_result['issues']},
                            )
                            self.telemetry.record_error(
                                operation="english_generation",
                                kind="validation_failed",
                                detail=validation_result['issues'] or "unknown",
                                area=normalized_area,
                            )
                            area_status = "fallback"
                            area_error_detail = validation_result['issues']
                    
                    english_status = "fallback" if english_fallback_used else "done"
                    english_reason = area_error_detail if english_fallback_used else None
                    en_path = await self.io.persist_area_language_output(
                        version=version,
                        channel=channel,
                        normalized_area=normalized_area,
                        area_key=area,
                        language='en',
                        content=english_digest,
                        lock=lock,
                        progress_data=progress_data,
                        results=results,
                        status=english_status,
                        debug=debug,
                        reason=english_reason,
                    )
                    
                    # Generate Chinese translation if needed
                    if 'zh' in languages:
                        if debug:
                            print(f"Translating to Chinese for {area}")
                        
                        async with lock:
                            progress_data["per_area"][area]["zh"] = "in_progress"
                            await self.io.update_progress(progress_data, debug)
                        
                        try:
                            translation_stage_start = time.perf_counter()
                            try:
                                chinese_digest = await self.generation.translate_digest(
                                    ctx, english_digest, normalized_area, version, channel, debug
                                )
                            except Exception as e:
                                translation_duration = time.perf_counter() - translation_stage_start
                                self.telemetry.observe_area_stage(
                                    area=normalized_area,
                                    stage="translation",
                                    language="zh",
                                    duration_seconds=translation_duration,
                                    status="error",
                                    extra={"attempt": 1},
                                )
                                self.telemetry.record_error(
                                    operation="translation",
                                    kind=type(e).__name__,
                                    detail=str(e),
                                    area=normalized_area,
                                )
                                area_status = "error"
                                area_error_detail = str(e)
                                raise
                            else:
                                translation_duration = time.perf_counter() - translation_stage_start
                                self.telemetry.observe_area_stage(
                                    area=normalized_area,
                                    stage="translation",
                                    language="zh",
                                    duration_seconds=translation_duration,
                                    status="success",
                                    extra={"attempt": 1},
                                )
                            
                            # Validate translation
                            translation_valid = self.generation.validate_translation(english_digest, chinese_digest)
                            if not translation_valid['valid']:
                                if debug:
                                    print(f"Translation validation failed: {translation_valid['issues']}")
                                # Retry translation once
                                translation_retried = True
                                translation_retry_start = time.perf_counter()
                                try:
                                    chinese_digest = await self.generation.translate_digest(
                                        ctx,
                                        english_digest,
                                        normalized_area,
                                        version,
                                        channel,
                                        debug,
                                        retry_context=translation_valid['issues'],
                                    )
                                except Exception as e:
                                    retry_duration = time.perf_counter() - translation_retry_start
                                    self.telemetry.observe_area_stage(
                                        area=normalized_area,
                                        stage="translation",
                                        language="zh",
                                        duration_seconds=retry_duration,
                                        status="error",
                                        extra={"attempt": 2, "retry": True},
                                    )
                                    self.telemetry.record_error(
                                        operation="translation",
                                        kind=type(e).__name__,
                                        detail=str(e),
                                        area=normalized_area,
                                    )
                                    area_status = "error"
                                    area_error_detail = str(e)
                                    raise
                                else:
                                    retry_duration = time.perf_counter() - translation_retry_start
                                    self.telemetry.observe_area_stage(
                                        area=normalized_area,
                                        stage="translation",
                                        language="zh",
                                        duration_seconds=retry_duration,
                                        status="success",
                                        extra={"attempt": 2, "retry": True},
                                    )
                                translation_valid = self.generation.validate_translation(english_digest, chinese_digest)
                                if not translation_valid['valid']:
                                    # Translation fallback
                                    translation_fallback_used = True
                                    fallback_start = time.perf_counter()
                                    chinese_digest = self.generation.generate_translation_fallback(
                                        version, channel, normalized_area, en_path
                                    )
                                    fallback_duration = time.perf_counter() - fallback_start
                                    async with lock:
                                        results["translation_status"][normalized_area] = "fallback"
                                    self.telemetry.observe_area_stage(
                                        area=normalized_area,
                                        stage="translation_fallback",
                                        language="zh",
                                        duration_seconds=fallback_duration,
                                        status="success",
                                        extra={"issues": translation_valid['issues']},
                                    )
                                    self.telemetry.record_error(
                                        operation="translation",
                                        kind="validation_failed",
                                        detail=translation_valid['issues'] or "unknown",
                                        area=normalized_area,
                                    )
                                    translation_fallback_reason = translation_valid['issues'] or "validation_failed"
                                    if area_status != "error":
                                        area_status = "fallback"
                                        area_error_detail = translation_fallback_reason
                                else:
                                    async with lock:
                                        results["translation_status"][normalized_area] = "retry_success"
                            else:
                                async with lock:
                                    results["translation_status"][normalized_area] = "ok"
                            
                            translation_status_label = "fallback" if translation_fallback_used else "done"
                            zh_path = await self.io.persist_area_language_output(
                                version=version,
                                channel=channel,
                                normalized_area=normalized_area,
                                area_key=area,
                                language='zh',
                                content=chinese_digest,
                                lock=lock,
                                progress_data=progress_data,
                                results=results,
                                status=translation_status_label,
                                debug=debug,
                                reason=translation_fallback_reason if translation_fallback_used else None,
                            )
                            
                        except Exception as e:
                            if debug:
                                print(f"Translation failed for {area}: {e}")
                            area_status = "error"
                            area_error_detail = str(e)
                            translation_fallback_reason = f"exception: {e}"
                            async with lock:
                                results["errors"][f"{normalized_area}:zh"] = str(e)
                                results["translation_status"][normalized_area] = "error"
                                progress_data["per_area"][area]["zh"] = "error"
                                progress_data["per_area"][area]["zh_error"] = str(e)
                            
                            # Generate translation fallback
                            translation_fallback_used = True
                            fallback_start = time.perf_counter()
                            fallback = self.generation.generate_translation_fallback(
                                version, channel, normalized_area, en_path
                            )
                            fallback_duration = time.perf_counter() - fallback_start
                            zh_path = await self.io.persist_area_language_output(
                                version=version,
                                channel=channel,
                                normalized_area=normalized_area,
                                area_key=area,
                                language='zh',
                                content=fallback,
                                lock=lock,
                                progress_data=progress_data,
                                results=results,
                                status="error",
                                debug=debug,
                                reason=translation_fallback_reason,
                            )
                            self.telemetry.observe_area_stage(
                                area=normalized_area,
                                stage="translation_fallback",
                                language="zh",
                                duration_seconds=fallback_duration,
                                status="success",
                                extra={"reason": "exception"},
                            )
                    
                except Exception as e:
                    if debug:
                        print(f"Failed to generate digest for {area}: {e}")
                    async with lock:
                        results["errors"][f"{normalized_area}:en"] = str(e)
                        results["success"] = False
                        progress_data["per_area"][area]["en"] = "error"
                        progress_data["per_area"][area]["error"] = str(e)
                        await self.io.update_progress(progress_data, debug)
                
                # Mark area as completed
                area_elapsed = time.perf_counter() - area_start_perf
                area_extra = {
                    "features": feature_count,
                    "english_retried": english_retried,
                    "english_fallback": english_fallback_used,
                    "translation_retried": translation_retried,
                    "translation_fallback": translation_fallback_used,
                }
                if area_error_detail:
                    area_extra["error"] = area_error_detail

                self.telemetry.observe_area_stage(
                    area=normalized_area,
                    stage="area_total",
                    language=None,
                    duration_seconds=area_elapsed,
                    status=area_status,
                    extra=area_extra,
                )
                self.telemetry.log_event(
                    "area_completed",
                    {
                        "area": normalized_area,
                        "status": area_status,
                        "duration_ms": round(area_elapsed * 1000, 2),
                        "features": feature_count,
                        "english_retried": english_retried,
                        "english_fallback": english_fallback_used,
                        "translation_retried": translation_retried,
                        "translation_fallback": translation_fallback_used,
                        "error": area_error_detail,
                    },
                )

                if debug:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Completed {normalized_area} in {area_elapsed:.1f}s")
                
                async with lock:
                    progress_data["completed_areas"] += 1
                    await self.io.update_progress(progress_data, debug)
        
        # Execute all areas in parallel with concurrency control
        run_exec_start = time.perf_counter()
        # Phase 2: wire in AreaRunner for future replacement (no behavior change yet)
        await asyncio.gather(*(process_area(area) for area in areas))
        
        total_time = time.perf_counter() - run_exec_start
        if debug:
            print(f"\n[COMPLETED] All {len(areas)} areas processed in {total_time:.1f} seconds")
            print(f"Average time per area: {total_time/len(areas):.1f} seconds")
        
        self.telemetry.log_event(
            "per_area_run_completed",
            {
                "version": version,
                "channel": channel,
                "languages": languages,
                "area_count": len(areas),
                "duration_ms": round(total_time * 1000, 2),
            },
        )
        
        # Final progress update
        progress_data["completed_at"] = datetime.now().isoformat()
        progress_data["total_time_seconds"] = total_time
        await self.io.update_progress(progress_data, debug)

        if preparation_notice and preparation_notice.get("triggered"):
            results.setdefault("preparation_steps", []).append(
                self._sanitize_preparation_notice(preparation_notice)
            )

        return json.dumps(results, ensure_ascii=False, indent=2)
    
    def _get_areas_from_yaml(self, yaml_data: Dict) -> List[str]:
        """Extract all areas from YAML data and normalize them."""
        # Start with any explicit area list provided by aggregation
        areas = set(yaml_data.get('areas', []))
        # Also infer areas from feature tags to be robust
        for feature in yaml_data.get('features', []):
            tags = feature.get('primary_tags', [])
            for tag in tags:
                if isinstance(tag, dict):
                    tag_name = tag.get('name', 'others')
                else:
                    tag_name = str(tag)
                
                # Normalize the area name to match folder structure
                normalized = self.focus_manager.normalize_area(tag_name)
                areas.add(normalized)
        
        # Always include 'others' if there are untagged features
        if not areas:
            areas.add('others')
        
        return sorted(list(areas))
    
    
    def _validate_digest(self, digest: str, yaml_data: Dict) -> Dict[str, Any]:
        """Validate that digest contains expected features and links."""
        import re
        
        # Extract feature titles from YAML
        expected_titles = set()
        expected_links = set()
        
        for feature in yaml_data.get('features', []):
            expected_titles.add(feature.get('title', ''))
            for link in feature.get('links', []):
                if isinstance(link, dict):
                    expected_links.add(link.get('url', ''))
                else:
                    expected_links.add(str(link))
        
        # Extract titles and links from digest
        # Prefer H3 feature headings; fall back to H4 if none found to guard against prompt drift
        h3_titles = re.findall(r'^###\s+(.+)$', digest, re.MULTILINE)
        h4_titles = re.findall(r'^####\s+(.+)$', digest, re.MULTILINE)

        def _normalize_title(title: str) -> str:
            """Normalize feature titles for resilient comparison."""
            # Replace smart quotes and dashes before collapsing whitespace for consistent matching
            normalized = title.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
            normalized = normalized.replace('–', '-').replace('—', '-')
            normalized = re.sub(r'\s+', ' ', normalized.strip().lower())
            return normalized

        # Decide which heading level to treat as the feature marker
        raw_found_titles = h3_titles if h3_titles else h4_titles
        found_titles = {_normalize_title(title) for title in raw_found_titles}

        # Normalize expected titles for comparison but keep originals for reporting
        normalized_expected = {_normalize_title(title) for title in expected_titles}

        # Look for markdown links
        found_links = set(re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', digest))
        found_link_urls = {url for _, url in found_links}

        # Calculate missing elements
        missing_normalized = normalized_expected - found_titles
        missing_titles = [title for title in expected_titles if _normalize_title(title) in missing_normalized]
        extra_links = found_link_urls - expected_links

        # Determine if valid
        missing_ratio = len(missing_titles) / len(expected_titles) if expected_titles else 0
        valid = missing_ratio <= 0.3 and len(extra_links) <= 2
        
        issues = []
        if missing_ratio > 0.3:
            issues.append(f"Missing {len(missing_titles)} of {len(expected_titles)} features")
        if len(extra_links) > 2:
            issues.append(f"Found {len(extra_links)} unknown links")
        
        return {
            'valid': valid,
            'missing_titles': list(missing_titles),
            'extra_links': list(extra_links),
            'missing_ratio': missing_ratio,
            'issues': '; '.join(issues) if issues else None
        }

    async def _get_yaml_data(
        self,
        ctx: Context,
        version: str,
        channel: str,
        use_cache: bool = True,
        split_by_area: bool = True,
        target_area: Optional[str] = None,
        debug: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Compatibility shim for tests that patch YAML loading directly.

        Delegates to the DigestYAMLCache while preserving the asynchronous signature
        expected by the original implementation.
        """
        return await self.yaml_cache.get_yaml_data(
            ctx=ctx,
            version=version,
            channel=channel,
            use_cache=use_cache,
            split_by_area=split_by_area,
            target_area=target_area,
            debug=debug,
        )

    async def _generate_digest_from_yaml(
        self,
        ctx: Context,
        yaml_data: Dict[str, Any],
        language: Optional[str],
        target_area: Optional[str],
        debug: bool,
    ) -> str:
        """
        Generate a digest with graceful fallback when sampling fails.

        Older tests expect this helper to exist on the tool class rather than on the
        generation engine, so we proxy the call and surface the same behaviour.
        """
        try:
            return await self.generation.generate_digest_from_yaml(
                ctx,
                yaml_data,
                language or 'en',
                target_area,
                debug,
            )
        except asyncio.CancelledError:
            # Preserve cooperative cancellation semantics for upstream callers.
            raise
        except Exception as exc:
            if debug:
                print(f"LLM digest generation failed ({language or 'en'}): {exc}; falling back to deterministic output")
            self.telemetry.record_error(
                operation="bulk_digest_generation",
                kind=type(exc).__name__,
                detail=str(exc),
                area=target_area,
            )
            return self._generate_fallback_digest(yaml_data, language or 'en')

    def _format_features_for_llm(self, yaml_data: Dict[str, Any]) -> str:
        """Expose formatting helper retained for backward-compatible tests."""
        return self.generation._format_features_for_llm(yaml_data)

    def _truncate_features(self, yaml_data: Dict[str, Any], max_content_length: int = 300) -> Dict[str, Any]:
        """Delegate to the generation engine's truncation logic."""
        return self.generation._truncate_features(yaml_data, max_content_length=max_content_length)

    def _validate_translation(self, english_digest: str, chinese_digest: str) -> Dict[str, Any]:
        """Compatibility wrapper for translation validation helper."""
        return self.generation.validate_translation(english_digest, chinese_digest)

    def _generate_area_fallback(self, area_yaml: Dict[str, Any], language: str, area: str, reason: str) -> str:
        """Proxy to the generation engine for area-level fallback content."""
        return self.generation.generate_area_fallback(area_yaml, language, area, reason)

    def _generate_translation_fallback(self, version: str, channel: str, area: str, en_path: Path) -> str:
        """Proxy helper retained for legacy tests."""
        return self.generation.generate_translation_fallback(version, channel, area, en_path)

    def _generate_minimal_fallback(self, version: str, channel: str, area: str, language: str) -> str:
        """Proxy helper retained for legacy tests."""
        return self.generation.generate_minimal_fallback(version, channel, area, language)

    async def _load_prompt(
        self,
        ctx: Context,
        language: str,
        target_area: Optional[str],
        debug: bool,
    ) -> str:
        """Expose prompt loading for tests that assert on template contents."""
        return await self.generation._load_prompt(language, target_area, debug)

    async def _load_release_notes(
        self,
        ctx: Context,
        version: str,
        channel: str,
        target_area: Optional[str],
        debug: bool,
    ) -> Optional[str]:
        """
        Backward-compatible wrapper around the YAML cache release note loader.

        Tests patching this helper expect it to exist directly on the tool.
        """
        return await self.yaml_cache._load_release_notes(
            ctx,
            version,
            channel,
            debug,
            target_area,
        )

    def _get_digest_path(
        self,
        version: str,
        channel: str,
        target_area: Optional[str],
        language: str,
    ) -> Path:
        """Return the expected digest path without writing the file."""
        return self.io.get_digest_path(version, channel, target_area, language)

    def _read_digest_file(self, digest_type: str, version: int, channel: str) -> Optional[str]:
        """
        Legacy helper retained for scripts that introspect generated markdown.

        Args:
            digest_type: Currently only 'webplatform' is supported by this tool.
            version: Chrome version number
            channel: Release channel

        Returns:
            File contents if the digest exists, otherwise None.
        """
        if digest_type not in {"webplatform", "webgpu"}:
            raise ValueError(f"Unsupported digest type: {digest_type}")

        target_area = None if digest_type == "webplatform" else "graphics-webgpu"
        path = self._get_digest_path(str(version), channel, target_area, "en")
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8")
    
