# Rotate the current non-background layer 45°.

from appscript import k

from ps_connect import photoshop

ps = photoshop()
if len(ps.documents()) < 1:
    print("You must have at least one open document to run this script!")
else:
    doc = ps.current_document()
    layer = doc.current_layer()
    if layer.background_layer():
        print("Operation cannot be performed on background layer")
    else:
        layer.rotate(angle=45.0)
        print("Rotated:", layer.name())
