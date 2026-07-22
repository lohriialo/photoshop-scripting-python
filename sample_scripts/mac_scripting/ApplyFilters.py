# Apply filters to selections on a sample document (macOS).

from appscript import k

from ps_connect import photoshop, sample_file

ps = photoshop()
ps.display_dialogs.set(k.never)
ps.settings.ruler_units.set(k.pixel_units)
ps.open(sample_file("Layer Comps.psd"))
doc = ps.current_document()

# Activate a paintable layer when possible
try:
    doc.current_layer.set(doc.layer_sets[-1].art_layers[-1])
except Exception:
    pass
active = doc.current_layer()

sel_area = ((0, 212), (300, 212), (300, 300), (0, 300))
ps.select(doc, region=sel_area, combination_type=k.replaced, feather_amount=20, antialiasing=True)
try:
    active.filter(
        using=k.add_noise,
        with_options={k.amount: 15, k.distribution: k.Gaussian, k.monochromatic: False},
    )
except Exception as exc:
    print("Add Noise note:", exc)

sel_area2 = ((120, 20), (210, 20), (210, 110), (120, 110))
ps.select(doc, region=sel_area2, combination_type=k.replaced, feather_amount=25, antialiasing=False)
try:
    active.filter(
        using=k.diffuse_glow,
        with_options={k.graininess: 9, k.glow_amount: 12, k.clear_amount: 15},
    )
except Exception as exc:
    print("Diffuse Glow note:", exc)

try:
    doc.deselect()
except Exception:
    pass
print("Filter demo finished")
