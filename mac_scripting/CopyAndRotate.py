# Crop and rotate the active document.

from os.path import abspath
from appscript import app, k, mactypes

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance

ps = app(id="com.adobe.Photoshop", terms="sdef")

# This must be an absolute path
fileName = abspath("../PS_Samples_Files/Layer Comps.psd")
ps.open(fileName)
srcDoc = ps.current_document()

strtRulerUnits = ps.settings.ruler_units()
ps.settings.ruler_units.set(k.pixel_units)

# crop a 10 pixel border from the image
bounds = [10, 10, srcDoc.width() - 10, srcDoc.height() - 10]
srcDoc.rotate_canvas(angle=45)
srcDoc.crop(bounds=bounds)

# set ruler back to where it was
ps.settings.ruler_units.set(strtRulerUnits)
