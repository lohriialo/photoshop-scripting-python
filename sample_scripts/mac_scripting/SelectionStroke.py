# Stroke a selection border (macOS).

from appscript import k

from ps_connect import photoshop

ps = photoshop()
ps.display_dialogs.set(k.never)

if len(ps.documents()) < 1:
    ps.settings.ruler_units.set(k.pixel_units)
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
    doc.make(new=k.art_layer)
else:
    doc = ps.current_document()

ps.settings.ruler_units.set(k.pixel_units)
width, height = doc.width(), doc.height()
offset = 10
doc.select(
    region=(
        (offset, offset),
        (width - offset, offset),
        (width - offset, height - offset),
        (offset, height - offset),
    )
)
try:
    doc.select_border(width=5)
except Exception:
    pass

stroke_color = {
    k.class_: k.CMYK_color,
    k.cyan: 20,
    k.magenta: 90,
    k.yellow: 50,
    k.black: 50,
}
try:
    doc.stroke(
        using_color=stroke_color,
        width=2,
        location=k.outside,
        blend_mode=k.vivid_light,
        opacity=75,
        preserving_transparency=True,
    )
    print("Stroked selection")
except Exception as exc:
    print("stroke note:", exc)
