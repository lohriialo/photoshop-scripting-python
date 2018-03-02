# Fill the current selection with an RGB color.

from win32com.client import Dispatch, GetActiveObject, GetObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = win32com.client.Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")


# PS constants, see psCC2018.py
psPixels = 1
psNewRGB = 2
psWhite = 1
psNormalBlendColor = 2

strtRulerUnits = app.Preferences.RulerUnits

if len(app.Documents) < 1:
    if strtRulerUnits is not psPixels:
        app.Preferences.RulerUnits = psPixels
    docRef = app.Documents.Add(320, 240, 72, None, psNewRGB, psWhite)
    docRef.ArtLayers.Add()
    app.Preferences.RulerUnits = strtRulerUnits

if app.ActiveDocument.ActiveLayer.IsBackgroundLayer == False:
    selRef = app.ActiveDocument.Selection
    fillcolor = Dispatch("Photoshop.SolidColor")
    fillcolor.RGB.Red = 225
    fillcolor.RGB.Green = 0
    fillcolor.RGB.Blue = 0
    selRef.Fill(fillcolor, psNormalBlendColor, 25, False)
else:
    print("Can't perform operation on background layer")
