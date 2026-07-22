#!/usr/bin/env python3
"""Play a Photoshop Actions-panel action on every image in a folder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting.batch import iter_images, run_action_on_files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source folder")
    parser.add_argument("action", help='Action name, e.g. "Molten Lead"')
    parser.add_argument(
        "--set",
        dest="action_set",
        default="Default Actions",
        help='Action set name (default: "Default Actions")',
    )
    parser.add_argument("--no-save", action="store_true", help="Do not save after action")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    files = iter_images(args.input, recursive=args.recursive)
    if not files:
        print("No images found.", file=sys.stderr)
        return 1

    def progress(i, total, msg):
        print(f"[{i}/{total}] {msg}")

    results = run_action_on_files(
        files,
        args.action,
        args.action_set,
        save=not args.no_save,
        on_progress=progress,
    )
    print(f"Processed {len(results)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
