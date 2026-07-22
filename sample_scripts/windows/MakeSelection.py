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

# Selection.Select(region, type, feather, antiAlias)
# Region is a list of (x, y) corners. Prefer comtypes for array marshaling.

app = get_app(backend="comtypes")

ps_pixels = 1
ps_new_rgb = 2
ps_white = 1
ps_replace_selection = 1  # PsSelectionType.psReplaceSelection

if app.Documents.Count < 1:
    strt = app.Preferences.RulerUnits
    app.Preferences.RulerUnits = ps_pixels
    doc_ref = app.Documents.Add(320, 240, 72, None, ps_new_rgb, ps_white)
    app.Preferences.RulerUnits = strt
else:
    doc_ref = app.ActiveDocument

# Rectangle as four corner points (pixels; selections are always pixel-based)
sel_area = ((50, 60), (150, 60), (150, 120), (50, 120))
doc_ref.Selection.Select(sel_area, ps_replace_selection, 5.5, False)
print("Selection created with 5.5px feather")
