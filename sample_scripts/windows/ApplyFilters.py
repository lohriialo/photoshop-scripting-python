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

from photoshop_scripting import ensure_sample, get_app
from photoshop_scripting.app import create_solid_color
from photoshop_scripting.paths import as_ps_path

# Apply filter methods on ArtLayer after building selections.
# Demonstrates ApplyAddNoise, ApplyDiffuseGlow, ApplyGlassEffect.
# Use comtypes: Selection.Select needs array arguments.

app = get_app(backend="comtypes")

ps_display_no_dialogs = 3
app.displayDialogs = ps_display_no_dialogs

ps_pixels = 1
strt_ruler_units = app.Preferences.RulerUnits
if strt_ruler_units != ps_pixels:
    app.Preferences.RulerUnits = ps_pixels

file_name = as_ps_path(ensure_sample("Layer Comps.psd"))
doc_ref = app.Open(file_name)

# COM collections can be awkward with len(); counting via enumerate is reliable
n_layer_sets = len([(i, x) for i, x in enumerate(doc_ref.LayerSets, 1)])
n_art_layers = len(
    [(i, x) for i, x in enumerate(doc_ref.LayerSets[n_layer_sets].ArtLayers, 1)]
)

# Activate last art layer inside the last layer set
active_layer = doc_ref.ActiveLayer = doc_ref.LayerSets[n_layer_sets].ArtLayers[n_art_layers]

ps_replace_selection = 1
sel_area = ((0, 212), (300, 212), (300, 300), (0, 300))
doc_ref.Selection.Select(sel_area, ps_replace_selection, 20, True)

ps_gaussian_noise = 2  # PsNoiseDistribution
active_layer.ApplyAddNoise(15, ps_gaussian_noise, False)

back_color = create_solid_color(backend="comtypes")
back_color.HSB.Hue = 0
back_color.HSB.Saturation = 0
back_color.HSB.Brightness = 100
app.BackgroundColor = back_color

sel_area2 = ((120, 20), (210, 20), (210, 110), (120, 110))
doc_ref.Selection.Select(sel_area2, ps_replace_selection, 25, False)
active_layer.ApplyDiffuseGlow(9, 12, 15)
ps_tiny_lens_texture = 4  # PsTextureType
active_layer.ApplyGlassEffect(7, 3, 7, False, ps_tiny_lens_texture, None)
doc_ref.Selection.Deselect()

if strt_ruler_units != ps_pixels:
    app.Preferences.RulerUnits = strt_ruler_units
print("Applied Add Noise, Diffuse Glow, and Glass Effect to selections")
