"""
Photoshop scripting sample (Python / Windows COM).
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from photoshop_scripting import require_windows_com

require_windows_com()  # these samples use the Windows COM object model

from photoshop_scripting import get_app

# SolidColor.IsEqual compares two colour objects (foreground vs background).

app = get_app()

if app.ForegroundColor.IsEqual(app.BackgroundColor):
    print("They're Equal")
else:
    print("NOT Equal")
    print("  Foreground RGB:", app.ForegroundColor.RGB.Red, app.ForegroundColor.RGB.Green, app.ForegroundColor.RGB.Blue)
    print("  Background RGB:", app.BackgroundColor.RGB.Red, app.BackgroundColor.RGB.Green, app.BackgroundColor.RGB.Blue)
