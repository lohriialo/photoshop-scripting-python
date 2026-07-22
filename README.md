# Photoshop Scripting Automation

<p align="center">
  <img src="https://i.imgur.com/8wOWcPX.png" alt="Photoshop Python" width="520"/>
</p>

<p align="center">
  <strong>Control Adobe Photoshop with Python</strong> — examples, helpers,<br/>
  ready-made batch recipes, and a simple desktop toolkit.
</p>

<p align="center">
  <a href="https://github.com/lohriialo/photoshop-scripting-python/stargazers"><img src="https://img.shields.io/github/stars/lohriialo/photoshop-scripting-python?style=for-the-badge&logo=github&color=yellow" alt="GitHub stars"/></a>
  <a href="https://github.com/lohriialo/photoshop-scripting-python/network/members"><img src="https://img.shields.io/github/forks/lohriialo/photoshop-scripting-python?style=for-the-badge&logo=github&color=blue" alt="GitHub forks"/></a>
  <a href="https://github.com/lohriialo/photoshop-scripting-python/watchers"><img src="https://img.shields.io/github/watchers/lohriialo/photoshop-scripting-python?style=for-the-badge&logo=github&color=green" alt="GitHub watchers"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/license/lohriialo/photoshop-scripting-python?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey?style=flat-square" alt="Platform"/>
  <img src="https://img.shields.io/badge/Photoshop-CC%202018%E2%80%932025-31A8FF?style=flat-square&logo=adobephotoshop&logoColor=white" alt="Photoshop"/>
  <img src="https://img.shields.io/github/last-commit/lohriialo/photoshop-scripting-python?style=flat-square" alt="Last commit"/>
  <img src="https://img.shields.io/github/issues/lohriialo/photoshop-scripting-python?style=flat-square" alt="Issues"/>
  <a href="https://github.com/lohriialo/photoshop-scripting-python"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs welcome"/></a>
</p>

---

Photoshop scripting means **telling Photoshop what to do with code** instead of clicking through the same steps every time. Typical uses:

- Make many versions of one design (different languages, sizes, or colors)
- Export a folder of files overnight
- Check color settings across a library of images
- Swap text in templates, add watermarks, run saved Actions on hundreds of files

Adobe’s own scripting languages are **JavaScript**, **AppleScript** (Mac), and **VBScript** (Windows). This project shows how to do the **same kinds of jobs in Python**—which many people already use for data, tools, and AI coding assistants.

### How Python talks to Photoshop

Think of Photoshop as an app you can remote-control:

1. Your Python script **connects** to a running (or newly launched) Photoshop.
2. It works with a **tree of objects** the same way Adobe’s JavaScript does: the app, open documents, layers, selections, colors, and so on.
3. Almost anything you can do in the menus can be done from that tree—create a document, rename a layer, apply a filter, save a JPEG.

On **Windows**, that connection uses Microsoft’s automation interface (often called COM) via libraries like `pywin32` or `comtypes`. On **macOS**, it uses Apple’s automation bridge via `appscript`. The ideas match; the Python spelling differs slightly by platform (see the sample folders below).

Python is a good fit because it is readable, common in schools and industry, and the language many AI coding tools generate by default. Assistants still need **real, working examples**—not guesswork. This repository is a place to learn from, copy from, and point tools at: small demos, production-style recipes, and helpers so scripts keep working on other people’s machines. If something is unclear or missing, [open an issue](https://github.com/lohriialo/photoshop-scripting-python/issues). Contributions and citations in tools or learning materials are welcome.

### Where to start

| If you want to… | Go here |
|-----------------|--------|
| Learn with short examples | [`sample_scripts/`](sample_scripts/) |
| Reuse connect / path / constant helpers | package `photoshop_scripting` |
| Run common studio batch jobs from the command line | [`recipes/`](recipes/) |
| Use a point-and-click batch app | [`tools/photoshop_toolkit`](tools/photoshop_toolkit/) |
| Compare plugins, cloud APIs, and other options | [docs/landscape.md](docs/landscape.md) |

Also included: Action Manager and JavaScript bridge examples, optional COM type dumps under [`api_reference/`](api_reference/), and MIT-licensed project code.

---

## Quick start

### 1. Clone & install

```bash
git clone https://github.com/lohriialo/photoshop-scripting-python.git
cd photoshop-scripting-python

# Windows
pip install -e ".[windows]"

# macOS
pip install -e ".[macos]"

# Optional desktop toolkit UI
pip install -e ".[windows,gui]"
```

### 2. Hello World (Windows)

Start Photoshop, then:

```bash
python sample_scripts/windows/HelloWorld.py
```

```python
from photoshop_scripting import LayerKind, get_app

app = get_app()
doc = app.Documents.Add(320, 240)
layer = doc.ArtLayers.Add()
layer.Kind = int(LayerKind.TEXT)
layer.TextItem.Contents = "HELLO WORLD!"
layer.TextItem.Position = (120, 120)
```

### 3. Hello World (macOS)

```bash
pip install -e ".[macos]"   # or: pip install appscript
python sample_scripts/mac_scripting/HelloWorld.py
```

```python
from appscript import k
from ps_connect import photoshop  # when running inside sample_scripts/mac_scripting/

ps = photoshop()  # connects to your installed Photoshop app
doc = ps.make(new=k.document, with_properties={k.width: 320, k.height: 240})
layer = doc.make(new=k.art_layer, with_properties={k.kind: k.text_layer})
layer.text_object.contents.set("HELLO WORLD")
layer.text_object.position.set([120, 120])
```

If you have more than one Photoshop installed (for example a release build and a Beta), pick one:

```bash
export PHOTOSHOP_APP_PATH="/Applications/Adobe Photoshop 2026/Adobe Photoshop 2026.app"
```

Scripts under `sample_scripts/windows/` are for **Windows only**. On a Mac they will stop with a short message pointing you to `sample_scripts/mac_scripting/`.

---

## Photoshop Toolkit (GUI)

A dark, production-style multi-tool for everyday batch work:

| Tool | Purpose |
|------|---------|
| **Batch Resize** | Folder resize, aspect lock, resample methods |
| **Batch Export** | PSD/TIFF → JPEG/PNG delivery folders |
| **Layer Comps** | Export each layer comp to its own file |
| **Run Actions** | Apply Actions-panel macros across a folder |
| **Export Layers** | Each art layer → file (top Adobe forum ask) |
| **Watermark** | Copyright text on image folders |
| **Convert sRGB** | Web-safe color for delivery |
| **Canvas Border** | Padding / mockup frames |
| **Text Replace** | Bulk text-layer find/replace in PSD templates |

```bash
pip install -e ".[windows,gui]"
python -m tools.photoshop_toolkit
# or: photoshop-toolkit
```

See [`tools/photoshop_toolkit/README.md`](tools/photoshop_toolkit/README.md).

> The older single-purpose resizer remains in [`tools/gui_tool_example/`](tools/gui_tool_example/) for reference.

---

## Sample scripts

All learning samples live under [`sample_scripts/`](sample_scripts/):

| Path | Platform |
|------|----------|
| [`sample_scripts/windows/`](sample_scripts/windows/) | Windows (Python talks to Photoshop via COM libraries) |
| [`sample_scripts/mac_scripting/`](sample_scripts/mac_scripting/) | macOS (Python talks to Photoshop via appscript) |

Full list by topic: [`sample_scripts/README.md`](sample_scripts/README.md).  
Assets: [`sample_scripts/PS_Samples_Files/`](sample_scripts/PS_Samples_Files/).

---

## Production recipes

```bash
python recipes/batch_export/export_folder.py ./in ./out --format jpg
python recipes/layer_comps/export_comps.py ./out --format png
python recipes/run_action/run_action_folder.py ./in "Molten Lead"
python recipes/jsx_bridge/run_jsx.py
python recipes/smart_object/replace_smart_object.py --content photo.jpg
# Community favorites
python recipes/export_layers/export_layers.py ./out --format png
python recipes/watermark/watermark_folder.py ./in ./out --text "© Studio"
python recipes/convert_srgb/convert_srgb.py ./in ./out
python recipes/canvas_border/add_border.py ./in ./out --padding 40
python recipes/text_replace/replace_text.py ./psds "DRAFT" "FINAL"
```

Full list: [`recipes/README.md`](recipes/README.md).

---

## Helper package (`photoshop_scripting`)

Shared utilities so you do not copy the same “connect to Photoshop / find sample files / turn off dialogs” code into every script:

```python
from photoshop_scripting import (
    get_app,
    sample_path,
    ensure_sample,
    saved_preferences,
    DialogModes,
    LayerKind,
    Units,
)
from photoshop_scripting.actions import do_action, do_javascript
from photoshop_scripting.batch import batch_export_jpeg, export_layer_comps

app = get_app()  # use open Photoshop, or start it if needed
with saved_preferences(app, units=Units.PIXELS, dialogs=DialogModes.NO):
    doc = app.Open(str(ensure_sample("Layer Comps.psd")))
```

| Module | What it is for |
|--------|----------------|
| `photoshop_scripting.app` | Connect to Photoshop on Windows or Mac |
| `photoshop_scripting.constants` | Named numbers for layer types, units, etc. (instead of raw `2`, `3`, …) |
| `photoshop_scripting.paths` | Find sample files inside this repo |
| `photoshop_scripting.prefs` | Temporarily change settings (units, dialogs) and put them back |
| `photoshop_scripting.actions` | Run Actions panel items, low-level “action manager” calls, or JavaScript snippets |
| `photoshop_scripting.batch` | Folder-scale resize, export, layer comps, and similar jobs |

---

## Two Windows libraries: `win32com` and `comtypes`

On Windows, either library can drive Photoshop. Details: **[docs/backends.md](docs/backends.md)**.

**Practical tip:** use **comtypes** when you pass lists of points (for example selections). **win32com** is fine for simple document and layer work and for many Action Manager examples.

---

## Recording hard-to-find commands (ScriptListener)

Some menu commands are awkward to call with the simple object tree above. Adobe’s free **ScriptingListener** plug-in watches what you do in Photoshop and writes a log you can turn into Python (or run as JavaScript from Python).

Step-by-step install and examples: **[docs/action_manager.md](docs/action_manager.md)**

Adobe downloads:

- [Downloadable plug-ins page](https://helpx.adobe.com/photoshop/kb/downloadable-plugins-and-content.html) (ScriptingListener section)
- [Windows package](https://download.adobe.com/pub/adobe/photoshop/win/13.x/Win_Scripting_Plug-In.zip)
- [macOS package](https://download.adobe.com/pub/adobe/photoshop/mac/13.x/Mac_Scripting_Plug-In.dmg)

---

## When to use something else

This project is for **local Photoshop** on your computer. If you need in-app plugins, cloud processing, or reading PSD files *without* opening Photoshop, see **[docs/landscape.md](docs/landscape.md)**.

---

## Optional type dumps

[`api_reference/`](api_reference/) holds generated lists of Photoshop objects for older versions (CC 2018–2021). Handy for browsing names; day to day, prefer `photoshop_scripting.constants` and the samples. How to regenerate with **makepy**: [`api_reference/README.md`](api_reference/README.md).

---

## Project layout

```text
photoshop_scripting/             # Shared Python helpers
sample_scripts/windows/          # Examples for Windows
sample_scripts/mac_scripting/    # Examples for macOS
sample_scripts/PS_Samples_Files/ # Images used by the examples
tools/photoshop_toolkit/         # Desktop batch app
tools/gui_tool_example/          # Older single-purpose resizer
recipes/                         # Command-line workflows
api_reference/                   # Optional object lists
interop assemblies/              # C# interop DLLs + how to build them
docs/                            # Extra guides
```

Building C# interop DLLs: [`interop assemblies/README.md`](interop%20assemblies/README.md).

---

## Resources

- [Photoshop API landing page](https://developer.adobe.com/photoshop)
- [Photoshop scripting docs (Adobe)](https://developer.adobe.com/photoshop/uxp/)
- [Community forum](https://community.adobe.com/t5/photoshop-ecosystem/ct-p/ct-photoshop)
- [JS reference (unofficial HTML)](https://theiviaxx.github.io/photoshop-docs/Photoshop/index.html)
- [Scripting tutorials (YouTube)](https://www.youtube.com/playlist?list=PLUEniN8BpU8-Qmjyv3zyWaNvDYwJOJZ4m)

### Also by the author

- [InDesign Scripting in Python](https://github.com/lohriialo/indesign-scripting-python)
- [Illustrator Scripting in Python](https://github.com/lohriialo/illustrator-scripting-python)

---

## Contributing

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

Please include a short header on new samples:

```python
# script_file_name.py
__author__ = "Your Name"
__version__ = "1.0"
"""What the script does + how to run it."""
```

---

## License

MIT for project code — see [LICENSE](LICENSE).

Adobe sample files, interop DLLs, and type-library dumps may be subject to Adobe terms and are **not** covered by the MIT license.
