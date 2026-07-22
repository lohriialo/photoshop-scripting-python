# Windows backends: `comtypes` vs `win32com`

Photoshop on Windows is automated through **COM**. Two popular Python bridges:

| | **comtypes** | **win32com** (pywin32) |
|--|--------------|------------------------|
| Package | `comtypes` | `pywin32` |
| Arrays / nested tuples | Generally better (e.g. selection coordinates) | Often fails or needs `VARIANT` wrappers |
| Early-bound wrappers | `GetModule` / type libs | `makepy` / `EnsureDispatch` |
| SolidColor / create | `CreateObject(...)` | `Dispatch(...)` |
| Community samples | Growing | Very common in older code |

## Recommendation

1. **Default to `comtypes`** for new samples and tools (this repo’s `get_app()` does that in `auto` mode).
2. Use **win32com** when you are pasting Action Manager code generated against win32com examples, or when you rely on `makepy` wrappers under `api_reference/`.
3. **Do not import both** into the same module unless you know why — it confuses readers and can create two different proxy objects.

## Selection example

This pattern historically fails with raw win32com but works with comtypes:

```python
from photoshop_scripting import get_app
from photoshop_scripting.constants import SelectionType

app = get_app(backend="comtypes")
doc = app.ActiveDocument
area = ((0, 0), (100, 0), (100, 100), (0, 100))
doc.Selection.Select(area, int(SelectionType.REPLACE), 0, False)
```

## Connecting

```python
from photoshop_scripting import get_app

app = get_app()                      # auto backend, prefer running instance
app = get_app(backend="comtypes")
app = get_app(backend="win32com")
app = get_app(prefer_running=False)  # force launch
```

## Elevation gotcha

If Photoshop is running **as Administrator** and your Python process is not (or vice versa), COM attach fails. Run both at the same integrity level.

## macOS

macOS does not use COM. Use **appscript** and the samples under `sample_scripts/mac_scripting/`. Syntax does not port 1:1 — see that folder’s README.
