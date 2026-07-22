"""
Photoshop scripting sample (Python / Windows COM).
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from photoshop_scripting import require_windows_com

require_windows_com()  # these samples use the Windows COM object model

from photoshop_scripting import get_app

# ArtLayer.Rotate(angle) — rotates the active non-background layer.

app = get_app()

if app.Documents.Count < 1:
    print("You must have at least one open document to run this script!")
elif app.ActiveDocument.ActiveLayer.IsBackgroundLayer:
    print("Operation cannot be performed on background layer")
else:
    doc_ref = app.ActiveDocument
    # Layers[0] may work with some COM bridges; Item(1) is the portable form
    try:
        layer_ref = doc_ref.Layers[0]
    except Exception:
        layer_ref = doc_ref.Layers.Item(1)
    layer_ref.Rotate(45.0)
    print("Rotated layer 45°:", layer_ref.Name)
