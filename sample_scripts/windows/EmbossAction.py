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

# Action Manager for Filter > Stylize > Emboss.
# Record with ScriptListener, then translate putInteger / ExecuteAction.

app = get_app(backend="win32com")

file_name = as_ps_path(ensure_sample("Layer Comps.psd"))
doc_ref = app.Open(file_name)

n_layer_sets = doc_ref.LayerSets
n_art_layers = doc_ref.LayerSets.Item(len(n_layer_sets)).ArtLayers
doc_ref.ActiveLayer = doc_ref.LayerSets.Item(len(n_layer_sets)).ArtLayers.Item(
    len(n_art_layers)
)


def emboss(in_angle, in_height, in_amount):
    key_angle = app.CharIDToTypeID("Angl")
    key_height = app.CharIDToTypeID("Hght")
    key_amount = app.CharIDToTypeID("Amnt")
    event_emboss = app.CharIDToTypeID("Embs")

    desc = Dispatch("Photoshop.ActionDescriptor")
    desc.PutInteger(key_angle, in_angle)
    desc.PutInteger(key_height, in_height)
    desc.PutInteger(key_amount, in_amount)
    app.ExecuteAction(event_emboss, desc)


emboss(120, 10, 100)
print("Emboss applied via Action Manager")
