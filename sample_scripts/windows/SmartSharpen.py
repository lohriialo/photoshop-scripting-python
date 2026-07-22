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

# Action Manager: build an ActionDescriptor and ExecuteAction.
# IDs come from ScriptListener (stringID / charID). See docs/action_manager.md

app = get_app(backend="win32com")

file_name = as_ps_path(ensure_sample("Layer Comps.psd"))
doc_ref = app.Open(file_name)

n_layer_sets = doc_ref.LayerSets
n_art_layers = doc_ref.LayerSets.Item(len(n_layer_sets)).ArtLayers
doc_ref.ActiveLayer = doc_ref.LayerSets.Item(len(n_layer_sets)).ArtLayers.Item(
    len(n_art_layers)
)


def smart_sharpen(in_amount, in_radius, in_noise):
    """Run Filter > Sharpen > Smart Sharpen via Action Manager."""
    id_smart = app.stringIDToTypeID("smartSharpen")
    desc = Dispatch("Photoshop.ActionDescriptor")

    # presetKind = custom
    desc.putEnumerated(
        app.stringIDToTypeID("presetKind"),
        app.stringIDToTypeID("presetKindType"),
        app.stringIDToTypeID("presetKindCustom"),
    )
    # amount (%), radius (px), noise reduction (%)
    desc.putUnitDouble(app.charIDToTypeID("Amnt"), app.charIDToTypeID("#Prc"), in_amount)
    desc.putUnitDouble(app.charIDToTypeID("Rds "), app.charIDToTypeID("#Pxl"), in_radius)
    desc.putUnitDouble(
        app.stringIDToTypeID("noiseReduction"), app.charIDToTypeID("#Prc"), in_noise
    )
    # blur type = Gaussian
    desc.putEnumerated(
        app.charIDToTypeID("blur"),
        app.stringIDToTypeID("blurType"),
        app.charIDToTypeID("GsnB"),
    )
    app.ExecuteAction(id_smart, desc)


smart_sharpen(300, 2.0, 20)
print("Smart Sharpen applied via ExecuteAction")
