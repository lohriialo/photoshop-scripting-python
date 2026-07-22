"""
Shared Photoshop connection for mac_scripting samples.

Prefers a concrete .app path (Photoshop 2026, 2025, …) so installs that share
bundle id com.adobe.Photoshop (e.g. release + Beta) are not mixed up.

Override with:
  export PHOTOSHOP_APP_PATH='/Applications/Adobe Photoshop 2026/Adobe Photoshop 2026.app'
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]  # sample_scripts/mac_scripting -> repo root
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def photoshop(*, quiet: bool = True):
    """
    Return an appscript Application reference to Photoshop.

    When quiet=True (default), sets display_dialogs to never so samples
    are not blocked by modal UI.
    """
    from appscript import k
    from photoshop_scripting import get_app

    ps = get_app()
    if quiet:
        try:
            ps.display_dialogs.set(k.never)
        except Exception:
            pass
    return ps


def sample_file(*parts: str) -> str:
    """Absolute path under sample_scripts/PS_Samples_Files (cwd-independent)."""
    from photoshop_scripting.paths import ensure_sample

    return str(ensure_sample(*parts))


def close_all_documents(ps=None) -> int:
    """Close every open document without saving. Returns how many were closed."""
    from appscript import k

    if ps is None:
        ps = photoshop()
    closed = 0
    # documents() can change while closing; loop until empty
    for _ in range(50):
        try:
            docs = ps.documents()
            if not docs:
                break
            ps.current_document.close(saving=k.no)
            closed += 1
        except Exception:
            break
    return closed
