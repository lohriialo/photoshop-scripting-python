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

# Import a variables/data-sets file via Action Manager (data-driven graphics).
# Requires an open template document that defines variables.

app = get_app(backend="win32com")

if app.Documents.Count < 1:
    print("Open a template document with variables before running this script.")
else:
    dialog_mode = 3  # no dialogs
    data_file = as_ps_path(ensure_sample("ps_data_sets.txt"))

    desc = Dispatch("Photoshop.ActionDescriptor")
    ref = Dispatch("Photoshop.ActionReference")
    ref.putClass(app.StringIDToTypeID("dataSetClass"))
    desc.putReference(app.charIDToTypeID("null"), ref)
    desc.putPath(app.charIDToTypeID("Usng"), data_file)
    desc.putEnumerated(
        app.charIDToTypeID("Encd"),
        app.stringIDToTypeID("dataSetEncoding"),
        app.stringIDToTypeID("dataSetEncodingAuto"),
    )
    desc.putBoolean(app.stringIDToTypeID("eraseAll"), True)
    desc.putBoolean(app.stringIDToTypeID("useFirstColumn"), True)
    app.ExecuteAction(app.stringIDToTypeID("importDataSets"), desc, dialog_mode)
    print("Imported data sets from", data_file)
