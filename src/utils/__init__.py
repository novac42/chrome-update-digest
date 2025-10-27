"""
Legacy compatibility shims for modules that previously lived under a top-level
`utils` package. Test doubles still import `utils.<module>` so we proxy those
requests to the current `chrome_update_digest.utils` package.
"""

from __future__ import annotations

import importlib
import sys
from types import ModuleType
from typing import Any


def __getattr__(name: str) -> ModuleType:
    target = f"chrome_update_digest.utils.{name}"
    module = importlib.import_module(target)
    sys.modules[f"utils.{name}"] = module
    return module


def __dir__() -> Any:
    """Expose dynamically discoverable attributes for tooling."""
    chrome_utils = importlib.import_module("chrome_update_digest.utils")
    return sorted(set(globals().keys()) | set(dir(chrome_utils)))
