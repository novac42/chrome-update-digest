"""Pytest configuration shared across the test suite."""

import asyncio
import inspect
import sys
import pytest


@pytest.fixture(autouse=True)
def _ensure_utf8_output(monkeypatch: pytest.MonkeyPatch):
    """Force UTF-8 encoding for stdout/stderr to avoid Windows console errors."""
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except ValueError:
                # Some streams (like capsys replacements) do not allow reconfigure
                continue
    yield


def pytest_pyfunc_call(pyfuncitem):
    """Execute ``async def`` tests marked with ``@pytest.mark.asyncio``."""
    if pyfuncitem.get_closest_marker("asyncio") and inspect.iscoroutinefunction(pyfuncitem.obj):
        signature = inspect.signature(pyfuncitem.obj)
        kwargs = {name: pyfuncitem.funcargs[name] for name in signature.parameters}
        asyncio.run(pyfuncitem.obj(**kwargs))
        return True
    return None
