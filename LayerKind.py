# This script demonstrates how to create a new layer and set its kind.

from win32com.client import Dispatch, GetActiveObject, GetObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

# PS constants, see psCC2018.py
psPixels = 1
psNewRGB = 2
psWhite = 1
psTextLayer = 2  # from enum PsLayerKind

strtRulerUnits = app.Preferences.RulerUnits

if len(app.Documents) < 1:
    if strtRulerUnits is not psPixels:
        app.Preferences.RulerUnits = psPixels
    docRef = app.Documents.Add(320, 240, 72, None, psNewRGB, psWhite)
else:
    docRef = app.ActiveDocument

layerRef = docRef.ArtLayers.Add()
layerRef.Kind = psTextLayer
# Set the ruler back to where it was
app.Preferences.RulerUnits = strtRulerUnits
