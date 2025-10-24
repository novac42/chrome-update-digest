"""
Compatibility shim for legacy imports.

The FastMCP server has moved to `chrome_update_digest.mcp.server`. This module
re-exports the new package entry points so existing scripts keep working.
"""

from chrome_update_digest.mcp.server import *  # noqa: F401,F403

if __name__ == "__main__":  # pragma: no cover - manual entry point
    main()
