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

# Create a text layer and set contents, size, position, and solid color.
# Uses comtypes-friendly SolidColor creation for reliable RGB assignment.

app = get_app(backend="comtypes")

strt_ruler_units = app.Preferences.RulerUnits
strt_type_units = app.Preferences.TypeUnits
ps_inches = 2       # PsUnits.psInches
ps_type_points = 5  # PsTypeUnits.psTypePoints
app.Preferences.RulerUnits = ps_inches
app.Preferences.TypeUnits = ps_type_points  # measure type size in points

# Suppress modal dialogs during automation
ps_display_no_dialogs = 3  # PsDialogModes.psDisplayNoDialogs
app.displayDialogs = ps_display_no_dialogs

# 7" x 5" @ 72 ppi document
doc_ref = app.Documents.Add(7, 5, 72)

# SolidColor is a COM object: set .RGB.Red/Green/Blue (0–255)
text_color = create_solid_color(backend="comtypes")
text_color.RGB.Red = 225
text_color.RGB.Green = 0
text_color.RGB.Blue = 0

new_text_layer = doc_ref.ArtLayers.Add()
ps_text_layer = 2  # PsLayerKind.psTextLayer
new_text_layer.Kind = ps_text_layer
new_text_layer.TextItem.Contents = "Hello, World!"
new_text_layer.TextItem.Position = [0.75, 0.75]  # inches (current ruler units)
new_text_layer.TextItem.Size = 36                 # points (type units)
new_text_layer.TextItem.Color = text_color

# Restore preferences
app.Preferences.RulerUnits = strt_ruler_units
app.Preferences.TypeUnits = strt_type_units
