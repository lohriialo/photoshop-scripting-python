# This script compares the app.foregroundColor
# to the app.backgroundColor.

import win32com.client
# Start up Photoshop application
# app = win32com.client.Dispatch('Photoshop.Application')

# Or get Reference to already running Photoshop application instance
# app = win32com.client.GetObject(Class="Photoshop.Application")
app = win32com.client.GetActiveObject("Photoshop.Application")

if app.ForegroundColor.IsEqual(app.BackgroundColor):
    print("They're Equal")
else:
    print("NOT Equal")
