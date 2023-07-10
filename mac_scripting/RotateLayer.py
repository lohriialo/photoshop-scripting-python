# This scripts demonstrates how to rotate a layer 45 degrees clockwise.

from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

# ps.count(None, each=k.documents) also works instead of len() here
if len(ps.documents()) > 0:
    if ps.current_document.current_layer.background_layer() == False:
        docRef = ps.current_document()
        layerRef = docRef.current_layer()
        layerRef.rotate(angle=45.0)
    else:
        print("Operation cannot be performed on background layer")
else:
    print("You must have at least one open document to run this script!")
