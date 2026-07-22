# Translate a layer (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 500, k.height: 400, k.resolution: 72, k.name: "Transform"},
)
layer = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer})
layer.text_object.contents.set("Move & scale")
layer.text_object.size.set(36)
layer.text_object.position.set([40, 100])
try:
    layer.translate(delta_x=60, delta_y=40)
except Exception:
    try:
        layer.translate(x=60, y=40)
    except Exception as exc:
        print("translate note:", exc)
print("Layer ready:", layer.name())
