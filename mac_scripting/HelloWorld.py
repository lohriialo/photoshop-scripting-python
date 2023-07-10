# Hello World!

from appscript import app, k

ps = app(id="com.adobe.Photoshop", terms="sdef")
doc = ps.make(new=k.document, with_properties={k.width: 320, k.height: 240})
layer_ref = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer})


text_item = layer_ref.text_object
text_item.contents.set("HELLO WORLD")
text_item.position.set([120, 120])
