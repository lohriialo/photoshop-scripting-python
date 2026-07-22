# Sample scripts

Short scripts that show how to drive Photoshop from Python.

| Folder | Platform | Bridge |
|--------|----------|--------|
| [`windows/`](windows/) | Windows | COM (`comtypes` / `pywin32`) |
| [`mac_scripting/`](mac_scripting/) | macOS | `appscript` |

Shared assets: [`PS_Samples_Files/`](PS_Samples_Files/)  
Helpers: [`../photoshop_scripting/`](../photoshop_scripting/)

```bash
pip install -e ".[windows]"   # or ".[macos]"
python sample_scripts/windows/HelloWorld.py
python sample_scripts/mac_scripting/HelloWorld.py
```

---

## Samples by topic

### Application & documents

| Sample | APIs |
|--------|------|
| `HelloWorld.py` | New document, text layer, `TextItem` |
| `ApplicationInfo.py` | App name, version, path, preferences |
| `DocumentInfo.py` | Size, resolution, mode, layer/channel counts |
| `NewDocument.py` | Ruler units + `Documents.Add` |
| `OpenDocument.py` | `Application.Open` |
| `SaveAsJPEG.py` / `SaveAsPNG.py` | `SaveAs` + format options |

### Layers & compositing

| Sample | APIs |
|--------|------|
| `ActiveLayer.py` | Active layer / stack indices |
| `LayerKind.py` | `ArtLayer.Kind` |
| `WorkingWithText.py` | Text size, position, `SolidColor` |
| `DuplicateLayer.py` | `Duplicate`, `Translate` |
| `LayerOpacityBlend.py` | `Opacity`, `BlendMode` |
| `HideShowLayers.py` | `Visible` |
| `LinkLayer.py` / `RotateLayer.py` | `Link`, `Rotate` |
| `LayerSetGroup.py` | `LayerSets.Add` |
| `FlattenDocument.py` | `Flatten` |

### Geometry & canvas

| Sample | APIs |
|--------|------|
| `ResizeImage.py` | `ResizeImage` + resample |
| `ResizeCanvas.py` | `ResizeCanvas` + anchor |
| `CropDocument.py` | `Crop` |
| `CopyAndRotate.py` | `RotateCanvas`, `Crop` |
| `TranslateScaleLayer.py` | `Translate` / `Resize` |
| `Guides.py` | Ruler guides |

### Selection, colour & tools

| Sample | APIs |
|--------|------|
| `MakeSelection.py` / `FillSelection.py` | `Selection.Select` / `Fill` |
| `LoadSelection.py` | Channels + store/load selection |
| `SelectionStroke.py` | `SelectBorder`, `Stroke` |
| `CopyAndPaste.py` | Copy pixels into a new document |
| `CompareColors.py` / `ConvertColor.py` | Foreground / background colour |
| `SelectTool.py` | `CurrentTool` |

### Filters, actions & scripting bridges

| Sample | APIs |
|--------|------|
| `ApplyFilters.py` | Layer filter methods + selections |
| `SmartSharpen.py` / `EmbossAction.py` / `ApplyCrystallizeFilterAction.py` | Action Manager / `ExecuteAction` |
| `ExecuteMoltenLead.py` | Named action from the Actions panel |
| `ImportDataSetsAction.py` | Data sets import (Windows) |
| `DoJavaScriptBridge.py` | Run ExtendScript / JSX from Python |
| `ps.py` | Longer Action Manager experiment (Windows) |

---

## Tips

- Top-of-file and inline comments name the DOM objects and typical enum values.
- Run a sample with Photoshop open, change one argument, and run it again.
- Windows COM samples print a clear message on macOS (use `mac_scripting/` there).

Production CLIs: [`../recipes/`](../recipes/) · GUI: [`../tools/photoshop_toolkit/`](../tools/photoshop_toolkit/)
