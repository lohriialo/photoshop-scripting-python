# This scripts demonstrates how to link two layers.

from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

strtRulerUnits = ps.settings.ruler_units()

if len(ps.documents()) < 1:
    ps.settings.ruler_units.set(k.pixel_units)
    docRef = ps.make(new=k.document, with_properties={
            k.width: 320, k.height: 240, k.resolution: 72, k.mode: k.RGB, k.initial_fill: k.white
        }
    )
else:
    docRef = ps.current_document()

layerRef = docRef.make(new=k.art_layer)
layerRef2 = docRef.make(new=k.art_layer)
layerRef.link(with_=layerRef2)

# Set the ruler back to where it was
ps.settings.ruler_units.set(strtRulerUnits)