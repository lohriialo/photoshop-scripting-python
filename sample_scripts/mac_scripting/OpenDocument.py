# Open a document from disk (macOS).
# ps.open(absolute_path) — path must be absolute.

from ps_connect import photoshop, sample_file

ps = photoshop()
file_name = sample_file("Layer Comps.psd")

# open does not return the document; it becomes current_document
ps.open(file_name)
doc_ref = ps.current_document()
print("Opened:", doc_ref.name())
