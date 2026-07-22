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

# Copy a rectangular half of a document and paste into a new document.
# Selection.Copy / Document.Paste — use comtypes for Select(array).

app = get_app(backend="comtypes")

ps_inches = 2
ps_pixels = 1
ps_new_rgb = 2
ps_white = 1
ps_text_layer = 2
ps_replace_selection = 1

strt_ruler_units = app.Preferences.RulerUnits
if strt_ruler_units != ps_inches:
    app.Preferences.RulerUnits = ps_inches

src_doc = app.Documents.Add(7, 5, 72, None, ps_new_rgb, ps_white)

# Text layers cannot be copied as pixels this way
if src_doc.ActiveLayer.Kind == ps_text_layer:
    print("You cannot copy from a text layer")
else:
    # Selection coordinates are always in *pixels*
    x2 = (src_doc.Width * src_doc.Resolution) / 2
    y2 = src_doc.Height * src_doc.Resolution
    sel_area = ((0, 0), (x2, 0), (x2, y2), (0, y2))
    src_doc.Selection.Select(sel_area, ps_replace_selection, 0, False)
    src_doc.Selection.Copy()

    app.Preferences.RulerUnits = ps_pixels
    paste_doc = app.Documents.Add(x2, y2, src_doc.Resolution, "Paste Target")
    paste_doc.Paste()
    print("Pasted into", paste_doc.Name)

if strt_ruler_units != app.Preferences.RulerUnits:
    app.Preferences.RulerUnits = strt_ruler_units
