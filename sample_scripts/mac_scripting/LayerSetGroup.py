# Create a layer set / group (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 400, k.height: 300, k.resolution: 72, k.name: "LayerSet"},
)
doc.make(new=k.art_layer, with_properties={k.name: "Grouped layer"})
group = doc.make(new=k.layer_set, with_properties={k.name: "My Group"})
print("Layer sets:", len(doc.layer_sets()), "—", group.name())
