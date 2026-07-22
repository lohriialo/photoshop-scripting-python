# Save document as JPEG (macOS).

import tempfile
from pathlib import Path

from appscript import k

from ps_connect import close_all_documents, photoshop

ps = photoshop()
close_all_documents(ps)
ps.settings.ruler_units.set(k.pixel_units)
doc = ps.make(
    new=k.document,
    with_properties={k.width: 640, k.height: 480, k.resolution: 72, k.name: "SaveAsJPEG"},
)
dest = str(Path(tempfile.gettempdir()) / "ps_sample_saveas_mac.jpg")
try:
    doc.save(in_=dest, as_=k.JPEG)
except Exception:
    doc.save(in_=dest)
print("Saved:", dest)
