import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# LayerSets.Add — create a layer group (folder).

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        400, 300, 72, "LayerSet Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    layer = doc.ArtLayers.Add()
    layer.Name = "Grouped layer"

    group = doc.LayerSets.Add()
    group.Name = "My Group"
    try:
        layer.Move(group, 2)
    except Exception:
        try:
            layer.MoveToEnd(group)
        except Exception as exc:
            print("Created group; move API note:", exc)

    print("Layer sets:", doc.LayerSets.Count, "—", group.Name)
