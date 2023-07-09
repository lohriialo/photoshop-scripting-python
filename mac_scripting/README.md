
# Photoshop Scripting in Python on Mac
Just like `pypiwin32` or `comtypes` is used to script via COM on windows, `appscript` is used to script on Mac. Photoshop scripting is exposed via it's scriptable dictionary. 

[appscript](https://github.com/lohriialo/appscript) is a high-level, user-friendly Apple event bridge that allows you to control Apple's Scriptable macOS applications from Python.

`pip install appscript`

Usage:

```python
from appscript import app

psApp = app(id="com.adobe.Photoshop", terms="sdef")
psApp.open("/absolute/reference/to/file.psd")
```

# Hello World!
```python
from appscript import app, k

ps = app(id="com.adobe.Photoshop", terms="sdef")
doc = ps.make(new=k.document, with_properties={k.width: 320, k.height: 240})
layer_ref = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer})

text_item = layer_ref.text_object
text_item.contents.set("HELLO WORLD")
text_item.position.set([120, 120])
```

# Differences to Windows/COM based scripting.
Anything possible in Windows' COM based scripting is also possible in `appscript`, but I hope the example above shows that the syntax is quite different, and scripts designed for COM do not pass over to the macOS based scripting without tweaking.

Here are a few differences to look out for:

1. The syntax Adobe produces for AppleScript (which `appscript` bases it's terminology on) is just different to what it produces for the COM API.
2. In `appscript`, referencing an object or property does not return the _value_ of that object or property, to do that you must _call_ the reference, or its `get()` method. For example, `ps.documents[1].art_layers[1].name` returns a reference, not a string of the name. To retrieve the actual value of the layer's name, you must call it `ps.documents[1].art_layers[1].name()`. To set the value, you call `...art_layers[1].name.set(value)`
3. When using `comtypes`, you need to manually define constants/enums (e.g. the values for RulerUnits that are used a lot in the examples here). This is not the case with `appscript`, they are parsed from the terminology and stored in a global `k` object.
4. Keyword arguments! As mentioned in the [`appscript` documentation](https://appscript.sourceforge.io/py-appscript/doc_3x/appscript-manual/11_applicationcommands.html), if an argument (a.k.a. a parameter) has a keyword in the AppleScript documentation, it must have that keyword when you call it.
5. AppleScript container indcies start at 1, not 0, and `appscript` inherits this. If you're iterating over a list of appscript objects using `enumerate(...)` or `range(len(...))`, always start at 1, or add 1.

# API Reference
The most up‑to‐date reference for functions, arguments, keywords, and other Photoshop specific information will always be the Scripting Dictionary that comes with your install of Photoshop.

You can access this by opening the Script Editor app, then going to:
`File` > `Open Dictionary...` > `Adobe Photoshop 20XX.app`.

To translate this to `appscript` syntax, you can simply follow the rules specified [here](https://appscript.sourceforge.io/py-appscript/doc_3x/appscript-manual/05_keywordconversion.html):

- Replace `"&"` with `"and"`
- Replace any remaining spaces or symbols with `"_"`
- Any names that are a reserved Python keyword (i.e. `"def"`, `"class"`, `"in"`, `"from"`) have an `"_"` appended to the end

The developer of `appscript` has a tool called [ASDictionary](https://appscript.sourceforge.io/tools.html#asdictionary) which can be useful as a reference.

It's worth having a cursory browse of appscript's [documentation](https://appscript.sourceforge.io/py-appscript/doc_3x/appscript-manual) to get a feel for how to translate AppleScript documentation for use in appscript. It's very verbose though, be warned.

See [Photoshop CC 2018 doc/reference](https://github.com/lohriialo/photoshop-scripting-python/tree/master/mac_scripting/doc_reference) for an appscript specific reference.

Also see Adobe's [AppleScript developer reference](https://github.com/Adobe-CEP/CEP-Resources/blob/master/Documentation/Product%20specific%20Documentation/Photoshop%20Scripting/photoshop-applescript-ref-2020.pdf).
