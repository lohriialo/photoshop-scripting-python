# Show/hide layers (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 400, k.height: 300, k.resolution: 72, k.name: "HideShow"},
)
doc.make(new=k.art_layer, with_properties={k.name: "A"})
b = doc.make(new=k.art_layer, with_properties={k.name: "B"})
b.visible.set(False)
print("B visible?", b.visible())
b.visible.set(True)
print("B visible again?", b.visible())
