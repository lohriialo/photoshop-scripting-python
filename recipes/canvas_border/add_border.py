#!/usr/bin/env python3
"""
Add equal canvas padding around every image in a folder.

Useful for social safe-margins, mockup frames, and product shots on a matte.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting.batch import batch_add_canvas_border, iter_images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source folder")
    parser.add_argument("output", type=Path, help="Destination folder")
    parser.add_argument("--padding", type=int, default=40, help="Pixels on each side")
    parser.add_argument("--format", choices=("png", "jpg"), default="png")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    files = iter_images(args.input, recursive=args.recursive)
    if not files:
        print("No images found.", file=sys.stderr)
        return 1

    def progress(i, total, msg):
        print(f"[{i}/{total}] {msg}")

    results = batch_add_canvas_border(
        files,
        args.output,
        padding_px=args.padding,
        format=args.format,
        on_progress=progress,
    )
    print(f"Bordered {len(results)} file(s) → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
