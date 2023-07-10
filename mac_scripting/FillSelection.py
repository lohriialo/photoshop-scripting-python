# Fill the current selection with an RGB color.

from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

strtRulerUnits = ps.settings.ruler_units()

if len(ps.documents()) < 1:
    ps.settings.ruler_units.set(k.pixel_units)
    docRef = ps.make(
        new=k.document,
        with_properties={
            k.width: 320, k.height: 240, k.resolution: 72, k.mode: k.RGB, k.initial_fill: k.white
        }
    )
    docRef.make(new=k.art_layer)
    ps.settings.ruler_units.set(strtRulerUnits)

if ps.current_document.current_layer.background_layer() == False:
    selRef = ps.current_document.selection
    # Note the "_" here in both RGB_color_ and class_
    fillcolor = {k.class_: k.RGB_color_, k.red: 255, k.green: 0, k.blue: 0}
    selRef.fill(
        with_contents=fillcolor, blend_mode=k.normal, opacity=25, preserving_transparency=False
    )
else:
    print("Can't perform operation on background layer")
