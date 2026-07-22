# Fill the current selection with an RGB colour (non-background layer).

from appscript import k

from ps_connect import photoshop

ps = photoshop()
strt = ps.settings.ruler_units()
ps.settings.ruler_units.set(k.pixel_units)

if len(ps.documents()) < 1:
    doc = ps.make(
        new=k.document,
        with_properties={
            k.width: 320,
            k.height: 240,
            k.resolution: 72,
            k.mode: k.RGB,
            k.initial_fill: k.white,
        },
    )
    doc.make(new=k.art_layer)
else:
    doc = ps.current_document()
    if doc.current_layer.background_layer():
        doc.make(new=k.art_layer)

# Select a region then fill
doc.select(
    region=((20, 20), (300, 20), (300, 220), (20, 220)),
    combination_type=k.replaced,
    feather_amount=0,
    antialiasing=False,
)
fillcolor = {k.class_: k.RGB_color_, k.red: 255, k.green: 0, k.blue: 0}
doc.selection.fill(
    with_contents=fillcolor, blend_mode=k.normal, opacity=25, preserving_transparency=False
)
ps.settings.ruler_units.set(strt)
print("Filled selection with red @ 25% opacity")
