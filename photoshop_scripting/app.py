"""Connect to a local Adobe Photoshop application instance."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, List, Literal, Optional

Backend = Literal["comtypes", "win32com", "auto"]

_PROG_ID = "Photoshop.Application"

# Prefer concrete app bundles when several Photoshop installs share com.adobe.Photoshop
_MAC_APP_CANDIDATES = (
    "/Applications/Adobe Photoshop 2026/Adobe Photoshop 2026.app",
    "/Applications/Adobe Photoshop 2025/Adobe Photoshop 2025.app",
    "/Applications/Adobe Photoshop 2024/Adobe Photoshop 2024.app",
    "/Applications/Adobe Photoshop 2023/Adobe Photoshop 2023.app",
    "/Applications/Adobe Photoshop 2022/Adobe Photoshop 2022.app",
    "/Applications/Adobe Photoshop 2021/Adobe Photoshop 2021.app",
    "/Applications/Adobe Photoshop 2020/Adobe Photoshop 2020.app",
    "/Applications/Adobe Photoshop CC 2019/Adobe Photoshop CC 2019.app",
    "/Applications/Adobe Photoshop CC 2018/Adobe Photoshop CC 2018.app",
)


class PhotoshopNotFoundError(RuntimeError):
    """Raised when Photoshop cannot be started or attached to."""


def require_windows_com() -> None:
    """
    Exit with a clear message when a Windows-COM sample is run on another OS.

    Windows samples under sample_scripts/windows/ use the COM object model
    (Documents.Add, etc.). macOS equivalents live under sample_scripts/mac_scripting/.
    """
    if sys.platform.startswith("win"):
        return
    script = Path(sys.argv[0]).name if sys.argv else "this script"
    mac = script  # same filename under sample_scripts/mac_scripting/ for most samples
    raise SystemExit(
        f"{script} uses Windows COM APIs and cannot run on {sys.platform}.\n"
        f"On macOS use the appscript samples instead, e.g.:\n"
        f"  python sample_scripts/mac_scripting/{mac}\n"
        f"Or: pip install -e '.[macos]'  then use photoshop_scripting.get_app() "
        f"with appscript syntax (see sample_scripts/mac_scripting/README.md)."
    )


def _windows_get_app(backend: Backend, prefer_running: bool) -> Any:
    last_error: Optional[Exception] = None

    def try_comtypes() -> Any:
        from comtypes.client import CreateObject, GetActiveObject

        if prefer_running:
            try:
                return GetActiveObject(_PROG_ID)
            except Exception as exc:  # noqa: BLE001 - COM raises varied types
                nonlocal last_error
                last_error = exc
        return CreateObject(_PROG_ID)

    def try_win32com() -> Any:
        from win32com.client import Dispatch, GetActiveObject

        if prefer_running:
            try:
                return GetActiveObject(_PROG_ID)
            except Exception as exc:  # noqa: BLE001
                nonlocal last_error
                last_error = exc
        return Dispatch(_PROG_ID)

    if backend == "comtypes":
        order = ["comtypes"]
    elif backend == "win32com":
        order = ["win32com"]
    else:
        order = ["comtypes", "win32com"]

    errors: list[str] = []
    for name in order:
        try:
            if name == "comtypes":
                return try_comtypes()
            return try_win32com()
        except ImportError as exc:
            errors.append(f"{name} not installed ({exc})")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")

    hint = (
        "Install extras: pip install 'photoshop-scripting-python[windows]'\n"
        "Ensure Adobe Photoshop is installed. "
        "If it is running as admin, run Python with the same elevation."
    )
    detail = "; ".join(errors)
    if last_error:
        detail = f"{detail}; last attach error: {last_error}"
    raise PhotoshopNotFoundError(f"Could not connect to Photoshop. {detail}\n{hint}")


def _discover_mac_photoshop_apps() -> List[Path]:
    """Return installed Photoshop .app bundles, newest year first."""
    found: List[Path] = []
    seen = set()

    env = os.environ.get("PHOTOSHOP_APP_PATH")
    if env:
        p = Path(env).expanduser()
        if p.exists():
            found.append(p)
            seen.add(p.resolve())

    for raw in _MAC_APP_CANDIDATES:
        p = Path(raw)
        if p.exists():
            key = p.resolve()
            if key not in seen:
                found.append(p)
                seen.add(key)

    apps_dir = Path("/Applications")
    if apps_dir.is_dir():
        # e.g. "Adobe Photoshop 2026", "Adobe Photoshop (Beta)"
        matches = sorted(
            apps_dir.glob("Adobe Photoshop*/Adobe Photoshop*.app"),
            key=lambda p: p.as_posix().lower(),
            reverse=True,
        )
        # Prefer non-Beta stable builds first
        stable = [p for p in matches if "(Beta)" not in p.as_posix()]
        beta = [p for p in matches if "(Beta)" in p.as_posix()]
        for p in stable + beta:
            key = p.resolve()
            if key not in seen and p.exists():
                found.append(p)
                seen.add(key)

    return found


def _mac_get_app() -> Any:
    try:
        from appscript import app
    except ImportError as exc:
        raise PhotoshopNotFoundError(
            "appscript is required on macOS. "
            "Install with: pip install 'photoshop-scripting-python[macos]'"
        ) from exc

    errors: list[str] = []
    for path in _discover_mac_photoshop_apps():
        try:
            return app(str(path), terms="sdef")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: {exc}")

    # Last resort: bundle id (ambiguous when Beta + release both installed)
    try:
        return app(id="com.adobe.Photoshop", terms="sdef")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"bundle id com.adobe.Photoshop: {exc}")

    raise PhotoshopNotFoundError(
        "Could not connect to Photoshop via appscript.\n"
        + "\n".join(errors)
        + "\nSet PHOTOSHOP_APP_PATH to your .app bundle if needed, e.g.\n"
        "  export PHOTOSHOP_APP_PATH='/Applications/Adobe Photoshop 2026/"
        "Adobe Photoshop 2026.app'"
    )


def get_app(
    *,
    prefer_running: bool = True,
    backend: Backend = "auto",
    platform: Optional[str] = None,
) -> Any:
    """
    Return a live Photoshop application object.

    Parameters
    ----------
    prefer_running:
        On Windows, try attaching to a running instance before launching.
    backend:
        ``comtypes``, ``win32com``, or ``auto`` (Windows only).
    platform:
        Override platform detection (``win32`` / ``darwin``) for testing.

    On macOS, prefers an explicit app path (see ``PHOTOSHOP_APP_PATH`` and
    known ``/Applications/Adobe Photoshop <year>/...`` locations) so Beta and
    release installs that share ``com.adobe.Photoshop`` are not mixed up.
    """
    plat = platform or sys.platform
    if plat == "darwin":
        return _mac_get_app()
    if plat.startswith("win"):
        return _windows_get_app(backend, prefer_running)
    raise PhotoshopNotFoundError(
        f"Unsupported platform {plat!r}. "
        "Use Windows (COM) or macOS (appscript). "
        "See docs/landscape.md for cloud/API alternatives."
    )


def is_photoshop_running(backend: Backend = "auto") -> bool:
    """Return True if a Photoshop instance can be attached."""
    if sys.platform == "darwin":
        try:
            ps = _mac_get_app()
            return ps is not None
        except PhotoshopNotFoundError:
            return False
    if not sys.platform.startswith("win"):
        return False
    try:
        if backend == "win32com":
            from win32com.client import GetActiveObject

            GetActiveObject(_PROG_ID)
            return True
        from comtypes.client import GetActiveObject

        GetActiveObject(_PROG_ID)
        return True
    except Exception:  # noqa: BLE001
        if backend == "auto":
            try:
                from win32com.client import GetActiveObject

                GetActiveObject(_PROG_ID)
                return True
            except Exception:  # noqa: BLE001
                return False
        return False


def photoshop_available() -> bool:
    """Best-effort check that COM/appscript bindings and Photoshop are usable."""
    try:
        get_app(prefer_running=True)
        return True
    except PhotoshopNotFoundError:
        return False


def create_solid_color(backend: Backend = "auto") -> Any:
    """Create a Photoshop.SolidColor COM object (Windows)."""
    if not sys.platform.startswith("win"):
        raise PhotoshopNotFoundError("SolidColor COM objects are Windows-only.")
    if backend in ("comtypes", "auto"):
        try:
            from comtypes.client import CreateObject

            return CreateObject("Photoshop.SolidColor")
        except Exception:
            if backend == "comtypes":
                raise
    from win32com.client import Dispatch

    return Dispatch("Photoshop.SolidColor")
