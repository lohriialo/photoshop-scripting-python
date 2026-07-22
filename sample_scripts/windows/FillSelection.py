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
from photoshop_scripting.app import create_solid_color

# Selection.Fill(color, blendMode, opacity, preserveTransparency)
# Requires a non-background target layer.

app = get_app(backend="comtypes")

ps_pixels = 1
ps_new_rgb = 2
ps_white = 1
ps_normal_blend = 2  # PsColorBlendMode / blend normal

strt_ruler_units = app.Preferences.RulerUnits

if app.Documents.Count < 1:
    if strt_ruler_units != ps_pixels:
        app.Preferences.RulerUnits = ps_pixels
    doc_ref = app.Documents.Add(320, 240, 72, None, ps_new_rgb, ps_white)
    doc_ref.ArtLayers.Add()  # non-background layer
    app.Preferences.RulerUnits = strt_ruler_units

if app.ActiveDocument.ActiveLayer.IsBackgroundLayer:
    print("Can't perform operation on background layer")
else:
    sel_ref = app.ActiveDocument.Selection
    # Ensure there is a selection to fill
    try:
        # if empty, select all
        _ = sel_ref.Bounds
    except Exception:
        w, h = app.ActiveDocument.Width, app.ActiveDocument.Height
        sel_ref.Select(((0, 0), (w, 0), (w, h), (0, h)))

    fill_color = create_solid_color(backend="comtypes")
    fill_color.RGB.Red = 225
    fill_color.RGB.Green = 0
    fill_color.RGB.Blue = 0
    sel_ref.Fill(fill_color, ps_normal_blend, 25, False)
    print("Filled selection with red at 25% opacity")
