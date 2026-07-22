"""Shared path bootstrap for Windows samples (import first)."""

from __future__ import annotations

import sys
from pathlib import Path

_SAMPLE_SCRIPTS = Path(__file__).resolve().parents[1]
_REPO_ROOT = _SAMPLE_SCRIPTS.parent
for _p in (_REPO_ROOT, _SAMPLE_SCRIPTS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from photoshop_scripting import require_windows_com  # noqa: E402

require_windows_com()
