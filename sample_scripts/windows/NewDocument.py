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

# Create a document measured in *inches* by temporarily changing ruler units.

app = get_app()

# Always save and restore preferences you change — be a good citizen.
strt_ruler_units = app.Preferences.RulerUnits
ps_inches = 2  # PsUnits.psInches
app.Preferences.RulerUnits = ps_inches

# Documents.Add(width, height, resolution, name)
# With inches as ruler units, 4 x 4 means a 4-inch square at 72 ppi.
doc_ref = app.Documents.Add(4, 4, 72.0, "My New Document")

app.Preferences.RulerUnits = strt_ruler_units
print("Created:", doc_ref.Name)
