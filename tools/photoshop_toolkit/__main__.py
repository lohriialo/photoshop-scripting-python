"""Entry point: python -m tools.photoshop_toolkit"""

from __future__ import annotations

import sys


def main() -> int:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print(
            "PySide6 is required for the toolkit UI.\n"
            "  pip install 'photoshop-scripting-python[gui]'\n"
            "  # or: pip install PySide6",
            file=sys.stderr,
        )
        return 1

    # Ensure repo root is importable when run as a module from a clone
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from tools.photoshop_toolkit.main_window import ToolkitWindow

    app = QApplication(sys.argv)
    app.setApplicationName("Photoshop Toolkit")
    app.setOrganizationName("photoshop-scripting-python")
    window = ToolkitWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
