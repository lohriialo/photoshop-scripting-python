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

import time

from win32com.client import Dispatch

from photoshop_scripting import get_app

# Longer Action Manager experiment: play actions + build solid-fill layers.
# Shows CharIDToTypeID, ActionDescriptor, ActionReference, ExecuteAction.
# Small sleeps help avoid "application is busy" COM errors during rapid calls.

app = get_app(backend="win32com")
ps_display_no_dialogs = 3

for index in range(5):  # shortened from 50 for a friendlier demo loop
    # Play "Sepia Toning (layer)" from Default Actions if present
    try:
        id_ply = app.CharIDToTypeID("Ply ")
        desc = Dispatch("Photoshop.ActionDescriptor")
        ref = Dispatch("Photoshop.ActionReference")
        ref.PutName(app.CharIDToTypeID("Actn"), "Sepia Toning (layer)")
        ref.PutName(app.CharIDToTypeID("ASet"), "Default Actions")
        desc.PutReference(app.CharIDToTypeID("null"), ref)
        app.ExecuteAction(id_ply, desc, ps_display_no_dialogs)
    except Exception as exc:
        print("DoAction skip:", exc)

    time.sleep(0.3)

    # Make a solid color fill layer (RGB from loop index)
    try:
        id_mk = app.CharIDToTypeID("Mk  ")
        desc21 = Dispatch("Photoshop.ActionDescriptor")
        ref12 = Dispatch("Photoshop.ActionReference")
        ref12.PutClass(app.StringIDToTypeID("contentLayer"))
        desc21.PutReference(app.CharIDToTypeID("null"), ref12)

        desc24 = Dispatch("Photoshop.ActionDescriptor")
        desc24.PutDouble(app.CharIDToTypeID("Rd  "), float(index * 40))
        desc24.PutDouble(app.CharIDToTypeID("Grn "), float(index * 20))
        desc24.PutDouble(app.CharIDToTypeID("Bl  "), float(index * 10))

        desc23 = Dispatch("Photoshop.ActionDescriptor")
        desc23.PutObject(app.CharIDToTypeID("Clr "), app.CharIDToTypeID("RGBC"), desc24)
        desc22 = Dispatch("Photoshop.ActionDescriptor")
        desc22.PutObject(
            app.CharIDToTypeID("Type"), app.StringIDToTypeID("solidColorLayer"), desc23
        )
        desc21.PutObject(
            app.CharIDToTypeID("Usng"), app.StringIDToTypeID("contentLayer"), desc22
        )
        app.ExecuteAction(id_mk, desc21, ps_display_no_dialogs)
    except Exception as exc:
        print("Fill layer skip:", exc)

    time.sleep(0.3)

print("Action Manager demo loop finished")
