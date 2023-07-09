# Open a Photoshop document located in the Photoshop samples folder
# You must first create a File object to pass into the open method.

from os.path import abspath
from appscript import app, mactypes

# Start up Photoshop application
ps = app(id="com.adobe.Photoshop", terms="sdef")

# Must be an absolute path
fileName = abspath("../PS_Samples_Files/Layer Comps.psd")


# Note: the open command (frustratingly) does not return a value
# but it will always make the opened document the current document
# even if it's already open.
ps.open(fileName)
docRef = ps.current_document()


# There is also the mactype.Alias or mactype.File that you can use classes like so:
# ps.open(mactypes.Alias(fileName))
# ps.open(mactypes.File(fileName))
# These are equivalent to the AppleScript "file" and "alias" classes
