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

# Toggle which layer is ActiveLayer — many commands act only on ActiveLayer / ActiveDocument.

app = get_app()

# Ensure there is a document and at least two layers to switch between.
if app.Documents.Count < 1:
    doc_ref = app.Documents.Add()
else:
    doc_ref = app.ActiveDocument

if doc_ref.Layers.Count < 2:
    doc_ref.ArtLayers.Add()

# Layers collection is 1-based in COM (Item(1) is the first layer).
last_index = doc_ref.Layers.Count
first_index = 1

if doc_ref.ActiveLayer.Name != doc_ref.Layers.Item(last_index).Name:
    # Jump to the last layer in the stack
    doc_ref.ActiveLayer = doc_ref.Layers.Item(last_index)
else:
    # Already on last — jump to first
    doc_ref.ActiveLayer = doc_ref.Layers.Item(first_index)

print("Active layer is now:", doc_ref.ActiveLayer.Name)
