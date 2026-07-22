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

# Set ArtLayer.Kind to create different layer types (here: text).

app = get_app()

ps_pixels = 1
ps_new_rgb = 2   # document mode RGB
ps_white = 1     # initial fill white
ps_text_layer = 2  # PsLayerKind.psTextLayer

strt_ruler_units = app.Preferences.RulerUnits

if app.Documents.Count < 1:
    if strt_ruler_units != ps_pixels:
        app.Preferences.RulerUnits = ps_pixels
    doc_ref = app.Documents.Add(320, 240, 72, None, ps_new_rgb, ps_white)
else:
    doc_ref = app.ActiveDocument

layer_ref = doc_ref.ArtLayers.Add()
layer_ref.Kind = ps_text_layer  # convert normal layer → text layer
layer_ref.TextItem.Contents = "Text layer via Kind"

app.Preferences.RulerUnits = strt_ruler_units
print("Layer kind set; name:", layer_ref.Name)
