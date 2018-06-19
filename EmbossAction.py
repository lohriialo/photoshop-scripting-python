# This script demonstrates how you can use the action manager
# to execute the Emboss filter.
# Inorder to find all the IDs, see https://helpx.adobe.com/photoshop/kb/downloadable-plugins-and-content.html#ScriptingListenerplugin
# This blog here exlains what a script listener is http://blogs.adobe.com/crawlspace/2006/05/installing_and_1.html

from win32com.client import Dispatch, GetActiveObject, GetObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

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

    filterDescriptor = Dispatch('Photoshop.ActionDescriptor')
    filterDescriptor.PutInteger(keyAngleID, inAngle)
    filterDescriptor.PutInteger(keyHeightID, inHeight)
    filterDescriptor.PutInteger(keyAmountID, inAmount)

    app.ExecuteAction(eventEmbossID, filterDescriptor)

emboss( 120, 10, 100)
