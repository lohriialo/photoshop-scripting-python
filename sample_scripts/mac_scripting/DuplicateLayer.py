# Duplicate a layer (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 400, k.height: 300, k.resolution: 72, k.name: "DuplicateLayer"},
)
layer = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer, k.name: "Original"})
layer.text_object.contents.set("Duplicate me")
layer.text_object.position.set([40, 80])
layer.duplicate()
print("Art layers:", len(doc.art_layers()))
