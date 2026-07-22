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

# Store a selection into an alpha channel, then load/combine selections.
# Selection.Store(channel) / Selection.Load(channel, combineType, invert)

app = get_app(backend="comtypes")

ps_pixels = 1
ps_extend_selection = 2  # PsSelectionType.psExtendSelection

strt_ruler_units = app.Preferences.RulerUnits
if strt_ruler_units != ps_pixels:
    app.Preferences.RulerUnits = ps_pixels

doc_ref = app.Documents.Add(320, 240)

# Rectangular selection inset by 50px → save to a new alpha channel
offset = 50
sel_bounds1 = (
    (offset, offset),
    (doc_ref.Width - offset, offset),
    (doc_ref.Width - offset, doc_ref.Height - offset),
    (offset, doc_ref.Height - offset),
)
doc_ref.Selection.Select(sel_bounds1)
sel_alpha = doc_ref.Channels.Add()
doc_ref.Selection.Store(sel_alpha)

# Second selection (horizontal band)
sel_bounds2 = ((0, 75), (doc_ref.Width, 75), (doc_ref.Width, 150), (0, 150))
doc_ref.Selection.Select(sel_bounds2)

# Load alpha and *extend* (union) with the active selection
doc_ref.Selection.Load(sel_alpha, ps_extend_selection, False)

app.Preferences.RulerUnits = strt_ruler_units
print("Combined selection loaded from alpha channel:", sel_alpha.Name)
