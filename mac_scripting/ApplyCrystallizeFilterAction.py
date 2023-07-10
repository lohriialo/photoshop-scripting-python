# This script demonstrates how you can use the action manager
# to execute the Crystallize filter.

from os.path import abspath
from appscript import app, mactypes

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

# This must be an absolute path.
fileName = abspath("../PS_Samples_Files/Layer Comps.psd")
ps.open(fileName)
docRef = ps.current_document()

nLayerSets = docRef.layer_sets
nArtLayers = docRef.layer_sets[-1].art_layers

# get the last layer in LayerSets
docRef.current_layer.set(docRef.layer_sets[-1].art_layers[-1])

# custom actions like this must be done as Javascript, unfortunately
def applyCrystallize(cellSize):
    script = """
    cellSizeID = charIDToTypeID("ClSz");
    eventCrystallizeID = charIDToTypeID("Crst");
    filterDescriptor = new ActionDescriptor();
    filterDescriptor.putInteger(cellSizeID, arguments[0]);
    executeAction(eventCrystallizeID, filterDescriptor);
    """
    ps.do_javascript(script, with_arguments=[cellSize])

applyCrystallize(25)
