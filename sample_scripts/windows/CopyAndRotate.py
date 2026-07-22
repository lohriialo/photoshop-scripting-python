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

from photoshop_scripting import ensure_sample, get_app
from photoshop_scripting.paths import as_ps_path

# Open a sample, rotate the canvas, then crop an inset border.
# Document.RotateCanvas(angle) / Document.Crop(bounds)

app = get_app()

ps_pixels = 1
file_name = as_ps_path(ensure_sample("Layer Comps.psd"))
src_doc = app.Open(file_name)

strt_ruler_units = app.Preferences.RulerUnits
if strt_ruler_units != ps_pixels:
    app.Preferences.RulerUnits = ps_pixels

# bounds = [left, top, right, bottom] in current ruler units (pixels here)
bounds = [10, 10, src_doc.Width - 10, src_doc.Height - 10]
src_doc.RotateCanvas(45)
src_doc.Crop(bounds)

app.Preferences.RulerUnits = strt_ruler_units
print("Rotated 45° and cropped a 10px border")
