# Create a 4" × 4" document by setting ruler units to inches first.

from appscript import k

from ps_connect import photoshop

ps = photoshop()

strt_ruler_units = ps.settings.ruler_units()
ps.settings.ruler_units.set(k.inch_units)

doc_ref = ps.make(
    new=k.document,
    with_properties={
        k.width: 4,
        k.height: 4,
        k.resolution: 72,
        k.name: "My New Document",
    },
)

ps.settings.ruler_units.set(strt_ruler_units)
print("Created:", doc_ref.name())
