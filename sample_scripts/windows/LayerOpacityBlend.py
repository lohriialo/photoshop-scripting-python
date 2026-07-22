import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Layer.Opacity and BlendMode — fundamental compositing controls.

from photoshop_scripting import BlendMode, DocumentFill, DocumentMode, Units, get_app, saved_preferences

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        400, 300, 72, "OpacityBlend Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    layer = doc.ArtLayers.Add()
    layer.Name = "Soft overlay"
    layer.Opacity = 50.0
    layer.BlendMode = int(BlendMode.MULTIPLY)
    print(f"Layer {layer.Name!r}: opacity={layer.Opacity}, blend={layer.BlendMode}")
