#!/usr/bin/env python3
"""
Replace the contents of the active smart object with a new file, then save.

Typical template pipeline:
  1. Open a PSD template with a smart object placeholder
  2. Select the smart object layer
  3. Run this script with --content path/to/photo.jpg
  4. Export or save the composed result

This uses Action Manager IDs recorded from Photoshop's placed-object workflow.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting import DialogModes, get_app
from photoshop_scripting.actions import action_descriptor, char_id, execute, string_id
from photoshop_scripting.prefs import saved_preferences


def replace_contents(app, content_path: Path) -> None:
    """Replace active smart object contents with content_path."""
    desc = action_descriptor()
    desc.PutPath(char_id(app, "null"), str(content_path.resolve()))
    # placedLayerReplaceContents
    execute(app, string_id(app, "placedLayerReplaceContents"), desc, DialogModes.NO)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template",
        type=Path,
        help="Optional PSD template to open first",
    )
    parser.add_argument(
        "--content",
        type=Path,
        required=True,
        help="Image file to place into the active smart object",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional path to SaveAs the result (PSD)",
    )
    args = parser.parse_args()

    if not args.content.is_file():
        print(f"Content not found: {args.content}", file=sys.stderr)
        return 1

    app = get_app()
    with saved_preferences(app, dialogs=DialogModes.NO):
        if args.template:
            app.Open(str(args.template.resolve()))
        if len(app.Documents) < 1:
            print("Open a document with an active smart object layer first.", file=sys.stderr)
            return 1

        layer = app.ActiveDocument.ActiveLayer
        # PsLayerKind.psSmartObjectLayer == 17
        if int(layer.Kind) != 17:
            print(
                f"Active layer {layer.Name!r} is not a smart object (kind={layer.Kind}).",
                file=sys.stderr,
            )
            return 1

        replace_contents(app, args.content)
        print(f"Replaced smart object contents with {args.content}")

        if args.save:
            app.ActiveDocument.SaveAs(str(args.save.resolve()))
            print(f"Saved → {args.save}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
