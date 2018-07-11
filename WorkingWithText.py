# Create a new art layer and convert it to a text layer.
# Set its contents, size and color.
# from win32com.client import Dispatch, GetActiveObject
from comtypes.client import GetActiveObject, CreateObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

strtRulerUnits = app.Preferences.RulerUnits
strtTypeUnits = app.Preferences.TypeUnits
psInches = 2    # from enum PsUnits
psTypePoints = 5    # from enum PsTypeUnits
app.Preferences.RulerUnits = psInches
app.Preferences.TypeUnits = psTypePoints

# suppress all dialogs
psDisplayNoDialogs = 3 # from enum PsDialogModes
app.displayDialogs = psDisplayNoDialogs

# create a new document
docRef = app.Documents.Add(7, 5, 72)

# create text color properties
textColor = CreateObject("Photoshop.SolidColor")
textColor.RGB.Red = 225
textColor.RGB.Green = 0
textColor.RGB.Blue = 0

# add a new text layer to document and apply the text color
newTextLayer = docRef.ArtLayers.Add()
psTextLayer = 2     # from enum PsLayerKind
newTextLayer.Kind = psTextLayer
newTextLayer.TextItem.Contents = "Hello, World!"
newTextLayer.TextItem.Position = [0.75, 0.75]
newTextLayer.TextItem.Size = 36
newTextLayer.TextItem.Color = textColor

# set the app preference the way it was before the operation
app.Preferences.RulerUnits = strtRulerUnits
app.Preferences.TypeUnits = strtTypeUnits

