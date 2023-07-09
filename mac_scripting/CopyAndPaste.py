# This example makes a creates a selection in the activeDocument, copies the selection,
# to the clipboard, creates a new document of the same dimensions
# and pastes the contents of the clipboard into it.
# It ensures that rulerUnits are set before creating the new document.
# It checks the kind of the layer before making the selection to be
# sure not to copy a text layer.

from appscript import app, k

ps = app(id="com.adobe.Photoshop", terms="sdef")

strtRulerUnits = ps.settings.ruler_units()
ps.settings.ruler_units.set(k.inch_units)

srcDoc = ps.make(
    new=k.document,
    with_properties={k.width: 7, k.height: 5, k.resolution: 72, k.mode: k.RGB, k.initial_fill: k.white}
)

# Make sure the active layer is not a text layer, which cannot be copied to the clipboard
if srcDoc.current_layer.kind() != k.text_layer:
    # Select the left half of the document. Selections are always expressed
    # in pixels regardless of the current ruler unit type, so we're computing
    # the selection corner points based on the inch unit width and height
    # of the document
    x2 = (srcDoc.width() * srcDoc.height()) / 2
    y2 = srcDoc.height() * srcDoc.resolution()

    sel_area = ((0, 0), (x2, 0), (x2, y2), (0, y2))
    srcDoc.select(
        region=sel_area,
        combination_type=k.replaced,
        feather_amount=0,
        antialiasing=False
    )

    # AppleScript implementation of this function
    # can only copy and paste from the current_document
    # and only if it is the frontmost application
    ps.activate()
    ps.copy()

    # The new doc is created
    # need to change ruler units to pixels because x2 and y2 are pixel units.
    ps.settings.ruler_units = k.pixel_units
    pasteDoc = ps.make(
        new=k.document,
        with_properties={
            k.width: x2, k.height: y2, k.resolution: srcDoc.resolution(), k.name: "Paste Target"
        }
    )
    ps.paste()
else:
    print("You cannot copy from a text layer")


ps.settings.ruler_units.set(strtRulerUnits)
