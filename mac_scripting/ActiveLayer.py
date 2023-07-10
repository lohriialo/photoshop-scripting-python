# Set the active layer to the last art layer of the active document, or the
# first if the last is already active.

from appscript import app, k
ps = app(id="com.adobe.Photoshop", terms="sdef")

# We could also use "ps.count(None, k.documents)" here, if
# we expect many documents to be open and speed was of concern.
if len(ps.documents()) < 1:
    docRef = ps.make(new=k.document)
else:
    docRef = ps.current_document

if len(docRef.layers()) < 2:
    docRef.make(new=k.art_layer)

if docRef.current_layer() != docRef.layers[-1]():
    docRef.current_layer.set(docRef.layers[-1])
else:
    docRef.current_layer.set(docRef.layers[1])
