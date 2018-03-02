# Hello World!
from win32com.client import Dispatch

app = Dispatch("Photoshop.Application")

psTextLayer = 2  # from enum PsLayerKind
docRef = app.Documents.Add(320, 240)
layerRef = docRef.ArtLayers.Add()
layerRef.Kind = psTextLayer
textItem = layerRef.TextItem
textItem.Contents = "HELLO WORLD!"
textItem.Position = (120, 120)
