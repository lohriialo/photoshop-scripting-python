# Store selection to a channel and load/combine selections (macOS).

from appscript import k

from ps_connect import photoshop

ps = photoshop()
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(new=k.document, with_properties={k.width: 320, k.height: 240})

offset = 50
doc.select(
    region=(
        (offset, offset),
        (320 - offset, offset),
        (320 - offset, 240 - offset),
        (offset, 240 - offset),
    )
)
# Channel store/load terminology varies; try common form
try:
    ch = doc.make(new=k.channel)
    doc.selection.store(channel=ch)
    doc.select(region=((0, 75), (320, 75), (320, 150), (0, 150)))
    doc.selection.load(from_=ch, combination_type=k.extended, inverted=False)
    print("Stored and reloaded selection via channel")
except Exception as exc:
    print("Channel store/load note:", exc)
