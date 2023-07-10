# This script demonstrates how you can use the action manager
# to execute the Emboss filter.
# Inorder to find all the IDs, see https://helpx.adobe.com/photoshop/kb/downloadable-plugins-and-content.html#ScriptingListenerplugin
# This blog here exlains what a script listener is http://blogs.adobe.com/crawlspace/2006/05/installing_and_1.html

from os.path import abspath
from appscript import app, k, mactypes

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

fileName = abspath("../PS_Samples_Files/Layer Comps.psd")
ps.open(fileName)
docRef = ps.current_document()

docRef.current_layer.set(docRef.layer_sets[-1].art_layers[-1])

# Unfortunately, since there is no way to send raw Photoshop actions
# via AppleScript, we must use JavaScript for this
# Note: ScriptListener generated code looks awful, but you can tidy it up quite a lot ;)
def emboss(angle, height, amount):
    ps.do_javascript("""
    var desc = new ActionDescriptor()
    var c = charIDToTypeID
    desc.putInteger(c("Angl"), arguments[0])
    desc.putInteger(c("Hght"), arguments[1])
    desc.putInteger(c("Amnt"), arguments[2])
    executeAction(c("Embs"), desc)
    """, with_arguments=[angle, height, amount])

emboss(120, 10, 100)
