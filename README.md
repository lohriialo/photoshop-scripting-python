# Photoshop Scripting in Python
![](https://i.imgur.com/8wOWcPX.png "Photoshop Python")

Scripting in Photoshop is used to automate repetitive tasks and are often used as a creative tool to streamline tasks that might be too
time consuming to do manually. For example, you could write a script to generate a number of localized
versions of a particular image or to gather information about the various color profiles used by a collection
of images.

# Photoshop COM & DOM
Photoshop can be scripted through COM(Component Object Model). Its DOM(Document Object Model) is the same when accessing it through either its own JavaScript engine or Python or any other scripting language it supports. The Photoshop DOM consists of a hierarchical representation of the Photoshop application, the documents used in it, and the components of the documents. The DOM allows you to programmatically access and manipulate the document and its components. For example, through the DOM, you can create
a new document, add a layer to an existing document, or change the background color of a layer. Most of
the functionality available through the Photoshop user interface is available through the DOM.

# But why Python?
Photoshop scripting officially supports JavaScript, AppleScript & VBScript. However, Scripting in Python is also fairly easy if not easier if you're already comfortable with Python. You may have already heard that Python is gaining in popularity, but did you know it’s now the most popular introductory programming language in U.S. universities? Python is also cross platform just like JavaScript is and lately becoming one of the fastest growing programming language according to StackOverflow [as of 2017](https://stackoverflow.blog/2017/09/06/incredible-growth-python) / [as of 2019](https://insights.stackoverflow.com/survey/2019#key-results)

Python is easy to use, powerful, and versatile, making it a great choice for beginners and experts alike. Python’s readability makes it a great first programming language - it allows you to think like a programmer and not waste time understanding the mysterious syntax that other programming languages can require.

# Getting Started
Python allows you to access COM and it's DOM with the help of a Python extensions like  "pypiwin32" or "comtypes". Install these modules and you're ready to start scripting Photoshop in Python

* `pip install pypiwin32` or `pip install comtypes`

# Hello World!
```python
from win32com.client import Dispatch

app = Dispatch("Photoshop.Application")
doc = app.Documents.Add(320, 240)
layerRef = doc.ArtLayers.Add()

psTextLayer = 2  # from enum PsLayerKind
layerRef.Kind = psTextLayer

textItem = layerRef.TextItem
textItem.Contents = "HELLO WORLD!"
textItem.Position = (120, 120)
```
# How to inspect scripting object properties?
There's not a straight forward way, you need to read the documentation to understand what properties/attributes are available for a scripting object, or possibly a COM browser. For example, I've extracted the Python scripting object reference for Photoshop CC 2018 at [api_reference](https://github.com/lohriialo/photoshop-scripting-python/tree/master/api_reference)

# GUI tool example
See [`gui_tool`](https://github.com/lohriialo/photoshop-scripting-python/tree/master/gui_tool_example) for an example of how you can use Photoshop Scripting to develop your own tool/utilities

# Scripting on Mac?
Yes, scripting on Mac is also possible, see [mac_scripting](https://github.com/lohriialo/photoshop-scripting-python/tree/master/mac_scripting) for more details

# Photoshop Scripting Resources
* [Photoshop Scripting Documentation](https://www.adobe.com/devnet/photoshop/scripting.html)
* [Photoshop Scripting Developer Forum](https://forums.adobe.com/community/photoshop/photoshop_scripting)
* [Photoshop Scripting API Reference](https://www.adobe.com/devnet/photoshop/scripting.html)
* [Photoshop Scripting Tutorials](https://www.youtube.com/playlist?list=PLUEniN8BpU8-Qmjyv3zyWaNvDYwJOJZ4m)

# Also see
* [InDesign Scripting in Python](https://github.com/lohriialo/indesign-scripting-python)
* [Illustrator Scripting in Python](https://github.com/lohriialo/illustrator-scripting-python)

# Contribution
If you've written a useful Photoshop Python script and wants to share with the world, please create a new issue with the file as an attachment to the issue.

When you submit a script, please try to include the following information at the start of your script
```python
# script_file_name.py

# Created: 1st January 2019
__author__ = 'Your Name or Original Author Name'
__version__ = '1.0'

"""
A short description of what the script does
"""

"""
Instructions on how to use the script, if any
"""

```
* Go to  [photoshop-scripting-python/issues/new](https://github.com/lohriialo/photoshop-scripting-python/issues/new)
* Add title  as `Useful Script`
* Drag & drop your .py script file into the description area
* Click `Submit new issue`
