from win32com.client import Dispatch, GetActiveObject, GetObject
# Start up Photoshop application
# app = Dispatch('Photoshop.Application')
# Or get Reference to already running Photoshop application instance
# app = GetObject(Class="Photoshop.Application")
app = GetActiveObject("Photoshop.Application")

# app.CurrentTool = 'cropTool'
print(app.CurrentTool)