# Create a new Photoshop document with diminsions 4 inches by 4 inches.
from comtypes.client import GetActiveObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

strtRulerUnits = app.Preferences.RulerUnits
psInches = 2 # from enum PsUnits
app.Preferences.RulerUnits = psInches

# Create the document
docRef = app.Documents.Add(4, 4, 72.0, "My New Document")

# Make sure to set the ruler units prior to creating the document.
app.Preferences.RulerUnits = strtRulerUnits