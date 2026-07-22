#!/usr/bin/env python3
"""
Run ExtendScript (JSX) from Python.

Useful when you already have a .jsx library, or need APIs that are awkward
via COM. Requires Windows + Photoshop.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from photoshop_scripting import get_app
from photoshop_scripting.actions import do_javascript, do_javascript_file


DEMO_JSX = r"""
var doc = app.documents.add(800, 600, 72, "Python JSX Bridge");
var layer = doc.artLayers.add();
layer.kind = LayerKind.TEXT;
layer.textItem.contents = "Hello from JSX via Python";
layer.textItem.size = 36;
"ok";
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "jsx",
        type=Path,
        nargs="?",
        help="Optional path to a .jsx file (default: run built-in demo snippet)",
    )
    args = parser.parse_args()

    app = get_app()
    if args.jsx:
        result = do_javascript_file(app, str(args.jsx.resolve()))
    else:
        result = do_javascript(app, DEMO_JSX)
    print(f"JSX finished. Result: {result!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
