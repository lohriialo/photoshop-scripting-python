# Generating Photoshop Interop DLLs (C# / .NET)

The `.dll` files in this folder (`Interop.Photoshop.*.dll`) are **.NET interop assemblies**. They let **C# / VB.NET** code call Photoshop’s COM scripting API with IntelliSense and compile-time types.

> **Python users:** you do **not** need these DLLs. Use `comtypes` or `pywin32` (see the main [README](../README.md)). This guide is for .NET only.

Example assemblies checked in here were generated against older Photoshop installs (CC 2019, 2020) and are for reference only. **Generate your own** against the Photoshop version you actually use.

---

## What you will produce

| Input | Tool | Output |
|-------|------|--------|
| Photoshop type library (`.8li` / registered COM type lib) | `tlbimp.exe` or Visual Studio | `Interop.Photoshop.dll` (or similar name) |

---

## Prerequisites

1. **Windows** (COM type libraries are a Windows technology).
2. **Adobe Photoshop** installed (any recent desktop version).
3. One of:
   - **Visual Studio** (Community is fine) with the **“.NET desktop development”** workload, **or**
   - **Windows SDK** / **Build Tools for Visual Studio** (so `tlbimp.exe` is on your machine).

`tlbimp.exe` is the Type Library Importer. Typical install locations:

```text
C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\tlbimp.exe
C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\x64\tlbimp.exe
```

Find it if the path differs:

```powershell
Get-ChildItem -Path "C:\Program Files*" -Filter tlbimp.exe -Recurse -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty FullName
```

---

## Step 1 — Locate Photoshop’s type library

Photoshop ships a type library used for COM scripting. The file is usually named:

```text
ScriptingSupport.8li
```

### 1a. Search under the Photoshop install folder

Open PowerShell:

```powershell
# Adjust the year/version folder to match your install
Get-ChildItem -Path "C:\Program Files\Adobe" -Filter "ScriptingSupport.8li" -Recurse -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty FullName
```

Common results look like:

```text
C:\Program Files\Adobe\Adobe Photoshop 2024\ScriptingSupport.8li
C:\Program Files\Adobe\Adobe Photoshop 2025\ScriptingSupport.8li
C:\Program Files\Adobe\Adobe Photoshop 2021\ScriptingSupport.8li
```

### 1b. If the file is not found

1. Confirm Photoshop launches normally.
2. Repair / reinstall Photoshop (scripting support is part of the standard install).
3. Use the **registered** type library instead of a file path (Step 3b below).

Optional: list registered type libraries that mention Photoshop:

```powershell
Get-ChildItem "Registry::HKEY_CLASSES_ROOT\TypeLib" -ErrorAction SilentlyContinue |
  ForEach-Object {
    $p = $_.PSPath
    Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue |
      Where-Object { $_.GetValue("") -match "Photoshop" } |
      ForEach-Object { $_.GetValue(""); $_.PSPath }
  }
```

---

## Step 2 — Create an output folder

```powershell
New-Item -ItemType Directory -Force -Path "C:\Dev\PhotoshopInterop" | Out-Null
cd C:\Dev\PhotoshopInterop
```

Use any path you prefer; keep it outside Program Files so you don’t need admin rights to write the DLL.

---

## Step 3 — Generate the interop assembly with `tlbimp`

### 3a. Recommended: import from `ScriptingSupport.8li`

In PowerShell, set paths for your machine, then run `tlbimp`:

```powershell
$tlbimp = "C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\tlbimp.exe"
$typelib = "C:\Program Files\Adobe\Adobe Photoshop 2024\ScriptingSupport.8li"
$outDir  = "C:\Dev\PhotoshopInterop"
$outDll  = Join-Path $outDir "Interop.Photoshop.2024.dll"

& $tlbimp $typelib `
  /out:$outDll `
  /namespace:Photoshop `
  /sysarray `
  /machine:X64

# Confirm
Get-Item $outDll | Format-List FullName, Length, LastWriteTime
```

**Flags explained:**

| Flag | Purpose |
|------|---------|
| `/out:` | Output DLL path and file name |
| `/namespace:Photoshop` | .NET namespace for generated types (pick any clear name) |
| `/sysarray` | Import SAFEARRAYs as `System.Array` (usually what you want) |
| `/machine:X64` | Match 64-bit Photoshop (default Photoshop installs are 64-bit) |

If `tlbimp` complains about the path, wrap the type library path in quotes (already done via the variable).

### 3b. Alternative: import by ProgID / registered library

If you cannot point at the `.8li` file but Photoshop is installed and registered:

```powershell
# Some environments accept the type library name registered with COM
& $tlbimp "Adobe Photoshop Type Library" /out:$outDll /namespace:Photoshop /sysarray /machine:X64
```

If that fails, stick to the explicit `ScriptingSupport.8li` path from Step 1.

### 3c. Useful optional flags

```powershell
& $tlbimp $typelib `
  /out:$outDll `
  /namespace:Photoshop `
  /sysarray `
  /machine:X64 `
  /verbose `
  /strictref
```

- `/verbose` — print more detail while generating  
- `/strictref` — stricter reference resolution (can help or cause extra errors depending on SDK version)

---

## Step 4 — Use the DLL in a C# project

### Option A — Visual Studio (Reference Manager)

1. Create or open a **C#** project (e.g. Console App, .NET Framework 4.x or SDK-style that can reference COM interop).
2. Right-click the project → **Add** → **Project Reference…** / **Add Reference…**.
3. **Browse** → select your generated `Interop.Photoshop.2024.dll`.
4. In project properties, if present:
   - **Embed Interop Types** = `True` is often convenient (no need to ship the interop DLL separately), **or**
   - `False` if you prefer to deploy the DLL next to your `.exe`.

### Option B — Visual Studio “COM” tab (no manual tlbimp)

You can skip the command line entirely:

1. **Add Reference…** → **COM** tab.
2. Find **Adobe Photoshop Type Library** (wording varies by version).
3. Check it → **OK**.

Visual Studio runs the equivalent of `tlbimp` for you and adds a reference (often named like `Interop.Photoshop`).

### Option C — `csc` / command-line compile

```powershell
csc /r:Interop.Photoshop.2024.dll Program.cs
```

### Minimal C# smoke test

```csharp
using System;
using Photoshop; // namespace you passed to /namespace:

class Program
{
    static void Main()
    {
        // ProgID for the running / installed Photoshop application
        Type t = Type.GetTypeFromProgID("Photoshop.Application");
        dynamic app = Activator.CreateInstance(t);

        // Or, with a strongly typed interop assembly (names may vary by PS version):
        // Application app = new Application();

        Console.WriteLine(app.Name);
        Console.WriteLine(app.Version);
    }
}
```

> Exact interface names (`Application`, `Document`, …) come from the generated assembly. Browse the DLL in Visual Studio’s **Object Browser** if IntelliSense does not show what you expect.

---

## Step 5 — Verify the assembly

```powershell
# File exists and is non-trivial size
Get-Item "C:\Dev\PhotoshopInterop\Interop.Photoshop.2024.dll"

# Optional: list public types with PowerShell + Reflection
Add-Type -Path "C:\Dev\PhotoshopInterop\Interop.Photoshop.2024.dll"
[AppDomain]::CurrentDomain.GetAssemblies() |
  Where-Object { $_.GetName().Name -like "*Photoshop*" } |
  ForEach-Object { $_.GetExportedTypes() | Select-Object -First 20 FullName }
```

Or in Visual Studio: **View → Object Browser** → select the interop reference → expand namespaces.

---

## Naming convention (recommended)

Include the Photoshop major version in the file name so studio machines don’t mix DLLs:

```text
Interop.Photoshop.CC2019.dll
Interop.Photoshop.2020.dll
Interop.Photoshop.2024.dll
Interop.Photoshop.2025.dll
```

Regenerate when you upgrade Photoshop major versions if COM members you rely on change.

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| `tlbimp` not found | Install Visual Studio **.NET desktop development** workload or Windows SDK; re-run the search command in Prerequisites. |
| `ScriptingSupport.8li` not found | Search under `C:\Program Files\Adobe`; repair Photoshop install. |
| Access denied reading `.8li` | Run PowerShell **as the same user** that can run Photoshop; avoid copying from a locked install dir without permissions. |
| 32-bit vs 64-bit errors | Use `/machine:X64` and a **64-bit** project platform; Photoshop is 64-bit. |
| “Application is busy” / COM errors at runtime | Start Photoshop first; run your app at the **same elevation** (both admin or both not). |
| Types missing / wrong members | Regenerate against **your** Photoshop’s type library; don’t reuse an old DLL from this repo for a newer PS. |
| .NET Core / .NET 5+ COM | Prefer **COMReference** in the `.csproj` or generate interop and enable `EmbedInteropTypes`. COM works, but project setup differs from classic .NET Framework. |

### Example `COMReference` in an SDK-style `.csproj`

If you know the type library GUID/version from OLE/Registry, Visual Studio can embed:

```xml
<ItemGroup>
  <COMReference Include="Photoshop">
    <WrapperTool>tlbimp</WrapperTool>
    <EmbedInteropTypes>true</EmbedInteropTypes>
    <!-- GUID / version values are machine- and PS-version-specific -->
  </COMReference>
</ItemGroup>
```

Browsing via **Add Reference → COM** is easier than hand-writing the GUID.

---

## How this relates to the Python samples in this repo

| Language | How you talk to Photoshop COM |
|----------|-------------------------------|
| **Python** | `comtypes` / `pywin32` — dynamic COM, no Interop DLL |
| **C# / VB.NET** | Interop assembly from `tlbimp` or VS COM reference |

Python’s `api_reference/*.py` files are a different artifact (generated by `makepy` / similar), not Interop DLLs.

---

## Quick copy-paste checklist

1. Install Photoshop + Visual Studio (or Windows SDK).  
2. Find `ScriptingSupport.8li` under `C:\Program Files\Adobe\Adobe Photoshop <year>\`.  
3. Locate `tlbimp.exe`.  
4. Run `tlbimp` with `/out`, `/namespace:Photoshop`, `/sysarray`, `/machine:X64`.  
5. Add the DLL as a reference in your C# project (or use **Add Reference → COM**).  
6. Create `Photoshop.Application` and call DOM methods.  
7. Regenerate when you change major Photoshop versions.

---

## Official Microsoft background (optional reading)

Microsoft’s general documentation for the Type Library Importer (concepts only; the steps above are Photoshop-specific):

- [Generate interop assemblies from type libraries](https://learn.microsoft.com/en-us/dotnet/framework/interop/how-to-generate-interop-assemblies-from-type-libraries)  
- [`Tlbimp.exe` reference](https://learn.microsoft.com/en-us/dotnet/framework/tools/tlbimp-exe-type-library-importer)
