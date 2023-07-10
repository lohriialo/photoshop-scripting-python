# Create a new Photoshop document with diminsions 4 inches by 4 inches.

from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

strtRulerUnits = ps.settings.ruler_units()
ps.settings.ruler_units.set(k.inch_units)

# Create the document
docRef = ps.make(
    new=k.document,
    with_properties={
        k.width: 4, k.height: 4, k.resolution: 72, k.name: "My New Document"
    }
)

# Make sure to set the ruler units prior to creating the document.
ps.settings.ruler_units.set(strtRulerUnits)
