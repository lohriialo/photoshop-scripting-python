#!/usr/bin/env python3
"""
Stamp a text watermark on every image in a folder.

Popular for portfolio proofs, client previews, and stock protection.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting.batch import batch_watermark_text, iter_images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source folder")
    parser.add_argument("output", type=Path, help="Destination folder")
    parser.add_argument("--text", default="© Copyright", help="Watermark text")
    parser.add_argument("--opacity", type=float, default=40.0, help="Layer opacity 1–100")
    parser.add_argument("--size", type=float, default=28.0, help="Font size (pt)")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    files = iter_images(args.input, recursive=args.recursive)
    if not files:
        print("No images found.", file=sys.stderr)
        return 1

    def progress(i, total, msg):
        print(f"[{i}/{total}] {msg}")

    results = batch_watermark_text(
        files,
        args.output,
        text=args.text,
        opacity=args.opacity,
        font_size=args.size,
        on_progress=progress,
    )
    print(f"Watermarked {len(results)} file(s) → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
