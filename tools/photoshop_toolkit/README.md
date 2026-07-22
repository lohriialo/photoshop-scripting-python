# Photoshop Toolkit

A production-oriented desktop utility for everyday Photoshop automation on **Windows**.

![Status](https://img.shields.io/badge/platform-Windows-0078D6?style=flat-square)
![UI](https://img.shields.io/badge/UI-PySide6-41CD52?style=flat-square)

## Tools

| Tool | What it does | Why (community) |
|------|----------------|-----------------|
| **Batch Resize** | Resize a folder (aspect lock, resample) | Delivery sizes / social |
| **Batch Export** | PSD/TIFF → JPEG or PNG | Client handoff |
| **Layer Comps** | Export each layer comp | Design variants |
| **Run Actions** | Actions-panel macro on a folder | Reuse recorded workflows |
| **Export Layers** | Each art layer → PNG/JPEG | Top forum ask (“layers to files”) |
| **Watermark** | Text stamp on a folder | Proofs / portfolio |
| **Convert sRGB** | Profile → sRGB + export | “Wrong colors in browser” |
| **Canvas Border** | Equal padding around canvas | Mockups / safe margins |
| **Text Replace** | Find/replace text layers | Templates / localization |

## Requirements

- Windows + Adobe Photoshop
- Python 3.9+
- `pip install -e ".[windows,gui]"` from the repo root

## Launch

```bash
# from repo root
pip install -e ".[windows,gui]"
python -m tools.photoshop_toolkit

# or after install
photoshop-toolkit
```

## Notes

- Photoshop should preferably already be running (same elevation as Python).
- Long jobs run on a background thread; use **Cancel** to stop after the current file.
- For headless/scripted pipelines, prefer the CLI recipes under [`recipes/`](../../recipes/).

## Legacy UI

The older single-purpose PyQt5 resizer remains in [`../gui_tool_example/`](../gui_tool_example/) for reference.
