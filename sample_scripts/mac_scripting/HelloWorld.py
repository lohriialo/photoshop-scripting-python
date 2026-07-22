# Hello World — create a document and a text layer (macOS / appscript).
# Mirrors the classic COM sample: Documents.Add → art layer → text.

from appscript import k

from ps_connect import photoshop

# Application reference (prefers a concrete .app path when several PS installs exist)
ps = photoshop()

# make(new=k.document, with_properties={...}) ≈ Documents.Add
doc = ps.make(new=k.document, with_properties={k.width: 320, k.height: 240})

# Text layer: set kind at creation time (COM often sets Kind after Add)
layer_ref = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer})

# Property access uses .get() / .set() in appscript (not bare assignment)
text_item = layer_ref.text_object
text_item.contents.set("HELLO WORLD")
text_item.position.set([120, 120])
