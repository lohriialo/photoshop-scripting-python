import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from photoshop_scripting import require_windows_com
require_windows_com()

# SaveAs with JPEGSaveOptions — the most common export path.

import tempfile
from pathlib import Path

from comtypes.client import CreateObject

from photoshop_scripting import DocumentFill, DocumentMode, Units, get_app, saved_preferences
from photoshop_scripting.constants import SaveOptions

app = get_app()

with saved_preferences(app, units=Units.PIXELS):
    doc = app.Documents.Add(
        640, 480, 72, "SaveAsJPEG Demo", int(DocumentMode.RGB), int(DocumentFill.WHITE)
    )
    opts = CreateObject("Photoshop.JPEGSaveOptions")
    opts.Quality = 10
    opts.EmbedColorProfile = True
    opts.FormatOptions = 1

    dest = Path(tempfile.gettempdir()) / "ps_sample_saveas.jpg"
    doc.SaveAs(str(dest), opts, True)
    doc.Close(int(SaveOptions.DO_NOT_SAVE))
    print("Saved:", dest)
