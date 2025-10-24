#!/usr/bin/env python3
"""
Compatibility shim for clean_data_pipeline.py

This file maintains backward compatibility for scripts and documentation
that reference src/processors/clean_data_pipeline.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import everything from the new location
from chrome_update_digest.processors.clean_data_pipeline import *

# Ensure the module can be run directly
if __name__ == "__main__":
    from chrome_update_digest.processors.clean_data_pipeline import main
    sys.exit(main())