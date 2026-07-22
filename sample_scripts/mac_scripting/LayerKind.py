# Create a layer and treat it as text (kind=text_layer).

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

layer = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer})
layer.text_object.contents.set("Text layer via kind")
print("Created text layer:", layer.name())
