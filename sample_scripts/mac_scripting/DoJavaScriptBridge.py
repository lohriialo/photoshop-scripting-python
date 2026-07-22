# Run JavaScript from appscript (do javascript).

from ps_connect import photoshop

ps = photoshop()
jsx = (
    'var doc = app.documents.add(300, 200, 72, "JSX Bridge Demo");'
    "var layer = doc.artLayers.add();"
    "layer.kind = LayerKind.TEXT;"
    'layer.textItem.contents = "From JSX via appscript";'
    "doc.name;"
)
try:
    result = ps.do_javascript(jsx)
    print("Result:", result)
except Exception as exc:
    try:
        result = ps.do_script(jsx)
        print("Result:", result)
    except Exception as exc2:
        print("JavaScript bridge note:", exc, "|", exc2)
