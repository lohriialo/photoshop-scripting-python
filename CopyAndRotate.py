# Crop and rotate the active document.

from win32com.client import Dispatch, GetActiveObject, GetObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance

# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

# PS constants, see psCC2018.py
psPixels = 1
psNewRGB = 2
psWhite = 1

fileName = "C:\Git\photoshop-scripting-python\PS_Samples_Files\Layer Comps.psd"
srcDoc = app.Open(fileName)

strtRulerUnits = app.Preferences.RulerUnits
if strtRulerUnits is not psPixels:
    app.Preferences.RulerUnits = psPixels

# crop a 10 pixel border from the image
bounds = [10, 10, srcDoc.Width - 10, srcDoc.Height - 10]
srcDoc.RotateCanvas(45)
srcDoc.Crop(bounds)

# set ruler back to where it was
app.Preferences.RulerUnits = strtRulerUnits
