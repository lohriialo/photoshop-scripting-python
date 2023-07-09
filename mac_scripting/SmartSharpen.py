# This script demonstrates how you can use the action manager
# to execute the Smart Sharpen filter.

from os.path import abspath
from appscript import app, k

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

fileName = abspath("../PS_Samples_Files/Layer Comps.psd")
ps.open(fileName)
docRef = ps.current_document()

docRef.current_layer.set(docRef.layer_sets[-1].art_layers[-1])

# While the AppleScript/appscript implementation does not expose an
# equivalent to executeAction, we can still use do_javascript to build
# and pass arguments to do the exact same thing from Python.
def SmartSharpen(amount, radius, noise):
    # Note: I have cleaned up the ScriptListener generated code here
    ps.do_javascript("""
    var s = stringIDToTypeID
    var c = charIDToTypeID
    maindesc = new ActionDescriptor()
    maindesc.putEnumerated(s("presetKind"), s("presetKindType"), s("presetKindCustom"))
    maindesc.putUnitDouble(c("Amnt"), c("#Prc"), arguments[0])
    maindesc.putUnitDouble(c("Rds "), c("#Pxl"), arguments[1])
    maindesc.putUnitDouble(s("noiseReduction"), c("#Prc"), arguments[2])
    maindesc.putEnumerated(c("blur"), s("blurType"), c("GsnB"))
    executeAction(s("smartSharpen"), maindesc, DialogModes.NO)
    """, with_arguments=[amount, radius, noise])

SmartSharpen(300, 2.0, 20)
