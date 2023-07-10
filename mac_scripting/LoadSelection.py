# This script will demonstrate how to load a selection from a saved alpha channel.

from appscript import app, k

ps = app(id="com.adobe.Photoshop", terms="sdef")

strtRulerUnits = ps.settings.ruler_units()
ps.settings.ruler_units.set(k.pixel_units)

docRef = ps.make(new=k.document, with_properties={k.width: 320, k.height: 240})

# To save querying Photoshop for every width/height
# reference, it's faster to just store the values here
width, height = docRef.width(), docRef.height()

# Save a rectangular selection area offset by 50 pixels from the image border into an alpha channel
offset = 50
selBounds1 = ((offset, offset), (width - offset, offset), (width - offset, height - offset), (offset, height - offset))
docRef.select(region=selBounds1)
selAlpha = docRef.make(new=k.channel)
docRef.selection.store(into=selAlpha)

# Now create a second wider but less tall selection
selBounds2 = ((0, 75), (width, 75), (width, 150), (0, 150))
docRef.select(region=selBounds2)

# Load the selection from the just saved alpha channel, combining it with the active selection
docRef.selection.load(from_=selAlpha, combination_type=k.extended, inverting=False)

# Set ruler back to where it was
ps.settings.ruler_units.set(strtRulerUnits)
