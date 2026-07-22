# Add ruler guides (macOS).
# Uses do_javascript for reliable cross-version guide creation.

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 600, k.height: 400, k.resolution: 72, k.name: "Guides"},
)

# Native appscript guide keywords vary by Photoshop version; JSX is stable.
jsx = """
var d = app.activeDocument;
d.guides.add(Direction.VERTICAL, 100);
d.guides.add(Direction.VERTICAL, 500);
d.guides.add(Direction.HORIZONTAL, 50);
d.guides.add(Direction.HORIZONTAL, 350);
d.guides.length;
"""
count = ps.do_javascript(jsx)
print("Guide count:", count)
