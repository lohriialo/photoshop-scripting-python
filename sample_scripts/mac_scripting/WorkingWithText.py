# Text layer with size, position, and RGB colour (macOS).

from appscript import k

from ps_connect import photoshop

ps = photoshop()

strt_ruler = ps.settings.ruler_units()
strt_type = ps.settings.type_units()
ps.settings.ruler_units.set(k.inch_units)
try:
    ps.settings.type_units.set(k.points_units)
except Exception:
    pass

ps.display_dialogs.set(k.never)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 7, k.height: 5, k.resolution: 72},
)

layer = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer})
text = layer.text_object
text.contents.set("Hello, World!")
text.position.set([0.75, 0.75])
text.size.set(36)
# Colour as RGB record
try:
    text.stroke_color.set({k.class_: k.RGB_color_, k.red: 225, k.green: 0, k.blue: 0})
except Exception:
    try:
        text.color.set({k.class_: k.RGB_color_, k.red: 225, k.green: 0, k.blue: 0})
    except Exception as exc:
        print("color note:", exc)

ps.settings.ruler_units.set(strt_ruler)
try:
    ps.settings.type_units.set(strt_type)
except Exception:
    pass
