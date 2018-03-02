# This script compares the app.foregroundColor
# to the app.backgroundColor.

from win32com.client import Dispatch, GetActiveObject, GetObject
# Start up Photoshop application
# app = Dispatch('Photoshop.Application')

# Or get Reference to already running Photoshop application instance
# app = GetObject(Class="Photoshop.Application")
app = GetActiveObject("Photoshop.Application")

if app.ForegroundColor.IsEqual(app.BackgroundColor):
    print("They're Equal")
else:
    print("NOT Equal")
