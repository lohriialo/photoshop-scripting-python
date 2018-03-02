# This example makes a creates a selection in the activeDocument, copies the selection,
# to the clipboard, creates a new document of the same dimensions
# and pastes the contents of the clipboard into it.
# It ensures that rulerUnits are set before creating the new document.
# It checks the kind of the layer before making the selection to be
# sure not to copy a text layer.

import win32com.client
import comtypes.client
from array import array

# Start up Photoshop application
# app = win32com.client.Dispatch('Photoshop.Application')

# Or get Reference to already running Photoshop application instance
# app = win32com.client.GetObject(Class="Photoshop.Application")
# app = win32com.client.GetActiveObject("Photoshop.Application")

# using comtypes instead on win32com
# why? see sel_area below, also http://discourse.techart.online/t/selecting-in-photoshop-using-python-doesnt-work/205
app = comtypes.client.GetActiveObject("Photoshop.Application")

# PS constants, see psCC2018.py
psInches = 2
psPixels = 1
psNewRGB = 2
psWhite = 1
psTextLayer = 2
psReplaceSelection = 1

strtRulerUnits = app.Preferences.RulerUnits
if strtRulerUnits is not psInches:
    app.Preferences.RulerUnits = psInches

srcDoc = app.Documents.Add(7, 5, 72, None, psNewRGB, psWhite)

# Make sure the active layer is not a text layer, which cannot be copied to the clipboard
if srcDoc.ActiveLayer.Kind != psTextLayer:
    # Select the left half of the document. Selections are always expressed
    # in pixels regardless of the current ruler unit type, so we're computing
    # the selection corner points based on the inch unit width and height
    # of the document
    x2 = (srcDoc.Width * srcDoc.Resolution) / 2
    y2 = srcDoc.Height * srcDoc.Resolution

    # srcDoc.Selection.Select([(0, 0), (x2, 0), (x2), (y2), (0, y2)], psReplaceSelection, 0, False)

    sel_area = ((0, 0), (x2, 0), (x2, y2), (0, y2))
    # sel_area argument not accepted if using win32com, using comtypes instead
    srcDoc.Selection.Select(sel_area, psReplaceSelection, 0, False)

    srcDoc.Selection.Copy()

    # The new doc is created
    # need to change ruler units to pixels because x2 and y2 are pixel units.
    app.Preferences.RulerUnits = psPixels
    pasteDoc = app.Documents.Add(x2, y2, srcDoc.Resolution, "Paste Target")
    pasteDoc.Paste()
else:
    print("You cannot copy from a text layer")

if strtRulerUnits != app.Preferences.RulerUnits:
    app.Preferences.RulerUnits = strtRulerUnits




