# Legacy GUI example (PyQt5 bulk resizer)

> **Prefer the new multi-tool app:** [`tools/photoshop_toolkit/`](../tools/photoshop_toolkit/)  
> Batch resize, export, layer comps, and run actions — PySide6, dark UI, progress + cancel.

This folder keeps the original single-purpose **Bulk Image Resizer** for reference.

![Legacy resizer](https://i.imgur.com/6l3kXw8.png "Photoshop Bulk Image Resizer")

## Requirements

- Python 3.x
- Photoshop (Windows) + `comtypes` / `pywin32`
- `PyQt5`
- Optional: [PyInstaller](https://www.pyinstaller.org/) to freeze an `.exe`

```bash
pip install PyQt5 comtypes
python tools/gui_tool_example/app.py
```

## Designer UI

Convert `.ui` → `.py`:

```bash
pyuic5 resizer_ui.ui -o resizer_ui.py
```

## Package with PyInstaller

```bash
pyinstaller app.py
```
