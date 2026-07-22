# Photoshop automation landscape

This repository focuses on **local desktop automation**: Python drives an installed Photoshop via COM (Windows) or Apple Events (macOS).

## Choose the right tool

| Approach | Best for | Runs Photoshop? |
|----------|----------|-----------------|
| **This repo (COM / appscript)** | Batch jobs, studio pipelines, learning the DOM, Actions | Yes, local |
| **[photoshop-python-api](https://github.com/loonghao/photoshop-python-api)** | Higher-level Windows COM wrapper library | Yes, local |
| **ExtendScript (.jsx)** | Classic scripts inside Photoshop | Yes |
| **UXP plugins** | Modern in-app panels & plugins | Yes, in-process |
| **CEP extensions** | Legacy HTML panels | Yes, in-process |
| **JSX bridge from Python** (`DoJavaScript`) | Reuse existing JSX from Python | Yes — see `recipes/jsx_bridge/` |
| **[Adobe Photoshop API](https://developer.adobe.com/photoshop/api/)** (REST) | Cloud, scale, no desktop install | Cloud |
| **[psd-tools](https://github.com/psd-tools/psd-tools)** / **[PhotoshopAPI](https://github.com/EmberLightVFX/PhotoshopAPI)** | Read/write PSD without launching the app | No |

## When *not* to use this repo

- You need an **in-app UI plugin** → UXP
- You need to process files on a **server without Photoshop** → psd-tools / PhotoshopAPI / cloud API
- You only need **pixel data science** on rasters → Pillow, OpenCV, etc.
- You want a **fully typed product API** with releases → consider `photoshop-python-api` or build on this repo’s helpers

## Complementary use

Many teams combine tools:

1. **psd-tools** to inspect layer structure in CI  
2. **This repo / COM** to apply Actions and export proofs on a workstation  
3. **Cloud API** for elastic production volume  

## Version notes

COM DOM surface is stable across recent Photoshop majors; edge cases exist around export APIs and new layer types. Test against the Photoshop version your studio actually ships.
