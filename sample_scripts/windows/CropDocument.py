import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Document.Crop — crop to pixel bounds [left, top, right, bottom].

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        800, 600, 72, "Crop Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    print("Before:", doc.Width, "x", doc.Height)
    doc.Crop([50, 50, 750, 550])
    print("After:", doc.Width, "x", doc.Height)
