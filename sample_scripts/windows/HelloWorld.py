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

# --- Application ---
# Connect to Photoshop (launches or attaches to a running instance).
app = get_app()

# --- Document ---
# Documents.Add(width, height, resolution=..., name=...) creates a new doc.
# Units follow Preferences.RulerUnits (default is often pixels).
doc_ref = app.Documents.Add(320, 240)

# --- Layer ---
# ArtLayers.Add() creates a normal raster layer on top of the stack.
layer_ref = doc_ref.ArtLayers.Add()

# PsLayerKind: 1=normal, 2=text, …  Convert this layer into a text layer.
ps_text_layer = 2  # PsLayerKind.psTextLayer
layer_ref.Kind = ps_text_layer

# --- TextItem ---
# Text layers expose .TextItem for contents, font metrics, and position.
text_item = layer_ref.TextItem
text_item.Contents = "HELLO WORLD!"
text_item.Position = (120, 120)  # (x, y) in current ruler units
