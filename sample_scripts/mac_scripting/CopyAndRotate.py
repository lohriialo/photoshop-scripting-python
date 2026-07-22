# Open sample, rotate canvas, crop border (macOS).

from appscript import k

from ps_connect import photoshop, sample_file

ps = photoshop()
ps.open(sample_file("Layer Comps.psd"))
src = ps.current_document()
ps.settings.ruler_units.set(k.pixel_units)
bounds = [10, 10, src.width() - 10, src.height() - 10]
src.rotate_canvas(angle=45)
src.crop(bounds=bounds)
print("Rotated 45° and cropped")
