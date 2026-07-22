import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Document metrics — size, resolution, mode, bit depth, layer counts.

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    if app.Documents.Count < 1:
        doc = app.Documents.Add(
            800, 600, 72, "DocumentInfo Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
        )
    else:
        doc = app.ActiveDocument

    print("Name:", doc.Name)
    print("Width x Height:", doc.Width, "x", doc.Height)
    print("Resolution:", doc.Resolution)
    print("Mode:", doc.Mode)
    print("Bits per channel:", doc.BitsPerChannel)
    print("Art layers:", doc.ArtLayers.Count)
    print("Layer sets:", doc.LayerSets.Count)
    print("Channels:", doc.Channels.Count)
    try:
        print("Path:", doc.FullName)
    except Exception:
        print("Path: (unsaved document)")
