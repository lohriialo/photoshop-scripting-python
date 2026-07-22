import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Document.Guides.Add — ruler guides for layout.

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences

app = get_app()

PS_HORIZONTAL = 1
PS_VERTICAL = 2

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        600, 400, 72, "Guides Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    doc.Guides.Add(PS_VERTICAL, 100)
    doc.Guides.Add(PS_VERTICAL, 500)
    doc.Guides.Add(PS_HORIZONTAL, 50)
    doc.Guides.Add(PS_HORIZONTAL, 350)
    print("Guide count:", doc.Guides.Count)
    for i in range(1, doc.Guides.Count + 1):
        g = doc.Guides.Item(i)
        print(f"  [{i}] direction={g.Direction} coordinate={g.Coordinate}")
