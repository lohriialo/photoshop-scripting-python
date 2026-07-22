"""
Helpers for scripting Adobe Photoshop from Python.

Windows: COM via comtypes (preferred) or win32com
macOS:   appscript (see sample_scripts/mac_scripting/ for Apple Event samples)
"""

from .app import get_app, is_photoshop_running, photoshop_available, require_windows_com
from .constants import DialogModes, LayerKind, ResampleMethod, StrokeLocation, Units
from .paths import ensure_sample, repo_root, sample_path, sample_scripts_dir, samples_dir
from .prefs import dialog_mode, ruler_units, saved_preferences

__version__ = "2.0.0"

__all__ = [
    "get_app",
    "is_photoshop_running",
    "photoshop_available",
    "require_windows_com",
    "DialogModes",
    "LayerKind",
    "Units",
    "ResampleMethod",
    "StrokeLocation",
    "repo_root",
    "sample_path",
    "sample_scripts_dir",
    "samples_dir",
    "ensure_sample",
    "dialog_mode",
    "ruler_units",
    "saved_preferences",
    "__version__",
]
