import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Document.Flatten — merge everything to a single background layer.

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        400, 300, 72, "Flatten Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    doc.ArtLayers.Add().Name = "Layer 1"
    doc.ArtLayers.Add().Name = "Layer 2"
    print("Before flatten — art layers:", doc.ArtLayers.Count)
    doc.Flatten()
    print("After flatten — art layers:", doc.ArtLayers.Count)
