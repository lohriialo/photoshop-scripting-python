import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# ArtLayer.Duplicate — clone a layer inside the same document.

from photoshop_scripting import DocumentFill, DocumentMode, LayerKind, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        400, 300, 72, "DuplicateLayer Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    layer = doc.ArtLayers.Add()
    layer.Name = "Original"
    layer.Kind = int(LayerKind.TEXT)
    layer.TextItem.Contents = "Duplicate me"
    layer.TextItem.Position = (40, 80)

    copy = layer.Duplicate()
    copy.Name = "Copy"
    try:
        copy.Translate(30, 30)
    except Exception:
        pass
    print("Layers:", [doc.ArtLayers.Item(i).Name for i in range(1, doc.ArtLayers.Count + 1)])
