# This sample script shows how to apply 3 different filters to
# selections in the open document.

# from win32com.client import Dispatch, GetActiveObject, GetObject
from comtypes.client import GetActiveObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

# We don't want any Photoshop dialogs displayed during automated execution
psDisplayNoDialogs = 3 # from enum PsDialogModes
app.displayDialogs = psDisplayNoDialogs

psPixels = 1
strtRulerUnits = app.Preferences.RulerUnits
if strtRulerUnits is not psPixels:
    app.Preferences.RulerUnits = psPixels

fileName = "C:\Git\PS_Samples_Files\Layer Comps.psd"
docRef = app.Open(fileName)

nLayerSets = len([(i, x) for i, x in enumerate(docRef.LayerSets, 1)])
# for some reason, len(docRef.LayerSets) return errors
# So above list comprehension is same as below
# nLayerSets = 0
# for layerSet in docRef.LayerSets:
#     nLayerSets += 1

nArtLayers = len([(i, x) for i, x in enumerate(docRef.LayerSets[nLayerSets].ArtLayers, 1)])

active_layer = docRef.ActiveLayer = docRef.LayerSets[nLayerSets].ArtLayers[nArtLayers]
# print(docRef.ActiveLayer.Name)
psReplaceSelection = 1  # from enum PsSelectionType
# # sel_area argument not accepted if using win32com, using comtypes instead
sel_area = ((0, 212), (300, 212), (300, 300), (0, 300))
docRef.Selection.Select(sel_area, psReplaceSelection, 20, True)
psGaussianNoise = 2     # from enum PsNoiseDistribution
active_layer.ApplyAddNoise(15, psGaussianNoise, False)

sel_area2 = ((120, 20), (210, 20), (210, 110), (120, 110))
docRef.Selection.Select(sel_area2, psReplaceSelection, 25, False)
active_layer.ApplyDiffuseGlow(9, 12, 15)
psTinyLensTexture = 4   # from enum PsTextureType
active_layer.ApplyGlassEffect(7, 3, 7, False, psTinyLensTexture, None)
docRef.Selection.Deselect()

# Set ruler units back the way we found it
if strtRulerUnits is not psPixels:
    app.Preferences.RulerUnits = strtRulerUnits

