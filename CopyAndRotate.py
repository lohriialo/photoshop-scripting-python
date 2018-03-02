# Crop and rotate the active document.

import win32com.client

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance

# app = win32com.client.Dispatch('Photoshop.Application')
app = win32com.client.GetActiveObject("Photoshop.Application")

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
