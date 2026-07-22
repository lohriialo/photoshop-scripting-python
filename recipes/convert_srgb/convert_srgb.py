#!/usr/bin/env python3
"""
Convert a folder of images to sRGB and export JPEG/PNG.

Fixes the classic “looks fine in Photoshop, wrong in the browser” profile issue.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting.batch import batch_convert_srgb, iter_images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source folder")
    parser.add_argument("output", type=Path, help="Destination folder")
    parser.add_argument("--format", choices=("jpg", "png"), default="jpg")
    parser.add_argument("--quality", type=int, default=10, help="JPEG quality 0–12")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    files = iter_images(args.input, recursive=args.recursive)
    if not files:
        print("No images found.", file=sys.stderr)
        return 1

    def progress(i, total, msg):
        print(f"[{i}/{total}] {msg}")

    results = batch_convert_srgb(
        files,
        args.output,
        format=args.format,
        quality=args.quality,
        on_progress=progress,
    )
    print(f"Converted {len(results)} file(s) → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
