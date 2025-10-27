"""
Telemetry helpers for the WebPlatform digest pipeline.

This module provides a small abstraction on top of `prometheus_client`
so the rest of the codebase can emit Prometheus-compatible metrics and
structured JSON telemetry events without needing to touch the metrics
library directly. When `prometheus_client` is not available the helpers
degrade gracefully to no-ops so production code can continue to run.
"""

from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, Iterable, Optional

try:
    from prometheus_client import Counter, Histogram  # type: ignore
except Exception:  # pragma: no cover - fallback when dependency missing
    Counter = None  # type: ignore
    Histogram = None  # type: ignore


class _NoOpMetric:
    """Fallback metric used when prometheus_client is unavailable."""

    def labels(self, *args: Any, **kwargs: Any) -> "_NoOpMetric":
        return self

    def observe(self, value: float) -> None:
        return None

    def inc(self, value: float = 1.0) -> None:
        return None


def _create_metric(factory: Any, name: str, documentation: str, *, labelnames: Iterable[str] = (), **kwargs: Any) -> Any:
    """
    Attempt to create a Prometheus metric and fall back to a no-op metric.

    Args:
        factory: prometheus_client metric factory (Counter/Histogram)
        name: metric name
        documentation: help text
        labelnames: metric label names
        **kwargs: forwarded kwargs (e.g. buckets for Histogram)

    Returns:
        A metric instance (Counter/Histogram) or a `_NoOpMetric`.
    """
    if factory is None:
        return _NoOpMetric()

    params: Dict[str, Any] = {"labelnames": tuple(labelnames)}
    params.update(kwargs)

    try:
        return factory(name, documentation, **params)
    except Exception:  # pragma: no cover - guard against misconfiguration
        return _NoOpMetric()


class DigestTelemetry:
    """
    Collects telemetry (Prometheus metrics + JSON events) for the digest pipeline.

    The class is lightweight but thread-safe so callers can safely share a single
    instance across asynchronous tasks.
    """

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.monitoring_dir = self.base_path / ".monitoring"
        self.monitoring_dir.mkdir(parents=True, exist_ok=True)
        self.telemetry_file = self.monitoring_dir / "webplatform-telemetry.jsonl"
        self._event_lock = threading.Lock()

        # Metrics
        self._area_stage_duration = _create_metric(
            Histogram,
            "webplatform_digest_stage_duration_seconds",
            "Time spent processing each area/stage of the digest pipeline.",
            labelnames=("area", "stage", "language", "status"),
            buckets=(
                0.1,
                0.25,
                0.5,
                1.0,
                2.5,
                5.0,
                10.0,
                20.0,
                40.0,
                80.0,
            ),
        )
        self._llm_attempt_duration = _create_metric(
            Histogram,
            "webplatform_digest_llm_attempt_seconds",
            "Latency per LLM call including retries.",
            labelnames=("operation", "status", "attempt"),
            buckets=(
                0.5,
                1.0,
                2.0,
                4.0,
                8.0,
                16.0,
                32.0,
                64.0,
            ),
        )
        self._llm_retry_counter = _create_metric(
            Counter,
            "webplatform_digest_llm_retries_total",
            "Count of LLM sampling retries grouped by outcome.",
            labelnames=("operation", "outcome"),
        )
        self._error_counter = _create_metric(
            Counter,
            "webplatform_digest_errors_total",
            "Count of errors encountered inside the digest pipeline.",
            labelnames=("operation", "kind"),
        )

    def _append_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """Append a structured telemetry event to JSONL storage."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_type,
            **payload,
        }

        try:
            with self._event_lock:
                with open(self.telemetry_file, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record, ensure_ascii=False))
                    handle.write("\n")
        except Exception:
            # Telemetry must not break the pipeline; swallow errors silently.
            return None

    def observe_area_stage(
        self,
        *,
        area: str,
        stage: str,
        language: Optional[str],
        duration_seconds: float,
        status: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record the time spent inside a specific pipeline stage for an area."""
        labels = {
            "area": area,
            "stage": stage,
            "language": language or "n/a",
            "status": status,
        }
        self._area_stage_duration.labels(**labels).observe(duration_seconds)

        payload = {
            "area": area,
            "stage": stage,
            "language": language or None,
            "status": status,
            "duration_ms": round(duration_seconds * 1000, 2),
        }
        if extra:
            payload.update(extra)
        self._append_event("area_stage_duration", payload)

    def observe_llm_attempt(
        self,
        *,
        operation: str,
        attempt: int,
        duration_seconds: float,
        status: str,
        model: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
        debug: bool = False,
    ) -> None:
        """Record latency for an LLM attempt and track retry counters."""
        labels = {"operation": operation, "status": status, "attempt": str(attempt)}
        self._llm_attempt_duration.labels(**labels).observe(duration_seconds)

        if attempt > 1:
            outcome = "success" if status == "success" else "failed"
            self._llm_retry_counter.labels(operation=operation, outcome=outcome).inc()

        payload = {
            "operation": operation,
            "attempt": attempt,
            "status": status,
            "duration_ms": round(duration_seconds * 1000, 2),
        }
        # Only include verbose details in debug mode
        if debug:
            if model:
                payload["model"] = model
            if extra:
                payload.update(extra)
        else:
            # In non-debug mode, only include essential context
            if extra:
                essential_keys = {
                    "language",
                    "area",
                    "version",
                    "channel",
                    "max_retries",
                    "wait_seconds",
                    "service_seconds",
                    "error",
                }
                payload.update({k: v for k, v in extra.items() if k in essential_keys})
        self._append_event("llm_attempt", payload)

    def record_error(self, *, operation: str, kind: str, detail: Optional[str] = None, area: Optional[str] = None) -> None:
        """Increment error counters and emit a telemetry event."""
        self._error_counter.labels(operation=operation, kind=kind).inc()
        payload = {"operation": operation, "kind": kind}
        if area:
            payload["area"] = area
        if detail:
            payload["detail"] = detail
        self._append_event("error", payload)

    def record_event(self, *, event_type: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Backward-compatible wrapper used by legacy tools/tests.

        Clean data pipeline tests still call `record_event`, so we delegate to the
        modern `log_event` helper.
        """
        self.log_event(event_type, data or {})

    def log_event(self, event_type: str, payload: Optional[Dict[str, Any]] = None, debug: bool = False) -> None:
        """
        Expose a lightweight structured event logger.
        
        Args:
            event_type: The type of event to log
            payload: Optional dictionary of event data
            debug: If True, include verbose/debug information. If False, skip certain debug-only events.
        """
        # Skip debug-only events when not in debug mode
        if not debug and event_type in ("llm_sampling_attempt_start", "llm_sampling_attempt_complete"):
            return
        
        # Filter out verbose payload fields when not in debug mode
        if not debug and payload:
            filtered_payload = {k: v for k, v in payload.items() if k not in ("payload_preview", "model", "has_model_preferences")}
            self._append_event(event_type, filtered_payload)
        else:
            self._append_event(event_type, payload or {})

    def log_tool_operation(
        self,
        *,
        tool_name: str,
        status: str,
        duration_seconds: float,
        wait_seconds: float,
        queue_depth: int,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an MCP tool invocation with wait/execute timings."""
        payload: Dict[str, Any] = {
            "tool": tool_name,
            "status": status,
            "duration_ms": round(duration_seconds * 1000, 2),
            "wait_ms": round(wait_seconds * 1000, 2),
            "queue_depth": queue_depth,
        }
        if extra:
            payload.update(extra)
        self._append_event("mcp_tool_operation", payload)

    @contextmanager
    def track_stage(
        self,
        *,
        area: str,
        stage: str,
        language: Optional[str],
        extra: Optional[Dict[str, Any]] = None,
    ):
        """
        Context manager that measures the time spent in a stage and records telemetry.
        """
        start = perf_counter()
        status = "success"
        try:
            yield
        except Exception as exc:
            status = "error"
            self.record_error(operation=stage, kind=type(exc).__name__, detail=str(exc), area=area)
            raise
        finally:
            duration_seconds = perf_counter() - start
            self.observe_area_stage(
                area=area,
                stage=stage,
                language=language,
                duration_seconds=duration_seconds,
                status=status,
                extra=extra,
            )


__all__ = ["DigestTelemetry"]
