# Switch the current (active) layer between first and last in the stack.

from appscript import k

from ps_connect import photoshop

ps = photoshop()

if len(ps.documents()) < 1:
    doc_ref = ps.make(new=k.document)
else:
    doc_ref = ps.current_document()

# Ensure multiple layers exist
if len(doc_ref.layers()) < 2:
    doc_ref.make(new=k.art_layer)

# appscript collections are 1-based like AppleScript
layers = doc_ref.layers()
last = layers[-1] if not isinstance(layers, list) else layers[-1]
# Prefer indexed access
try:
    last_layer = doc_ref.layers[len(doc_ref.layers())]
    first_layer = doc_ref.layers[1]
except Exception:
    last_layer = doc_ref.art_layers[-1]
    first_layer = doc_ref.art_layers[1]

try:
    current = doc_ref.current_layer()
    if current.name() != last_layer.name():
        doc_ref.current_layer.set(last_layer)
    else:
        doc_ref.current_layer.set(first_layer)
except Exception:
    doc_ref.current_layer.set(last_layer)

print("Active layer:", doc_ref.current_layer.name())
