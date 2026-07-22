"""Reusable batch operations for real-world Photoshop automation (Windows COM)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence

from .app import get_app
from .constants import DialogModes, ResampleMethod, SaveOptions
from .prefs import saved_preferences

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".gif", ".psd", ".psb", ".bmp", ".webp"}


def iter_images(folder: Path | str, recursive: bool = False) -> List[Path]:
    root = Path(folder)
    if not root.is_dir():
        raise NotADirectoryError(root)
    pattern_iter: Iterable[Path]
    if recursive:
        pattern_iter = root.rglob("*")
    else:
        pattern_iter = root.iterdir()
    files = [p for p in pattern_iter if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]
    return sorted(files)


def _close(doc: object, save: bool = False) -> None:
    option = SaveOptions.SAVE_CHANGES if save else SaveOptions.DO_NOT_SAVE
    doc.Close(int(option))  # type: ignore[attr-defined]


def batch_resize(
    files: Sequence[Path | str],
    *,
    width: int,
    height: Optional[int] = None,
    resolution: Optional[float] = None,
    resample: int = ResampleMethod.AUTOMATIC,
    save_as_copy_dir: Optional[Path | str] = None,
    overwrite: bool = True,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """
    Resize a list of images.

    If height is None, aspect ratio is preserved from width.
    If save_as_copy_dir is set, saves copies there; otherwise saves in place.
    """
    app = get_app()
    results: List[str] = []
    out_dir = Path(save_as_copy_dir) if save_as_copy_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    total = len(files)
    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                if height and height > 0:
                    doc.ResizeImage(int(width), int(height), resolution, int(resample))
                else:
                    doc_w = float(doc.Width)
                    doc_h = float(doc.Height)
                    new_h = (doc_h / doc_w) * float(width) if doc_w else float(width)
                    doc.ResizeImage(int(width), new_h, resolution, int(resample))

                if out_dir:
                    dest = out_dir / path.name
                    if dest.exists() and not overwrite:
                        results.append(f"skipped:{dest}")
                    else:
                        doc.SaveAs(str(dest))
                        results.append(str(dest))
                else:
                    doc.Save()
                    results.append(str(path))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def batch_export_jpeg(
    files: Sequence[Path | str],
    output_dir: Path | str,
    *,
    quality: int = 10,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """Export files to JPEG in output_dir (quality 0–12)."""
    from comtypes.client import CreateObject

    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                opts = CreateObject("Photoshop.JPEGSaveOptions")
                opts.Quality = max(0, min(12, int(quality)))
                opts.EmbedColorProfile = True
                opts.FormatOptions = 1  # optimized baseline-ish
                dest = out / f"{path.stem}.jpg"
                doc.SaveAs(str(dest), opts, True)
                results.append(str(dest))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def batch_export_png(
    files: Sequence[Path | str],
    output_dir: Path | str,
    *,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """Export files to PNG in output_dir."""
    from comtypes.client import CreateObject

    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                opts = CreateObject("Photoshop.PNGSaveOptions")
                opts.Interlaced = False
                dest = out / f"{path.stem}.png"
                doc.SaveAs(str(dest), opts, True)
                results.append(str(dest))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def export_layer_comps(
    psd_path: Path | str,
    output_dir: Path | str,
    *,
    format: str = "png",
    sleep_between: float = 0.2,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
) -> List[str]:
    """
    Export each layer comp in a PSD to a separate image file.

    format: 'png' or 'jpg'
    """
    from comtypes.client import CreateObject

    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    fmt = format.lower().strip()

    with saved_preferences(app, dialogs=DialogModes.NO):
        doc = app.Open(str(Path(psd_path).resolve()))
        try:
            comps = doc.LayerComps
            count = int(comps.Count)
            for i in range(1, count + 1):
                comp = comps.Item(i)
                name = str(comp.Name)
                if on_progress:
                    on_progress(i, count, name)
                comp.Apply()
                safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in name).strip()
                if fmt in ("jpg", "jpeg"):
                    opts = CreateObject("Photoshop.JPEGSaveOptions")
                    opts.Quality = 10
                    dest = out / f"{safe}.jpg"
                    doc.SaveAs(str(dest), opts, True)
                else:
                    opts = CreateObject("Photoshop.PNGSaveOptions")
                    dest = out / f"{safe}.png"
                    doc.SaveAs(str(dest), opts, True)
                results.append(str(dest))
                if sleep_between:
                    time.sleep(sleep_between)
        finally:
            _close(doc, save=False)
    return results


def run_action_on_files(
    files: Sequence[Path | str],
    action_name: str,
    action_set: str,
    *,
    save: bool = True,
    sleep_between: float = 0.2,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """Open each file, play an Actions-panel action, optionally save."""
    from .actions import do_action

    app = get_app()
    results: List[str] = []
    total = len(files)
    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                do_action(app, action_name, action_set)
                if save:
                    doc.Save()
                results.append(str(path))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


# ---------------------------------------------------------------------------
# Community favorites (export layers, watermark, sRGB, canvas, text replace)
# ---------------------------------------------------------------------------


def _safe_filename(name: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in "-_ ." else "_" for c in str(name)).strip()
    return cleaned or "layer"


def _iter_art_layers(container: object) -> List[object]:
    """Recursively collect ArtLayers under a Document or LayerSet."""
    layers: List[object] = []
    try:
        art = container.ArtLayers  # type: ignore[attr-defined]
        count = int(art.Count)
        for i in range(1, count + 1):
            layers.append(art.Item(i))
    except Exception:  # noqa: BLE001
        pass
    try:
        sets = container.LayerSets  # type: ignore[attr-defined]
        count = int(sets.Count)
        for i in range(1, count + 1):
            layers.extend(_iter_art_layers(sets.Item(i)))
    except Exception:  # noqa: BLE001
        pass
    return layers


def _set_layers_visible(layers: Sequence[object], visible: bool) -> None:
    for layer in layers:
        try:
            layer.Visible = visible  # type: ignore[attr-defined]
        except Exception:  # noqa: BLE001
            pass


def _save_doc_as(doc: object, dest: Path, fmt: str, quality: int = 10) -> None:
    from comtypes.client import CreateObject

    fmt = fmt.lower().strip()
    if fmt in ("jpg", "jpeg"):
        opts = CreateObject("Photoshop.JPEGSaveOptions")
        opts.Quality = max(0, min(12, int(quality)))
        opts.EmbedColorProfile = True
        doc.SaveAs(str(dest), opts, True)  # type: ignore[attr-defined]
    else:
        opts = CreateObject("Photoshop.PNGSaveOptions")
        opts.Interlaced = False
        doc.SaveAs(str(dest), opts, True)  # type: ignore[attr-defined]


def export_layers_to_files(
    psd_path: Path | str,
    output_dir: Path | str,
    *,
    format: str = "png",
    quality: int = 10,
    visible_only: bool = False,
    include_hidden: bool = True,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """
    Export each art layer in a PSD as its own image (classic forum request).

    Isolates one layer at a time (others hidden), preserving document canvas size.
    """
    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    fmt = format.lower().strip()

    with saved_preferences(app, dialogs=DialogModes.NO):
        doc = app.Open(str(Path(psd_path).resolve()))
        try:
            layers = _iter_art_layers(doc)
            if visible_only or not include_hidden:
                layers = [L for L in layers if bool(getattr(L, "Visible", True))]
            # Snapshot original visibility
            original = []
            for L in _iter_art_layers(doc):
                try:
                    original.append((L, bool(L.Visible)))
                except Exception:  # noqa: BLE001
                    original.append((L, True))

            total = len(layers)
            for index, layer in enumerate(layers, start=1):
                if should_cancel and should_cancel():
                    break
                name = str(getattr(layer, "Name", f"layer_{index}"))
                if on_progress:
                    on_progress(index, total, name)
                _set_layers_visible([L for L, _ in original], False)
                try:
                    layer.Visible = True
                except Exception:  # noqa: BLE001
                    continue
                dest = out / f"{_safe_filename(name)}.{ 'jpg' if fmt in ('jpg', 'jpeg') else 'png'}"
                # Avoid collisions
                if dest.exists():
                    dest = out / f"{_safe_filename(name)}_{index}.{dest.suffix.lstrip('.')}"
                _save_doc_as(doc, dest, fmt, quality=quality)
                results.append(str(dest))
                if sleep_between:
                    time.sleep(sleep_between)

            # Restore visibility
            for L, vis in original:
                try:
                    L.Visible = vis
                except Exception:  # noqa: BLE001
                    pass
        finally:
            _close(doc, save=False)
    return results


def batch_watermark_text(
    files: Sequence[Path | str],
    output_dir: Path | str,
    *,
    text: str = "© Copyright",
    opacity: float = 40.0,
    font_size: float = 24.0,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """
    Stamp a text watermark on every image and save PNG copies.

    Opacity is approximate via layer opacity (0–100).
    """
    from .app import create_solid_color
    from .constants import LayerKind

    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                layer = doc.ArtLayers.Add()
                layer.Kind = int(LayerKind.TEXT)
                layer.Opacity = max(1.0, min(100.0, float(opacity)))
                item = layer.TextItem
                item.Contents = text
                item.Size = float(font_size)
                # Bottom-right-ish: position near lower edge
                try:
                    w = float(doc.Width)
                    h = float(doc.Height)
                    item.Position = (max(10.0, w * 0.55), max(20.0, h * 0.92))
                except Exception:  # noqa: BLE001
                    item.Position = (20, 20)
                try:
                    color = create_solid_color(backend="comtypes")
                    color.RGB.Red = 255
                    color.RGB.Green = 255
                    color.RGB.Blue = 255
                    item.Color = color
                except Exception:  # noqa: BLE001
                    pass
                dest = out / f"{path.stem}_wm.png"
                _save_doc_as(doc, dest, "png")
                results.append(str(dest))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def batch_convert_srgb(
    files: Sequence[Path | str],
    output_dir: Path | str,
    *,
    format: str = "jpg",
    quality: int = 10,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """
    Convert each file to sRGB (web/delivery favorite) and export.

    Uses ExtendScript convertProfile for reliable cross-version behavior.
    """
    from .actions import do_javascript

    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)
    fmt = format.lower().strip()
    jsx = r"""
try {
  if (app.documents.length > 0) {
    app.activeDocument.convertProfile(
      "sRGB IEC61966-2.1",
      Intent.RELATIVECOLORIMETRIC,
      true,
      false
    );
  }
} catch (e) {}
"""

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                do_javascript(app, jsx)
                ext = "jpg" if fmt in ("jpg", "jpeg") else "png"
                dest = out / f"{path.stem}_srgb.{ext}"
                _save_doc_as(doc, dest, fmt, quality=quality)
                results.append(str(dest))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def batch_add_canvas_border(
    files: Sequence[Path | str],
    output_dir: Path | str,
    *,
    padding_px: int = 40,
    format: str = "png",
    quality: int = 10,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """
    Expand canvas by padding on all sides (social/mockup prep).

    Uses middle-center anchor (PsAnchorPosition.psMiddleCenter = 5).
    """
    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)
    pad = max(0, int(padding_px))
    fmt = format.lower().strip()
    anchor_middle_center = 5

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                new_w = float(doc.Width) + pad * 2
                new_h = float(doc.Height) + pad * 2
                doc.ResizeCanvas(new_w, new_h, anchor_middle_center)
                ext = "jpg" if fmt in ("jpg", "jpeg") else "png"
                dest = out / f"{path.stem}_border.{ext}"
                _save_doc_as(doc, dest, fmt, quality=quality)
                results.append(str(dest))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def batch_replace_text(
    files: Sequence[Path | str],
    find: str,
    replace: str,
    *,
    save: bool = True,
    output_dir: Optional[Path | str] = None,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """
    Find/replace string in every text layer across a folder of PSDs/images.

    If output_dir is set, saves PSD copies there; else saves in place when save=True.
    """
    from .constants import LayerKind

    app = get_app()
    out = Path(output_dir) if output_dir else None
    if out:
        out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                changed = 0
                for layer in _iter_art_layers(doc):
                    try:
                        if int(layer.Kind) != int(LayerKind.TEXT):
                            continue
                        contents = str(layer.TextItem.Contents)
                        if find in contents:
                            layer.TextItem.Contents = contents.replace(find, replace)
                            changed += 1
                    except Exception:  # noqa: BLE001
                        continue
                if out:
                    dest = out / path.name
                    doc.SaveAs(str(dest))
                    results.append(f"{dest} ({changed} layer(s))")
                else:
                    if save:
                        doc.Save()
                    results.append(f"{path} ({changed} layer(s))")
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def batch_trim_transparent(
    files: Sequence[Path | str],
    output_dir: Path | str,
    *,
    format: str = "png",
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """Trim transparent pixels on each file (sprite/UI asset cleanup)."""
    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)
    # PsTrimType.psTransparentPixels — value is typically 0 or 1 depending on version;
    # JSX bridge is more reliable:
    from .actions import do_javascript

    jsx = r"""
try {
  if (app.documents.length > 0) {
    app.activeDocument.trim(TrimType.TRANSPARENT, true, true, true, true);
  }
} catch (e) {}
"""
    fmt = format.lower().strip()

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                do_javascript(app, jsx)
                ext = "png" if fmt == "png" else "jpg"
                dest = out / f"{path.stem}_trim.{ext}"
                _save_doc_as(doc, dest, fmt)
                results.append(str(dest))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results


def batch_flatten_export(
    files: Sequence[Path | str],
    output_dir: Path | str,
    *,
    format: str = "jpg",
    quality: int = 10,
    sleep_between: float = 0.15,
    on_progress: Optional[Callable[[int, int, str], None]] = None,
    should_cancel: Optional[Callable[[], bool]] = None,
) -> List[str]:
    """Flatten layered files and export (print / client handoff)."""
    app = get_app()
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results: List[str] = []
    total = len(files)
    fmt = format.lower().strip()

    with saved_preferences(app, dialogs=DialogModes.NO):
        for index, file in enumerate(files, start=1):
            if should_cancel and should_cancel():
                break
            path = Path(file)
            if on_progress:
                on_progress(index, total, str(path))
            doc = app.Open(str(path.resolve()))
            try:
                try:
                    doc.Flatten()
                except Exception:  # noqa: BLE001
                    pass
                ext = "jpg" if fmt in ("jpg", "jpeg") else "png"
                dest = out / f"{path.stem}_flat.{ext}"
                _save_doc_as(doc, dest, fmt, quality=quality)
                results.append(str(dest))
            finally:
                _close(doc, save=False)
            if sleep_between:
                time.sleep(sleep_between)
    return results
