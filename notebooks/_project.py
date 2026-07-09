"""Add project root to sys.path and chdir so `app` imports and data paths work."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def setup() -> Path:
    root_str = str(ROOT)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    os.chdir(ROOT)

    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    return ROOT
