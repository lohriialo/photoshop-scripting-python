"""Context managers for temporary Photoshop preference changes."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator, Optional

from .constants import DialogModes, Units


@contextmanager
def dialog_mode(app: Any, mode: int = DialogModes.NO) -> Iterator[Any]:
    """Temporarily set app.displayDialogs (Windows COM)."""
    previous = getattr(app, "displayDialogs", None)
    try:
        app.displayDialogs = int(mode)
        yield app
    finally:
        if previous is not None:
            try:
                app.displayDialogs = previous
            except Exception:  # noqa: BLE001
                pass


@contextmanager
def ruler_units(app: Any, units: int = Units.PIXELS) -> Iterator[Any]:
    """Temporarily set Preferences.RulerUnits (Windows COM)."""
    prefs = app.Preferences
    previous = prefs.RulerUnits
    try:
        prefs.RulerUnits = int(units)
        yield app
    finally:
        try:
            prefs.RulerUnits = previous
        except Exception:  # noqa: BLE001
            pass


@contextmanager
def saved_preferences(
    app: Any,
    *,
    units: Optional[int] = Units.PIXELS,
    type_units: Optional[int] = None,
    dialogs: Optional[int] = DialogModes.NO,
) -> Iterator[Any]:
    """
    Save and restore common preferences around a block of automation.

    Example:
        with saved_preferences(app):
            doc = app.Open(path)
            ...
    """
    prefs = app.Preferences
    prev_ruler = prefs.RulerUnits
    prev_type = getattr(prefs, "TypeUnits", None)
    prev_dialogs = getattr(app, "displayDialogs", None)
    try:
        if units is not None:
            prefs.RulerUnits = int(units)
        if type_units is not None and prev_type is not None:
            prefs.TypeUnits = int(type_units)
        if dialogs is not None:
            app.displayDialogs = int(dialogs)
        yield app
    finally:
        try:
            prefs.RulerUnits = prev_ruler
        except Exception:  # noqa: BLE001
            pass
        if prev_type is not None and type_units is not None:
            try:
                prefs.TypeUnits = prev_type
            except Exception:  # noqa: BLE001
                pass
        if prev_dialogs is not None and dialogs is not None:
            try:
                app.displayDialogs = prev_dialogs
            except Exception:  # noqa: BLE001
                pass
