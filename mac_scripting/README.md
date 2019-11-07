
# Photoshop Scripting in Python on Mac
Just like `pypiwin32` or `comtypes` is used to script via COM on windows, `appscript` is used to script on Mac. Photoshop scripting is exposed via it's scriptable dictionary. 

[Appscript](https://github.com/lohriialo/appscript) is a high-level, user-friendly Apple event bridge that allows you to control Apple's Scriptable Mac OS X applications from Python.

`pip install appscript`

Usage:

```python
from appscript import *

psApp = app('/Applications/Adobe Photoshop CC 2018/Adobe Photoshop CC 2018.app')
psApp.open(mactypes.Alias(file_name))
```
See [Photoshop CC 2018 doc/reference](https://github.com/lohriialo/photoshop-scripting-python/tree/master/mac_scripting/doc_reference) for more details

# Note: 
I've not been able to explore more and write example scripts for Mac, would appreciate if someone wants to contribute few sample scripts for Mac using `appscript`
