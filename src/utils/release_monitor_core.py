"""
Compatibility wrapper so legacy imports (`utils.release_monitor_core`) continue
to work in tests that patch the module path directly.
"""

from chrome_update_digest.utils.release_monitor_core import *  # noqa: F401,F403
