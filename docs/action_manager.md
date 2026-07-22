# Action Manager + ScriptListener (step by step)

Some Photoshop features are incomplete or awkward on the high-level DOM (`Documents`, `ArtLayers`, …). The **Action Manager** (`ExecuteAction`, descriptors, CharIDs / StringIDs) exposes nearly everything the UI can do.

You almost never hand-write Action Manager code from scratch. You **record** it with Adobe’s free **ScriptingListener** (ScriptListener) plug-in, then translate the log into Python (or keep it as JSX).

---

## What is ScriptListener?

| | |
|--|--|
| **Name** | ScriptingListener plug-in (often called ScriptListener) |
| **Publisher** | Adobe |
| **What it does** | While installed, every actionable UI operation is appended to a log file as **JavaScript (ExtendScript)** Action Manager code |
| **Cost** | Free optional plug-in from Adobe |
| **Needed for** | Discovering the correct `charID` / `stringID` / descriptor tree for filters, exports, and obscure commands |

---

## Download (official Adobe)

Adobe hosts ScriptListener under **Downloadable plug-ins and content**:

**Hub page (always start here — links can move):**  
https://helpx.adobe.com/photoshop/kb/downloadable-plugins-and-content.html

Look for the section **“ScriptingListener plug-in”**.

### Direct package links (from Adobe’s page)

These are the packages Adobe currently documents (ZIP contains the plug-in under a `Utilities` folder, plus scripting docs/samples in some builds):

| Platform | Package |
|----------|---------|
| **Windows** | https://download.adobe.com/pub/adobe/photoshop/win/13.x/Win_Scripting_Plug-In.zip |
| **macOS** | https://download.adobe.com/pub/adobe/photoshop/mac/13.x/Mac_Scripting_Plug-In.dmg |

> If a direct link 404s, use the **hub page** above — Adobe sometimes renames packages but keeps the KB article updated.

Also listed from Adobe’s general plug-ins page:  
https://helpx.adobe.com/photoshop/kb/plugins.html → optional Adobe plug-ins including Script Listener.

---

## Install ScriptListener

### Windows

1. **Quit Photoshop** completely (check the system tray; end any leftover `Photoshop.exe` if needed).
2. Download **Win_Scripting_Plug-In.zip** from the links above.
3. Unzip the archive.
4. Inside, open the **`Utilities`** folder (name can vary slightly by package year).
5. Find the plug-in file, typically:
   - `ScriptingListener.8li`  
   or similar under a versioned folder.
6. **Copy** that plug-in into Photoshop’s **Plug-ins** folder for *your* install, for example:

   ```text
   C:\Program Files\Adobe\Adobe Photoshop 2024\Plug-ins\
   C:\Program Files\Adobe\Adobe Photoshop 2025\Plug-ins\
   ```

   Optional: put it in a subfolder, e.g. `Plug-ins\ScriptingListener\`, so it’s easy to enable/disable by moving the file.

7. Start Photoshop.
8. Confirm the plug-in loaded:
   - **Help → System Info…** → search the text for `ScriptingListener`.
   - Or simply perform a small action (Step “Record” below) and check that a log file appears on the Desktop.

### macOS

1. **Quit Photoshop**.
2. Download **Mac_Scripting_Plug-In.dmg** (or the current Mac package from the hub page).
3. Open the DMG / unzip and locate `ScriptingListener.plugin` (under **Utilities**).
4. Copy it into:

   ```text
   /Applications/Adobe Photoshop 2024/Plug-ins/
   /Applications/Adobe Photoshop 2025/Plug-ins/
   ```

   (Match the year of *your* app bundle.)

5. **Apple Silicon notes** (common gotchas):
   - Clear quarantine if macOS blocks the plug-in:

     ```bash
     sudo xattr -dr com.apple.quarantine "/Applications/Adobe Photoshop 2024/Plug-ins/ScriptingListener.plugin"
     ```

     Adjust the path to your Photoshop version and actual plugin filename.
   - Older ScriptListener builds may need **Photoshop → Get Info → Open using Rosetta** (community reports on M1/M2). Prefer testing System Info after launch.
6. Start Photoshop and verify via **Help → System Info** or a Desktop log file.

### Enable / disable without uninstalling

ScriptListener logs **everything** actionable and can slow you down or flood the log. When you’re done recording:

- **Quit Photoshop**, move the plug-in **out** of `Plug-ins` (e.g. to `Plug-ins (Disabled)`), restart Photoshop.

Or keep two shortcuts/scripts that copy the plug-in in/out of the folder.

---

## Where is the log file?

With ScriptListener installed and Photoshop running, operations append to log files on your **Desktop** (classic behavior):

| Platform | Typical log files |
|----------|-------------------|
| **Windows** | `Desktop\ScriptingListenerJS.log` (JavaScript)  
| | sometimes also a VBScript log depending on package/options |
| **macOS** | `~/Desktop/ScriptingListenerJS.log` |

- Logs **append**; they grow large. Delete or rename the file when starting a clean recording session.
- Prefer the **JS** log — it maps cleanly to Python and to `DoJavaScript`.

---

## Record a command (workflow)

1. Install ScriptListener and start Photoshop.
2. **Delete or rename** any existing `ScriptingListenerJS.log` on the Desktop (clean slate).
3. Open a document (or create one) so the command you care about is valid.
4. Perform **only** the UI steps you want to automate  
   e.g. *Filter → Sharpen → Smart Sharpen…* → set values → OK.
5. Open `ScriptingListenerJS.log` in a text editor.
6. Copy the **last** block of code (the newest action is at the bottom).
7. **Disable/remove** ScriptListener when finished recording.

### What the log looks like (JSX)

You’ll see something in this shape (simplified):

```javascript
var idsmartSharpen = stringIDToTypeID( "smartSharpen" );
    var desc = new ActionDescriptor();
    var idpresetKind = stringIDToTypeID( "presetKind" );
    var idpresetKindType = stringIDToTypeID( "presetKindType" );
    var idpresetKindCustom = stringIDToTypeID( "presetKindCustom" );
    desc.putEnumerated( idpresetKind, idpresetKindType, idpresetKindCustom );
    // ... more putDouble / putEnumerated ...
executeAction( idsmartSharpen, desc, DialogModes.NO );
```

That is pure **Action Manager**: type IDs + an `ActionDescriptor` + `executeAction`.

---

## Translate the log into Python

### Option A — Run the JSX as-is from Python (fastest)

Keep the recorded script almost unchanged and execute it via COM:

```python
from photoshop_scripting import get_app
from photoshop_scripting.actions import do_javascript

app = get_app()

jsx = r"""
var idsmartSharpen = stringIDToTypeID("smartSharpen");
var desc = new ActionDescriptor();
// ... paste from ScriptingListenerJS.log ...
executeAction(idsmartSharpen, desc, DialogModes.NO);
"""

do_javascript(app, jsx)
```

Or save the snippet as `my_filter.jsx` and:

```python
from photoshop_scripting.actions import do_javascript_file

do_javascript_file(app, r"C:\path\to\my_filter.jsx")
```

See also: [`recipes/jsx_bridge/run_jsx.py`](../recipes/jsx_bridge/run_jsx.py).

### Option B — Native Python COM (win32com / comtypes)

Map JSX → Python roughly like this:

| ExtendScript (log) | Python (win32com-style) |
|--------------------|-------------------------|
| `stringIDToTypeID("smartSharpen")` | `app.StringIDToTypeID("smartSharpen")` |
| `charIDToTypeID("Amnt")` | `app.CharIDToTypeID("Amnt")` |
| `new ActionDescriptor()` | `Dispatch("Photoshop.ActionDescriptor")` or `action_descriptor()` |
| `new ActionReference()` | `Dispatch("Photoshop.ActionReference")` or `action_reference()` |
| `desc.putEnumerated(...)` | `desc.PutEnumerated(...)` *(COM often uses PascalCase)* |
| `desc.putUnitDouble(...)` | `desc.PutUnitDouble(...)` |
| `desc.putInteger(...)` | `desc.PutInteger(...)` |
| `executeAction(id, desc, DialogModes.NO)` | `app.ExecuteAction(id, desc, 3)` |

Helpers in this repo:

```python
from photoshop_scripting import get_app, DialogModes
from photoshop_scripting.actions import (
    action_descriptor,
    char_id,
    string_id,
    execute,
    do_action,
)

app = get_app(backend="win32com")

desc = action_descriptor()
# fill descriptor from your recording...
execute(app, string_id(app, "smartSharpen"), desc, DialogModes.NO)

# Or play a named action from the Actions panel (no ScriptListener needed):
do_action(app, "Molten Lead", "Default Actions")
```

### Option C — Side-by-side example in this repo

| Sample | How it was derived |
|--------|--------------------|
| [`SmartSharpen.py`](../sample_scripts/windows/SmartSharpen.py) | Action Manager for Smart Sharpen |
| [`EmbossAction.py`](../sample_scripts/windows/EmbossAction.py) | Emboss filter descriptors |
| [`ApplyCrystallizeFilterAction.py`](../sample_scripts/windows/ApplyCrystallizeFilterAction.py) | Crystallize |
| [`ExecuteMoltenLead.py`](../sample_scripts/windows/ExecuteMoltenLead.py) | Named Actions-panel action (`DoAction`) |
| [`ps.py`](../sample_scripts/windows/ps.py) | Longer Action Manager experiment |

Worked **JSX → Python** pattern from Smart Sharpen:

```python
# JSX:  var id = stringIDToTypeID("smartSharpen");
# Py:
id_smart_sharpen = app.StringIDToTypeID("smartSharpen")

# JSX:  var desc = new ActionDescriptor();
from win32com.client import Dispatch
desc = Dispatch("Photoshop.ActionDescriptor")

# JSX:  desc.putUnitDouble(charIDToTypeID("Amnt"), charIDToTypeID("#Prc"), 300);
desc.PutUnitDouble(app.CharIDToTypeID("Amnt"), app.CharIDToTypeID("#Prc"), 300)

# JSX:  executeAction(id, desc, DialogModes.NO);
app.ExecuteAction(id_smart_sharpen, desc)  # or pass dialog mode 3
```

**Note:** `win32com` often exposes methods as `PutInteger` / `putInteger` depending on the wrapper. If one casing fails, try the other or use `comtypes`.

---

## CharID vs StringID

| Kind | Example | Notes |
|------|---------|--------|
| **CharID** | `"Amnt"`, `"Rds "`, `"Embs"` | Always **4 characters** (pad with spaces: `"Rds "`) |
| **StringID** | `"smartSharpen"`, `"noiseReduction"` | Newer, readable names |

ScriptListener emits whichever Photoshop used for that event. Keep them as recorded; don’t “simplify” IDs unless you know they are aliases.

---

## Tips for clean recordings

1. **One intent per log** — wipe the log, do one command, copy the tail.  
2. **Avoid extra clicks** — selecting tools, zooming, etc. also get logged.  
3. **Set dialog values in the UI** before OK so the log contains your parameters.  
4. **Record with `DialogModes.NO` in mind** — the log may still show dialog modes; in automation use `3` / `DialogModes.NO` so batch jobs don’t pop UI.  
5. **Disable ScriptListener** after recording so normal work isn’t logged.  
6. Prefer **StringID**-heavy blocks when both appear — easier to maintain.

---

## COM busy / reliability

Rapid Action Manager calls can raise “application is busy”:

- Short `time.sleep(0.1–0.5)` between heavy steps (see older samples)
- One thread only talking to Photoshop
- Or package the whole sequence as **one JSX** and call `do_javascript` once

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No log file on Desktop | Plug-in not in the correct `Plug-ins` folder; restart PS; check System Info for ScriptingListener |
| Log not updating | You’re editing an old log; delete it and retry; ensure PS has focus and the command is “actionable” |
| Plug-in missing after PS update | Copy ScriptListener into the **new** version’s `Plug-ins` folder |
| macOS won’t load plug-in | `xattr -dr com.apple.quarantine …`; try Rosetta for very old builds |
| Python `ExecuteAction` fails | Compare method casing; ensure ActionDescriptor is created via COM; try running the raw JSX via `do_javascript` first |
| Works in JSX but not Python | Prefer Option A (JSX bridge) for that command; translate later |

---

## Checklist

1. Download ScriptListener from Adobe’s [downloadable plug-ins page](https://helpx.adobe.com/photoshop/kb/downloadable-plugins-and-content.html).  
2. Quit Photoshop → copy plug-in into that version’s `Plug-ins` folder → restart.  
3. Delete Desktop `ScriptingListenerJS.log`.  
4. Perform the UI operation once.  
5. Copy the new JSX block from the log.  
6. Run via `do_javascript` **or** translate to `ActionDescriptor` + `ExecuteAction` in Python.  
7. Remove/disable ScriptListener when done recording.  
8. Compare with `sample_scripts/windows/SmartSharpen.py` / `EmbossAction.py`.

---

## See also

- [`photoshop_scripting/actions.py`](../photoshop_scripting/actions.py) — helpers  
- [`docs/backends.md`](backends.md) — comtypes vs win32com  
- [`recipes/jsx_bridge/`](../recipes/jsx_bridge/) — run JSX from Python  
- Adobe scripting overview: https://developer.adobe.com/photoshop/
