# Crop document (macOS).

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 800, k.height: 600, k.resolution: 72, k.name: "Crop"},
)
print("Before:", doc.width(), "x", doc.height())
doc.crop(bounds=[50, 50, 750, 550])
print("After:", doc.width(), "x", doc.height())
