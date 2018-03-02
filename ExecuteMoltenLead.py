# This script demonstrates how to use the action manager to execute a
# previously defined action liek the default actions that ships with Photoshop
# Or one that you've created yourself. The name of the action comes from
# Photoshop's Actions Palette

from win32com.client import Dispatch, GetActiveObject, GetObject

# Start up Photoshop application
# Or get Reference to already running Photoshop application instance
# app = Dispatch('Photoshop.Application')
app = GetActiveObject("Photoshop.Application")

fileName = "C:\Git\photoshop-scripting-python\PS_Samples_Files\Layer Comps.psd"
docRef = app.Open(fileName)

app.DoAction('Molten Lead', 'Default Actions')

