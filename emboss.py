# This script demonstrates how you can use the action manager
# to execute the Emboss filter.

import win32com.client
import pscc2018 as ps

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance

# app = win32com.client.Dispatch('Photoshop.Application')
app = win32com.client.GetActiveObject("Photoshop.Application")

fileName = "C:\Git\photoshop-scripting-python\PS_Samples_Files\Layer Comps.psd"
docRef = app.Open(fileName)

nLayerSets = docRef.LayerSets
nArtLayers = docRef.LayerSets.Item(len(nLayerSets)).ArtLayers

docRef.ActiveLayer = docRef.LayerSets.Item(len(nLayerSets)).ArtLayers.Item(len(nArtLayers))

def emboss(inAngle, inHeight, inAmount):
    # Get ID's for the related keys
    keyAngleID = app.CharIDToTypeID("Angl")
    keyHeightID = app.CharIDToTypeID("Hght")
    keyAmountID = app.CharIDToTypeID("Amnt")
    eventEmbossID = app.CharIDToTypeID("Embs")

    filterDescriptor = ps.ActionDescriptor()
    filterDescriptor.PutInteger(keyAngleID, inAngle)
    filterDescriptor.PutInteger(keyHeightID, inHeight)
    filterDescriptor.PutInteger(keyAmountID, inAmount)

    app.ExecuteAction(eventEmbossID, filterDescriptor)

emboss( 120, 10, 100)
