# This script demonstrates how you can use the action manager
# to execute the Emboss filter.

from win32com.client import Dispatch, GetActiveObject, GetObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

fileName = "C:\Git\PS_Samples_Files\Layer Comps.psd"
docRef = app.Open(fileName)

nLayerSets = docRef.LayerSets
nArtLayers = docRef.LayerSets.Item(len(nLayerSets)).ArtLayers

docRef.ActiveLayer = docRef.LayerSets.Item(len(nLayerSets)).ArtLayers.Item(len(nArtLayers))


def SmartSharpen(inAmount, inRadius, inNoise):

    idsmartSharpenID = app.stringIDToTypeID("smartSharpen")
    desc37 = Dispatch('Photoshop.ActionDescriptor')

    idpresetKind = app.stringIDToTypeID("presetKind")
    idpresetKindType = app.stringIDToTypeID("presetKindType")
    idpresetKindCustom = app.stringIDToTypeID("presetKindCustom")
    desc37.putEnumerated(idpresetKind, idpresetKindType, idpresetKindCustom)

    idAmnt = app.charIDToTypeID("Amnt")
    idPrc = app.charIDToTypeID("#Prc")
    desc37.putUnitDouble(idAmnt, idPrc, inAmount)

    idRds = app.charIDToTypeID("Rds ")
    idPxl = app.charIDToTypeID("#Pxl")
    desc37.putUnitDouble(idRds, idPxl, inRadius)

    idnoiseReduction = app.stringIDToTypeID("noiseReduction")
    idPrc = app.charIDToTypeID("#Prc")
    desc37.putUnitDouble(idnoiseReduction, idPrc, inNoise)

    idblur = app.charIDToTypeID("blur")
    idblurType = app.stringIDToTypeID("blurType")
    idGsnB = app.charIDToTypeID("GsnB")
    desc37.putEnumerated(idblur, idblurType, idGsnB)

    # now execute the action
    app.ExecuteAction(idsmartSharpenID, desc37)

SmartSharpen(300, 2.0, 20)
