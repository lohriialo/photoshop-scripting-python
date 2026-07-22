"""
Helpers for Photoshop Action Manager (ExecuteAction) scripting on Windows.

Action Manager code is usually recorded via Adobe's ScriptListener plugin and
translated from JSX. These helpers reduce boilerplate around descriptors.
"""

from __future__ import annotations

import sys
from typing import Any, Optional

from .constants import DialogModes


def _dispatch(prog_id: str) -> Any:
    try:
        from comtypes.client import CreateObject

        return CreateObject(prog_id)
    except Exception:
        from win32com.client import Dispatch

        return Dispatch(prog_id)


def action_descriptor() -> Any:
    """Create a Photoshop.ActionDescriptor."""
    if not sys.platform.startswith("win"):
        raise RuntimeError("Action Manager COM helpers are Windows-only.")
    return _dispatch("Photoshop.ActionDescriptor")


def action_reference() -> Any:
    """Create a Photoshop.ActionReference."""
    if not sys.platform.startswith("win"):
        raise RuntimeError("Action Manager COM helpers are Windows-only.")
    return _dispatch("Photoshop.ActionReference")


def action_list() -> Any:
    """Create a Photoshop.ActionList."""
    if not sys.platform.startswith("win"):
        raise RuntimeError("Action Manager COM helpers are Windows-only.")
    return _dispatch("Photoshop.ActionList")


def char_id(app: Any, code: str) -> int:
    """app.CharIDToTypeID with 4-char padding."""
    if len(code) < 4:
        code = code.ljust(4)
    return app.CharIDToTypeID(code)


def string_id(app: Any, key: str) -> int:
    return app.StringIDToTypeID(key)


def execute(
    app: Any,
    event_id: int,
    descriptor: Optional[Any] = None,
    dialog_mode: int = DialogModes.NO,
) -> Any:
    """Execute an Action Manager event."""
    if descriptor is None:
        descriptor = action_descriptor()
    return app.ExecuteAction(event_id, descriptor, int(dialog_mode))


def do_action(app: Any, action_name: str, action_set: str, dialog_mode: int = DialogModes.NO) -> None:
    """Play a named action from an action set (Actions panel)."""
    desc = action_descriptor()
    ref = action_reference()
    ref.PutName(char_id(app, "Actn"), action_name)
    ref.PutName(char_id(app, "ASet"), action_set)
    desc.PutReference(char_id(app, "null"), ref)
    execute(app, char_id(app, "Ply "), desc, dialog_mode)


def do_javascript(app: Any, code: str, arguments: Optional[list[Any]] = None) -> Any:
    """
    Run ExtendScript/JSX from Python (Windows COM).

    Useful for reusing existing .jsx scripts or APIs missing from the COM surface.
    """
    args = arguments or []
    return app.DoJavaScript(code, args, 1)  # 1 = PsJavaScriptExecutionMode.psNeverShowDebugger


def do_javascript_file(app: Any, path: str, arguments: Optional[list[Any]] = None) -> Any:
    """Load and run a .jsx file."""
    args = arguments or []
    return app.DoJavaScriptFile(str(path), args, 1)
