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

# Read the foreground colour as RGB components.
# SolidColor can also expose CMYK / HSB / Lab models on the same object.

app = get_app()

fg_color = app.ForegroundColor
fg_rgb = fg_color.RGB
print("Red:", fg_rgb.Red, "Green:", fg_rgb.Green, "Blue:", fg_rgb.Blue)
