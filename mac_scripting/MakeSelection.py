# Get the active document and make a new selection.

from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

# create new document if no document is opened
# can also use len(ps.documents()) here
if ps.count(None, each=k.document) < 1:
    strtRulerUnits = ps.settings.ruler_units()
    ps.settings.ruler_units.set(k.pixel_units)
    docRef = ps.make(new=k.document, with_properties={
            k.width: 320, k.height: 240, k.resolution: 72, k.mode:k.RGB, k.initial_fill: k.white
        }
    )
    ps.settings.ruler_units.set(strtRulerUnits)
else:
    docRef = ps.current_document

sel_area = ((50, 60), (150, 60), (150, 120), (50, 120))
docRef.select(region=sel_area, combination_type=k.replaced, feather_amount=5.5, antialiasing=False)
