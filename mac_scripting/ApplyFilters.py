# This sample script shows how to apply 3 different filters to
# selections in the open document.

from os.path import abspath
from appscript import app, k, mactypes

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

# We don't want any Photoshop dialogs displayed during automated execution
ps.display_dialogs.set(k.never)

start_rulers = ps.settings.ruler_units.get()
ps.settings.ruler_units.set(k.pixel_units)

# This needs to be an absolute path
fileName = abspath("../PS_Samples_Files/Layer Comps.psd")
ps.open(fileName)
docRef = ps.current_document()

docRef.current_layer.set(docRef.layer_sets[-1].art_layers[-1])
active_layer = docRef.current_layer()

sel_area = ((0, 212), (300, 212), (300, 300), (0, 300))
ps.select(
    docRef, region=sel_area, combination_type=k.replaced, feather_amount=20, antialiasing=True
)

active_layer.filter(
    using=k.add_noise,
    with_options={k.amount: 15, k.distribution: k.Gaussian, k.monochromatic: False}
)

ps.background_color.set({k.class_: k.HSB_color, k.hue: 0, k.saturation: 0, k.brightness: 100})


sel_area2 = ((120, 20), (210, 20), (210, 110), (120, 110))
ps.select(
    docRef, region=sel_area2, combination_type=k.replaced, feather_amount=25, antialiasing=False
)

active_layer.filter(
    using=k.diffuse_glow,
    with_options={k.graininess: 9, k.glow_amount: 12, k.clear_amount: 15}
)

active_layer.filter(
    using=k.glass_filter,
    with_options={
        k.distortion: 7,
        k.smoothness: 3,
        k.scaling: 7,
        k.invert_texture: False,
        k.texture_kind: k.tiny_lens
    }
)

docRef.deselect()

# Set ruler units back the way we found it
ps.settings.ruler_units.set(start_rulers)
