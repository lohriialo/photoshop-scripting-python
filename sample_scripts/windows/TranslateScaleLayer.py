import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# ArtLayer.Translate and Resize — move/scale layer content.

from photoshop_scripting import DocumentFill, DocumentMode, LayerKind, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        500, 400, 72, "Transform Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    layer = doc.ArtLayers.Add()
    layer.Kind = int(LayerKind.TEXT)
    layer.TextItem.Contents = "Move & scale"
    layer.TextItem.Size = 36
    layer.TextItem.Position = (40, 100)

    layer.Translate(60, 40)
    try:
        layer.Resize(120, 120)
        print("Translated and scaled layer:", layer.Name)
    except Exception as exc:
        print("Translated; Resize note:", exc)
