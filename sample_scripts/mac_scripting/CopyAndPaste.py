# Copy half the document and paste into a new document (macOS).

from appscript import k

from ps_connect import photoshop

ps = photoshop()
ps.settings.ruler_units.set(k.inch_units)
src = ps.make(
    new=k.document,
    with_properties={
        k.width: 7,
        k.height: 5,
        k.resolution: 72,
        k.mode: k.RGB,
        k.initial_fill: k.white,
    },
)
# Selection in pixels
x2 = (src.width() * src.resolution()) / 2
y2 = src.height() * src.resolution()
ps.settings.ruler_units.set(k.pixel_units)
src.select(region=((0, 0), (x2, 0), (x2, y2), (0, y2)), combination_type=k.replaced)
try:
    src.copy()  # or selection.copy
except Exception:
    src.selection.copy()
paste_doc = ps.make(
    new=k.document,
    with_properties={k.width: x2, k.height: y2, k.resolution: src.resolution(), k.name: "Paste Target"},
)
try:
    paste_doc.paste()
except Exception:
    ps.paste()
print("Pasted into new document")
