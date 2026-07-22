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
from photoshop_scripting.paths import as_ps_path

# Open an existing file via Application.Open(path).
# Path must be absolute for reliable COM behaviour.

app = get_app()

# Sample PSD lives under sample_scripts/PS_Samples_Files/
file_name = as_ps_path(ensure_sample("Layer Comps.psd"))
doc_ref = app.Open(file_name)

print("Opened:", doc_ref.Name)
print("Size:", doc_ref.Width, "x", doc_ref.Height)
