# Resize image (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 1000, k.height: 800, k.resolution: 72, k.name: "ResizeImage"},
)
print("Before:", doc.width(), "x", doc.height())
try:
    doc.resize_image(width=500, height=400, resolution=72, resample_method=k.bicubic)
except Exception:
    doc.resize_image(width=500, height=400)
print("After:", doc.width(), "x", doc.height())
