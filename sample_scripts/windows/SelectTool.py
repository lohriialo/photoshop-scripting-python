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

# Application.CurrentTool is a string tool ID (e.g. marqueeRectTool, moveTool).

app = get_app()

print("Current tool:", app.CurrentTool)
# Switch tool by assigning a known ID:
# app.CurrentTool = "marqueeRectTool"
# app.CurrentTool = "moveTool"
