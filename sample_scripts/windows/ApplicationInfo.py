import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# Application object — name, version, path, preferences, documents count.
# Core entry point for almost every script.

from photoshop_scripting import get_app

app = get_app()

print("Name:", app.Name)
print("Version:", app.Version)
try:
    print("Path:", app.Path)
except Exception as exc:
    print("Path: (unavailable)", exc)
try:
    print("Open documents:", app.Documents.Count)
except Exception:
    print("Open documents:", len(list(app.Documents)))
print("Ruler units:", int(app.Preferences.RulerUnits))
try:
    print("Display dialogs:", int(app.displayDialogs))
except Exception:
    print("Display dialogs:", int(app.DisplayDialogs))
print("Preferences.TypeUnits:", int(app.Preferences.TypeUnits))
