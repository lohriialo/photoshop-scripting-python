#!/usr/bin/env python3
"""
Find/replace text across every text layer in a folder of PSDs.

Common for localization, seasonal copy, and template pipelines
(e.g. replace "PLACEHOLDER" with a product name).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting.batch import batch_replace_text, iter_images


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Folder of PSD/PSB (or images with text layers)")
    parser.add_argument("find", help="Text to find")
    parser.add_argument("replace", help="Replacement text")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional folder for copies (default: save in place)",
    )
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()

    files = iter_images(args.input, recursive=args.recursive)
    files = [f for f in files if f.suffix.lower() in {".psd", ".psb"}] or files
    if not files:
        print("No files found.", file=sys.stderr)
        return 1

    def progress(i, total, msg):
        print(f"[{i}/{total}] {msg}")

    results = batch_replace_text(
        files,
        args.find,
        args.replace,
        save=args.output is None,
        output_dir=args.output,
        on_progress=progress,
    )
    print(f"Processed {len(results)} file(s).")
    for line in results:
        print(" ", line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
