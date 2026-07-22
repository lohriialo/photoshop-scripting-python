#!/usr/bin/env python3
"""Export every image in a folder to JPEG or PNG."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from a git clone without install
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting.batch import batch_export_jpeg, batch_export_png, iter_images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source folder")
    parser.add_argument("output", type=Path, help="Destination folder")
    parser.add_argument("--format", choices=("jpg", "png"), default="jpg")
    parser.add_argument("--quality", type=int, default=10, help="JPEG quality 0-12")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    files = iter_images(args.input, recursive=args.recursive)
    if not files:
        print("No images found.", file=sys.stderr)
        return 1

    def progress(i, total, msg):
        print(f"[{i}/{total}] {msg}")

    if args.format == "png":
        out = batch_export_png(files, args.output, on_progress=progress)
    else:
        out = batch_export_jpeg(
            files, args.output, quality=args.quality, on_progress=progress
        )
    print(f"Exported {len(out)} file(s) → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
