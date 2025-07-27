#!/usr/bin/env python3
"""
WSGI entry point for Vercel deployment
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app import app

if __name__ == "__main__":
    app.run() 