# Create a rectangular selection via document.select(region=...).

from appscript import k

from ps_connect import photoshop

ps = photoshop()
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
else:
    doc = ps.current_document()

sel_area = ((50, 60), (150, 60), (150, 120), (50, 120))
doc.select(region=sel_area, combination_type=k.replaced, feather_amount=5.5, antialiasing=False)
print("Selection created")
