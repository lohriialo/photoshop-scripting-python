import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Document.ResizeImage — width/height/resolution + resample method.

from photoshop_scripting import DocumentFill, DocumentMode, ResampleMethod, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        1000, 800, 72, "ResizeImage Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    print("Before:", doc.Width, "x", doc.Height, "@", doc.Resolution)
    new_h = (float(doc.Height) / float(doc.Width)) * 500
    doc.ResizeImage(500, new_h, 72, int(ResampleMethod.BICUBIC_SHARPER))
    print("After:", doc.Width, "x", doc.Height, "@", doc.Resolution)
