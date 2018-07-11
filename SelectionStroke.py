# Create a stroke around the current selection.
# Set the stroke color and width of the new stroke.
from win32com.client import Dispatch, GetActiveObject
from comtypes.client import GetActiveObject, CreateObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

if len([(i, x) for i, x in enumerate(app.Documents, 1)]) > 0:
    if app.ActiveDocument.ActiveLayer.IsBackgroundLayer == False:

        psPixels = 1
        strtRulerUnits = app.Preferences.RulerUnits
        app.Preferences.RulerUnits = psPixels

        selRef = app.ActiveDocument.Selection
        offset = 10
        selBounds = ((offset, offset),
                     (app.ActiveDocument.Width - offset, offset),
                     (app.ActiveDocument.Width - offset, app.ActiveDocument.Height - offset),
                     (offset, app.ActiveDocument.Height - offset))

        selRef.Select(selBounds)
        selRef.SelectBorder(5)

        # create text color properties
        strokeColor = CreateObject("Photoshop.SolidColor")
        strokeColor.CMYK.Cyan = 20
        strokeColor.CMYK.Magenta = 90
        strokeColor.CMYK.Yellow = 50
        strokeColor.CMYK.Black = 50

        # We don't want any Photoshop dialogs displayed during automated execution
        psDisplayNoDialogs = 3  # from enum PsDialogModes
        app.displayDialogs = psDisplayNoDialogs
        psOutsideStroke = 3  # from enum PsStrokeLocation
        psVividLightBlend = 15  # from enum PsColorBlendMode
        selRef.Stroke(strokeColor, 2, psOutsideStroke, psVividLightBlend, 75, True)

        # Set ruler units back the way we found it
        app.Preferences.RulerUnits = strtRulerUnits


    else:
        print("Operation cannot be performed on background layer")
else:
    print("Create a document with an active selection before running this script!")