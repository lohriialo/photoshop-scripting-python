# Document metrics via appscript.

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={
        k.width: 800,
        k.height: 600,
        k.resolution: 72,
        k.name: "DocumentInfo Demo",
        k.mode: k.RGB,
        k.initial_fill: k.white,
    },
)
print("Name:", doc.name())
print("Width x Height:", doc.width(), "x", doc.height())
print("Resolution:", doc.resolution())
print("Mode:", doc.mode())
