# Link two layers so they move/transform together.

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

a = doc.make(new=k.art_layer, with_properties={k.name: "A"})
b = doc.make(new=k.art_layer, with_properties={k.name: "B"})
try:
    a.link(with_=b)
except Exception:
    try:
        a.linked_layers.set([b])
    except Exception as exc:
        print("link note:", exc)
print("Created layers to link:", a.name(), b.name())
