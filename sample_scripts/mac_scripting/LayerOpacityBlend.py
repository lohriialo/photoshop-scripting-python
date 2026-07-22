# Layer opacity and blend mode (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 400, k.height: 300, k.resolution: 72, k.name: "OpacityBlend"},
)
layer = doc.make(new=k.art_layer, with_properties={k.name: "Soft overlay"})
layer.opacity.set(50)
try:
    layer.blend_mode.set(k.multiply)
except Exception as exc:
    print("blend_mode note:", exc)
print("opacity:", layer.opacity(), "blend:", layer.blend_mode())
