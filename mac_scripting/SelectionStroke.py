# Create a stroke around the current selection.
# Set the stroke color and width of the new stroke.

from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

# ps.count(None, each=k.documents) also works instead of len() here
if len(ps.documents()) > 0:
    if ps.current_document.current_layer.background_layer() == False:
        strtRulerUnits = ps.settings.ruler_units()
        ps.settings.ruler_units.set(k.pixel_units)

        width, height = ps.current_document.width(), ps.current_document.height()

        selRef = ps.current_document
        offset = 10
        selBounds = (
            (offset, offset),
            (width - offset, offset),
            (width - offset, height - offset),
            (offset, height - offset)
        )

        selRef.select(region=selBounds)
        selRef.select_border(width=5)

        # create text color properties
        strokeColor = {
            k.class_: k.CMYK_color,
            k.cyan: 20,
            k.magenta: 90,
            k.yellow: 50,
            k.black: 50
        }

        # We don't want any Photoshop dialogs displayed during automated execution
        ps.display_dialogs.set(k.never)
        selRef.stroke(
            using_color=strokeColor,
            width=2,
            location=k.outside,
            blend_mode=k.vivid_light,
            opacity=75,
            preserving_transparency=True
        )

        # Set ruler units back the way we found it
        ps.settings.ruler_units.set(strtRulerUnits)
    else:
        print("Operation cannot be performed on background layer")
else:
    print("Create a document with an active selection before running this script!")
