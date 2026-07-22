import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Layer.Visible — show/hide layers (basis of export-layers workflows).

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        400, 300, 72, "HideShow Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    a = doc.ArtLayers.Add()
    a.Name = "A"
    b = doc.ArtLayers.Add()
    b.Name = "B"

    b.Visible = False
    print("After hiding B:")
    for i in range(1, doc.ArtLayers.Count + 1):
        layer = doc.ArtLayers.Item(i)
        print(f"  {layer.Name}: visible={layer.Visible}")
    b.Visible = True
    print("B shown again:", b.Visible)
