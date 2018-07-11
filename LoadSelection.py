# This script will demonstrate how to load a selection from a saved alpha channel.

from comtypes.client import GetActiveObject, CreateObject

# Get Reference to already running Photoshop application instance
# using comtypes instead on win32com why? cos win32com has problem accepting 2 dimension array
# http://discourse.techart.online/t/selecting-in-photoshop-using-python-doesnt-work/205
app = GetActiveObject("Photoshop.Application")

# PS constants, see psCC2018.py
psPixels = 1
psExtendSelection = 2  # from enum PsSelectionType

strtRulerUnits = app.Preferences.RulerUnits

if strtRulerUnits is not psPixels:
    app.Preferences.RulerUnits = psPixels
docRef = app.Documents.Add(320, 240)

# Save a rectangular selection area offset by 50 pixels from the image border into an alpha channel
offset = 50
selBounds1 = ((offset, offset), (docRef.Width - offset, offset), (docRef.Width - offset, docRef.Height - offset), (offset, docRef.Height - offset))
docRef.Selection.Select(selBounds1)
selAlpha = docRef.Channels.Add()
docRef.Selection.Store(selAlpha)

# Now create a second wider but less tall selection
selBounds2 = ((0, 75), (docRef.Width, 75), (docRef.Width, 150), (0, 150))
docRef.Selection.Select(selBounds2)

# Load the selection from the just saved alpha channel, combining it with the active selection
docRef.Selection.Load(selAlpha, psExtendSelection, False)

# Set ruler back to where it was
app.Preferences.RulerUnits = strtRulerUnits

