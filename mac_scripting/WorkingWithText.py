# Create a new art layer and convert it to a text layer.
# Set its contents, size and color.

from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

strtRulerUnits = ps.settings.ruler_units()
strtTypeUnits = ps.settings.type_units()
ps.settings.ruler_units.set(k.inch_units)
ps.settings.type_units.set(k.point_units)

# suppress all dialogs
ps.display_dialogs.set(k.never)

# create a new document
docRef = ps.make(new=k.document, with_properties={k.width:7, k.height:5, k.resolution:72})

# create text color properties
textColor = {k.class_: k.RGB_color_, k.red: 225, k.green: 0, k.blue: 0}

# add a new text layer to document and apply the text color
# note: we can make the new layer and set the kind property in one command.
newTextLayer = docRef.make(
    new=k.art_layer,
    with_properties={k.kind: k.text_layer}
)
newTextLayer.text_object.contents.set("Hello, World!")
newTextLayer.text_object.position.set([0.75, 0.75])
newTextLayer.text_object.size.set(36)
newTextLayer.text_object.stroke_color.set(textColor)

# set the app preference the way it was before the operation
ps.settings.ruler_units.set(strtRulerUnits)
ps.settings.type_units.set(strtTypeUnits)
