# Windows vs macOS scripting

| | Windows | macOS |
|--|---------|--------|
| Bridge | COM (`comtypes` / `win32com`) | Apple Events (`appscript`) |
| Samples | `sample_scripts/windows/*.py` | `sample_scripts/mac_scripting/*.py` |
| Helpers | Full `photoshop_scripting` package | `get_app()` returns appscript app; batch/GUI are COM-oriented |
| Enums | Integer constants / `constants.py` | `appscript.k` terminology |
| Indexing | Often 1-based COM collections | 1-based (AppleScript heritage) |

## What ports

- Concepts: documents, layers, text items, open/save, actions
- Studio intent: batch export, resize, run named actions

## What does not port 1:1

- Python call syntax and property get/set (macOS needs `.get()` / `.set()`)
- Action Manager descriptor code (Windows COM samples)
- COM-only toolkit GUI and `photoshop_scripting.batch`

See `sample_scripts/mac_scripting/README.md` for appscript details and keyword conversion rules.
