from win32com.client import Dispatch, GetActiveObject, GetObject
# Start up Photoshop application
# app = Dispatch('Photoshop.Application')
# Or get Reference to already running Photoshop application instance
app = GetObject(Class="Photoshop.Application")
# app = GetActiveObject("Photoshop.Application")

docRef = app.ActiveDocument

# runtimeKeyID = app.StringIDToTypeID("kcanDispatchWhileModal")
# runtimeEnumID = app.StringIDToTypeID("enter")
# runtimeEventID = app.StringIDToTypeID("modalStateChanged")
#
# typeState = app.stringIDToTypeID("typeState")
# keyState = app.stringIDToTypeID("keyState")
# keyLevel = app.stringIDToTypeID("keyLevel")
# keyTitle = app.stringIDToTypeID("keyTitle")
#
# importDescriptor = Dispatch('Photoshop.ActionDescriptor')
# importDescriptor.PutInteger(keyLevel, 1)
# importDescriptor.PutEnumerated(keyState, typeState, runtimeEnumID)
# importDescriptor.PutBoolean(runtimeKeyID, True)
# importDescriptor.PutString(keyTitle, "Import Data Set")
#
# app.ExecuteAction(runtimeEventID, importDescriptor)


dialogMode = 3

# idmodalStateChanged = app.StringIDToTypeID("importDataSets")
# importDescriptor = Dispatch('Photoshop.ActionDescriptor')
#
# keyLevel = app.CharIDToTypeID("Lvl ")
# importDescriptor.PutInteger(keyLevel, 1)
#
# keyState = app.CharIDToTypeID("Stte")
# typeState = app.CharIDToTypeID("Stte")
# runtimeEnumID = app.StringIDToTypeID("enter")
#
# importDescriptor.PutEnumerated(keyState, typeState, runtimeEnumID)
#
# runtimeKeyID = app.StringIDToTypeID("kcanDispatchWhileModal")
# importDescriptor.PutBoolean(runtimeKeyID, True)
#
# keyTitle = app.CharIDToTypeID("Ttl ")
# importDescriptor.PutString(keyTitle, "Import Data Set")
#
# app.ExecuteAction(idmodalStateChanged, importDescriptor, dialogMode)


file = "C:\Git\photoshop-scripting-python\PS_Samples_Files\ps_data_sets.txt"

desc = Dispatch('Photoshop.ActionDescriptor')
ref = Dispatch('Photoshop.ActionReference')
ref.putClass(app.StringIDToTypeID("dataSetClass"))
desc.putReference(app.charIDToTypeID("null"), ref)
desc.putPath(app.charIDToTypeID("Usng"), file)
desc.putEnumerated(app.charIDToTypeID("Encd"), app.stringIDToTypeID("dataSetEncoding"), app.stringIDToTypeID("dataSetEncodingAuto"))
desc.putBoolean(app.stringIDToTypeID( "eraseAll" ), True)
desc.putBoolean(app.stringIDToTypeID("useFirstColumn"), True)
app.ExecuteAction(app.stringIDToTypeID( "importDataSets"), desc, dialogMode)