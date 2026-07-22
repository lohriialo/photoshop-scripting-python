import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Document.ResizeCanvas — expand/shrink canvas without resampling pixels.

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences
from photoshop_scripting.constants import AnchorPosition

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        400, 300, 72, "ResizeCanvas Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    print("Before:", doc.Width, "x", doc.Height)
    doc.ResizeCanvas(
        float(doc.Width) + 80,
        float(doc.Height) + 80,
        int(AnchorPosition.MIDDLE_CENTER),
    )
    print("After:", doc.Width, "x", doc.Height)
