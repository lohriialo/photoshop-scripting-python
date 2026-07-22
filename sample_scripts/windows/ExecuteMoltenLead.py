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
from photoshop_scripting.actions import do_action
from photoshop_scripting.paths import as_ps_path

# Play a named action from the Actions panel.
# Application.DoAction(actionName, actionSet) — names must match exactly.
# (We use the small do_action helper which builds the same descriptor.)

app = get_app()

file_name = as_ps_path(ensure_sample("Layer Comps.psd"))
doc_ref = app.Open(file_name)

# Requires the default "Molten Lead" action in set "Default Actions"
do_action(app, "Molten Lead", "Default Actions")
# Equivalent: app.DoAction("Molten Lead", "Default Actions")
print("Played action: Molten Lead / Default Actions")
