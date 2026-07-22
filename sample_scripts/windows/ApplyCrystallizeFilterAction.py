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

from win32com.client import Dispatch

from photoshop_scripting import ensure_sample, get_app
from photoshop_scripting.paths import as_ps_path

# Action Manager for Filter > Pixelate > Crystallize (cell size parameter).

app = get_app(backend="win32com")

file_name = as_ps_path(ensure_sample("Layer Comps.psd"))
doc_ref = app.Open(file_name)

n_layer_sets = doc_ref.LayerSets
n_art_layers = doc_ref.LayerSets.Item(len(n_layer_sets)).ArtLayers
doc_ref.ActiveLayer = doc_ref.LayerSets.Item(len(n_layer_sets)).ArtLayers.Item(
    len(n_art_layers)
)


def apply_crystallize(cell_size):
    cell_size_id = app.CharIDToTypeID("ClSz")
    event_id = app.CharIDToTypeID("Crst")
    desc = Dispatch("Photoshop.ActionDescriptor")
    desc.PutInteger(cell_size_id, cell_size)
    app.ExecuteAction(event_id, desc)


apply_crystallize(25)
print("Crystallize applied (cell size 25)")
