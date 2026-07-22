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

# ArtLayer.Link(otherLayer) links layers so they transform together.

app = get_app()

ps_pixels = 1
ps_new_rgb = 2
ps_white = 1

strt_ruler_units = app.Preferences.RulerUnits
if app.Documents.Count < 1:
    if strt_ruler_units != ps_pixels:
        app.Preferences.RulerUnits = ps_pixels
    doc_ref = app.Documents.Add(320, 240, 72, None, ps_new_rgb, ps_white)
else:
    doc_ref = app.ActiveDocument

layer_ref = doc_ref.ArtLayers.Add()
layer_ref2 = doc_ref.ArtLayers.Add()
layer_ref.Link(layer_ref2)

app.Preferences.RulerUnits = strt_ruler_units
print("Linked", layer_ref.Name, "↔", layer_ref2.Name)
