# This scripts demonstrates how to link two layers.

from win32com.client import Dispatch, GetActiveObject, GetObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

# PS constants, see psCC2018.py
psPixels = 1
psNewRGB = 2
psWhite = 1

strtRulerUnits = app.Preferences.RulerUnits

if len(app.Documents) < 1:
    if strtRulerUnits is not psPixels:
        app.Preferences.RulerUnits = psPixels
    docRef = app.Documents.Add(320, 240, 72, None, psNewRGB, psWhite)
else:
    docRef = app.ActiveDocument

layerRef = docRef.ArtLayers.Add()
layerRef2 = docRef.ArtLayers.Add()
layerRef.Link(layerRef2)

# Set the ruler back to where it was
app.Preferences.RulerUnits = strtRulerUnits