# Save document as PNG (macOS).

import tempfile
from pathlib import Path

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 512, k.height: 512, k.resolution: 72, k.name: "SaveAsPNG"},
)
dest = str(Path(tempfile.gettempdir()) / "ps_sample_saveas_mac.png")
try:
    doc.save(in_=dest, as_=k.PNG)
except Exception:
    doc.save(in_=dest)
print("Saved:", dest)
