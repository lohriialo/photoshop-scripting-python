# Flatten document (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 400, k.height: 300, k.resolution: 72, k.name: "Flatten"},
)
doc.make(new=k.art_layer, with_properties={k.name: "Layer 1"})
doc.make(new=k.art_layer, with_properties={k.name: "Layer 2"})
print("Before:", len(doc.art_layers()))
doc.flatten()
print("After flatten — art layers:", len(doc.art_layers()))
