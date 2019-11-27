# This script demonstrates how you can use the action manager
# to execute the Crystallize filter.
# In order to find all the IDs, see https://helpx.adobe.com/photoshop/kb/downloadable-plugins-and-content.html#ScriptingListenerplugin
# This blog here explains what a script listener is http://blogs.adobe.com/crawlspace/2006/05/installing_and_1.html

from win32com.client import Dispatch, GetActiveObject

# Start up Photoshop application
# app = Dispatch('Photoshop.Application')

# Or get Reference to already running Photoshop instance
app = GetActiveObject("Photoshop.Application")

fileName = "C:\Git\photoshop-scripting-python\PS_Samples_Files\Layer Comps.psd"
docRef = app.Open(fileName)

nLayerSets = docRef.LayerSets
nArtLayers = docRef.LayerSets.Item(len(nLayerSets)).ArtLayers

# get the last layer in LayerSets
docRef.ActiveLayer = docRef.LayerSets.Item(len(nLayerSets)).ArtLayers.Item(len(nArtLayers))

def applyCrystallize(cellSize):
    cellSizeID = app.CharIDToTypeID("ClSz")
    eventCrystallizeID = app.CharIDToTypeID("Crst")

    filterDescriptor = Dispatch('Photoshop.ActionDescriptor')
    filterDescriptor.PutInteger(cellSizeID, cellSize)

    app.ExecuteAction(eventCrystallizeID, filterDescriptor)

applyCrystallize(25)

