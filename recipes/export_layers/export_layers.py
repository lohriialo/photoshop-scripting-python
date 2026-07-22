#!/usr/bin/env python3
"""
Export each art layer in a PSD to its own PNG/JPEG.

#1 automation request on Adobe community forums ("layers to files").
Isolates one layer at a time while keeping the full document canvas.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting.batch import export_layers_to_files
from photoshop_scripting.paths import sample_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "psd",
        type=Path,
        nargs="?",
        default=None,
        help="Source PSD (default: sample Layer Comps.psd)",
    )
    parser.add_argument("output", type=Path, help="Destination folder")
    parser.add_argument("--format", choices=("png", "jpg"), default="png")
    parser.add_argument("--visible-only", action="store_true")
    args = parser.parse_args()

    psd = args.psd or sample_path("Layer Comps.psd")
    if not Path(psd).is_file():
        print(f"PSD not found: {psd}", file=sys.stderr)
        return 1

    def progress(i, total, msg):
        print(f"[{i}/{total}] {msg}")

    results = export_layers_to_files(
        psd,
        args.output,
        format=args.format,
        visible_only=args.visible_only,
        on_progress=progress,
    )
    print(f"Exported {len(results)} layer(s) → {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
