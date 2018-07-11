# This scripts demonstrates how to rotate a layer 45 degrees clockwise.
from win32com.client import Dispatch, GetActiveObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

if len(app.Documents) > 0:
    if app.ActiveDocument.ActiveLayer.IsBackgroundLayer == False:
        docRef = app.ActiveDocument
        layerRef = docRef.Layers[0]
        layerRef.Rotate(45.0)
    else:
        print("Operation cannot be performed on background layer")
else:
    print("You must have at least one open document to run this script!")