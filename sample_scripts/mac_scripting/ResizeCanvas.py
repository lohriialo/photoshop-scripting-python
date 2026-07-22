# Resize canvas (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 400, k.height: 300, k.resolution: 72, k.name: "ResizeCanvas"},
)
print("Before:", doc.width(), "x", doc.height())
doc.resize_canvas(width=480, height=380)
print("After:", doc.width(), "x", doc.height())
