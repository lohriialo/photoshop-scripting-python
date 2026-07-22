# Photoshop COM object reference (makepy)

This folder holds **generated** Python files that describe Photoshop’s COM scripting library (classes, methods, and constants such as `psTextLayer`).

They were produced with **makepy** from [pywin32](https://github.com/mhammond/pywin32) against Photoshop’s type library (`ScriptingSupport.8li`). Example header:

```text
# Created by makepy.py version 0.5.01
# From type library 'ScriptingSupport.8li'
'Adobe Photoshop 2021 Object Library'
```

| File | Photoshop version (approx.) |
|------|-----------------------------|
| `photoshop_CC_2018.py` | CC 2018 |
| `photoshop_CC_2019.py` | CC 2019 |
| `photoshop_2020.py` | 2020 |
| `photoshop_2021.py` | 2021 |

These dumps are large and mostly for **browsing names and enum numbers**. Day-to-day scripts usually only need a few constants—prefer `photoshop_scripting.constants` or copy values from the `class constants:` section of a dump.

**Windows only.** makepy and Photoshop COM type libraries are a Windows workflow.

---

## What you need

1. **Windows**
2. **Adobe Photoshop** installed (the version you want a reference for)
3. **Python 3** with **pywin32**:

   ```bash
   pip install pywin32
   ```

4. Optional: a place to save the output (this `api_reference/` folder)

---

## Find Photoshop’s type library

makepy reads the same type library COM uses. The file is usually:

```text
ScriptingSupport.8li
```

Search under your Photoshop install, for example:

```text
C:\Program Files\Adobe\Adobe Photoshop 2024\
C:\Program Files\Adobe\Adobe Photoshop 2025\
```

PowerShell:

```powershell
Get-ChildItem "C:\Program Files\Adobe" -Filter "ScriptingSupport.8li" -Recurse -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty FullName
```

If that file is missing, repair/reinstall Photoshop, or pick the type library from the makepy GUI list (step below) after Photoshop has been launched at least once so it registers with COM.

---

## Method A — Interactive makepy (easiest)

1. Open a **Command Prompt** or PowerShell.
2. Start the COM browser / makepy UI:

   ```bash
   python -m win32com.client.makepy
   ```

   If that fails, try:

   ```bash
   python -c "from win32com.client import makepy; makepy.main()"
   ```

3. In the list of type libraries, find an entry like:
   - **Adobe Photoshop XX Object Library**, or  
   - a name that mentions **Photoshop** / **ScriptingSupport**
4. Select it and confirm.
5. makepy generates a module under your pywin32 `gen_py` cache (not always into this repo). Typical location:

   ```text
   %LOCALAPPDATA%\Temp\gen_py\
   ```

   or next to your Python install under `Lib\site-packages\win32com\gen_py\`.

6. Copy the generated `.py` into this folder and rename it clearly, e.g.:

   ```text
   api_reference/photoshop_2024.py
   ```

---

## Method B — Command line from `ScriptingSupport.8li`

Useful when you know the exact type library path and want a predictable output file.

### 1. Locate `makepy.py`

```powershell
python -c "import win32com.client.makepy as m, inspect; print(inspect.getfile(m))"
```

Example path:

```text
...\site-packages\win32com\client\makepy.py
```

### 2. Run makepy on the type library

```powershell
$typelib = "C:\Program Files\Adobe\Adobe Photoshop 2024\ScriptingSupport.8li"
$out     = "C:\path\to\photoshop-scripting-python\api_reference\photoshop_2024.py"

python -m win32com.client.makepy -o $out $typelib
```

If `-o` is not accepted on your pywin32 version, run:

```powershell
python -m win32com.client.makepy $typelib
```

…then copy the new module from `gen_py` into `api_reference/` as above.

### 3. Check the file

Open the top of the generated file. You should see:

- `Created by makepy.py`
- `From type library 'ScriptingSupport.8li'` (or similar)
- A title like `Adobe Photoshop 20XX Object Library`
- A large `class constants:` block with `ps…` names

---

## Method C — EnsureDispatch (generate while coding)

At runtime, early-binding wrappers can be generated when you first use Photoshop:

```python
from win32com.client import gencache

# May create gen_py modules the first time it runs
app = gencache.EnsureDispatch("Photoshop.Application")
print(app.Name, app.Version)
```

That still writes into **gen_py**, not automatically into this repo. Copy into `api_reference/` only if you want a checked-in snapshot for a specific Photoshop version.

---

## Using a generated reference

### Browse constants

```python
# After placing the file on PYTHONPATH or importing from this folder:
from api_reference import photoshop_2021 as ps  # if packaged
# or open photoshop_2021.py and search for:
#   class constants:
#       psTextLayer = 2
```

Many samples in this project still document enums inline:

```python
psTextLayer = 2  # from enum PsLayerKind
```

Those numbers come from the same type library makepy dumps.

### Prefer small helpers for real scripts

```python
from photoshop_scripting.constants import LayerKind, Units, DialogModes
```

Only dig through full makepy dumps when you need an obscure constant or class name.

---

## Naming and versioning tips

- Name files by Photoshop year: `photoshop_2024.py`, `photoshop_2025.py`.
- Regenerate when you upgrade major Photoshop versions if you rely on new APIs.
- Do not hand-edit generated files; regenerate and replace.
- Committing multi‑MB dumps is optional—document the makepy steps so others can build their own.

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| No Photoshop entry in makepy list | Launch Photoshop once, then retry; confirm `ScriptingSupport.8li` exists |
| `makepy` module not found | `pip install pywin32`; use the same Python you install packages into |
| Permission error reading `.8li` | Run the shell as a normal user who can read `Program Files\Adobe\...` |
| Generated file is huge | Expected—type libraries expand to lots of Python stubs |
| Constants differ from an older dump | Normal across Photoshop versions; regenerate for *your* install |

---

## Related docs in this repo

- [Windows backends (`win32com` vs `comtypes`)](../docs/backends.md)
- [Main README](../README.md)
- [C# interop DLLs from the same type library](../interop%20assemblies/README.md) (`tlbimp` instead of makepy)

---

## Quick checklist

1. Install Photoshop + `pip install pywin32` on Windows.  
2. Find `ScriptingSupport.8li` or the “Adobe Photoshop Object Library” in makepy.  
3. Run `python -m win32com.client.makepy` (GUI or CLI).  
4. Copy the generated module into `api_reference/photoshop_YEAR.py`.  
5. Use `class constants` for enum values; keep day-to-day code on small helpers and samples.
