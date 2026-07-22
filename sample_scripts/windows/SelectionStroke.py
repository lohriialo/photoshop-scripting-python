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

# Stroke the selection border: Selection.SelectBorder + Selection.Stroke
# Prefer comtypes when constructing SolidColor / complex args.

app = get_app(backend="comtypes")

if app.Documents.Count < 1:
    print("Create a document with a non-background layer before running this script!")
elif app.ActiveDocument.ActiveLayer.IsBackgroundLayer:
    print("Operation cannot be performed on background layer")
else:
    ps_pixels = 1
    strt_ruler_units = app.Preferences.RulerUnits
    app.Preferences.RulerUnits = ps_pixels

    doc = app.ActiveDocument
    sel_ref = doc.Selection
    offset = 10
    sel_bounds = (
        (offset, offset),
        (doc.Width - offset, offset),
        (doc.Width - offset, doc.Height - offset),
        (offset, doc.Height - offset),
    )
    sel_ref.Select(sel_bounds)
    sel_ref.SelectBorder(5)  # border width in px

    stroke_color = create_solid_color(backend="comtypes")
    stroke_color.CMYK.Cyan = 20
    stroke_color.CMYK.Magenta = 90
    stroke_color.CMYK.Yellow = 50
    stroke_color.CMYK.Black = 50

    app.displayDialogs = 3  # no dialogs
    ps_outside_stroke = 3   # PsStrokeLocation.psOutsideStroke
    ps_vivid_light = 15     # blend mode
    # Stroke(color, width, location, mode, opacity, preserveTransparency)
    sel_ref.Stroke(stroke_color, 2, ps_outside_stroke, ps_vivid_light, 75, True)

    app.Preferences.RulerUnits = strt_ruler_units
    print("Stroked selection border")
