# Open a Photoshop document located in the Photoshop samples folder
# You must first create a File object to pass into the open method.
from comtypes.client import GetActiveObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")


fileName = "C:\Git\PS_Samples_Files\Layer Comps.psd"
docRef = app.Open(fileName)