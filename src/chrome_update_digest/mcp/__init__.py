"""
Integrations and entry points that expose Chrome digest functionality through
Claude MCP compatible servers and tooling.
"""

from .server import create_app, main

__all__ = ["create_app", "main"]
