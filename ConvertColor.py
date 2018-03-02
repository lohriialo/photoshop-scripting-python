# Convert the foreground color to RGB.

from win32com.client import Dispatch, GetActiveObject, GetObject
# Start up Photoshop application
# app = win32com.client.Dispatch('Photoshop.Application')

# Or get Reference to already running Photoshop application instance
# app = GetObject(Class="Photoshop.Application")
app = GetActiveObject("Photoshop.Application")

# fgColor = app.SolidColor()
fgColor = app.ForegroundColor

fgRGBColor = fgColor.RGB
print("Red:" + str(fgRGBColor.Red) + " Green:" + str(fgRGBColor.Green) + " Blue:" + str(fgRGBColor.Blue))


