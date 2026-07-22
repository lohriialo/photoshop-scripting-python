import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Application.DoJavaScript — run ExtendScript from Python.
# Escape hatch when a COM binding is awkward or missing.

from photoshop_scripting import get_app
from photoshop_scripting.actions import do_javascript

app = get_app()

jsx = (
    'var doc = app.documents.add(300, 200, 72, "JSX Bridge Demo");'
    "var layer = doc.artLayers.add();"
    "layer.kind = LayerKind.TEXT;"
    'layer.textItem.contents = "From JSX via Python";'
    "layer.textItem.size = 24;"
    "doc.name;"
)
result = do_javascript(app, jsx)
print("DoJavaScript returned:", result)
