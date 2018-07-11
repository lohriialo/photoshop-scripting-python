# Get the active document and make a new selection.
from comtypes.client import GetActiveObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

# create new document if no document is opened
if len([(i, x) for i, x in enumerate(app.Documents, 1)]) < 1:
    psPixels = 1
    strtRulerUnits = app.Preferences.RulerUnits
    app.Preferences.RulerUnits = psPixels
    psNewRGB = 2  # from enum PsNewDocumentMode
    psWhite = 1  # from enum PsDocumentFill
    docRef = app.Documents.Add(320, 240, 72, None, psNewRGB, psWhite)
    app.preferences.rulerUnits = strtRulerUnits
else:
    docRef = app.ActiveDocument

sel_area = ((50, 60), (150, 60), (150, 120), (50, 120))
psReplaceSelection = 1  # from enum PsSelectionType
docRef.Selection.Select(sel_area, psReplaceSelection, 5.5, False)
