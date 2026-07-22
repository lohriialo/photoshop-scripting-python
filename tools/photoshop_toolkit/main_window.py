"""Main window for Photoshop Toolkit."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .styles import APP_STYLE
from .workers import BatchWorker, collect_images

NAV_ITEMS = [
    ("resize", "Batch Resize", "Scale folders of images with optional aspect lock"),
    ("export", "Batch Export", "Export PSD/TIFF/etc. to JPEG or PNG for delivery"),
    ("comps", "Layer Comps", "Export every layer comp in a PSD to separate files"),
    ("actions", "Run Actions", "Apply a Photoshop Actions-panel action across a folder"),
    ("layers", "Export Layers", "Save each art layer as its own PNG/JPEG (top forum ask)"),
    ("watermark", "Watermark", "Stamp copyright text on a folder of images"),
    ("srgb", "Convert sRGB", "Web-safe sRGB conversion for client delivery"),
    ("border", "Canvas Border", "Add equal padding around images"),
    ("text", "Text Replace", "Find/replace across text layers in PSD folders"),
    ("about", "About", "Status, setup, and project links"),
]


def make_card(title: str) -> Tuple[QFrame, QGridLayout]:
    frame = QFrame()
    frame.setObjectName("card")
    outer = QVBoxLayout(frame)
    outer.setContentsMargins(14, 12, 14, 12)
    label = QLabel(title)
    font = QFont()
    font.setBold(True)
    label.setFont(font)
    label.setStyleSheet("color: #b8b8c8; padding-bottom: 6px;")
    grid = QGridLayout()
    grid.setHorizontalSpacing(10)
    grid.setVerticalSpacing(8)
    outer.addWidget(label)
    outer.addLayout(grid)
    return frame, grid


class PathRow(QWidget):
    def __init__(self, label: str, mode: str = "dir", parent=None):
        super().__init__(parent)
        self.mode = mode
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(label)
        btn = QPushButton("Browse…")
        btn.setObjectName("secondary")
        btn.clicked.connect(self._browse)
        layout.addWidget(self.edit, 1)
        layout.addWidget(btn)

    def _browse(self) -> None:
        if self.mode == "file":
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Select file",
                "",
                "Photoshop (*.psd *.psb);;Images (*.png *.jpg *.jpeg *.tif *.tiff);;All (*.*)",
            )
        else:
            path = QFileDialog.getExistingDirectory(self, "Select folder")
        if path:
            self.edit.setText(path)

    def text(self) -> str:
        return self.edit.text().strip()

    def setText(self, value: str) -> None:
        self.edit.setText(value)


class ToolkitWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Photoshop Toolkit")
        self.resize(980, 680)
        self.setMinimumSize(860, 560)
        self.setStyleSheet(APP_STYLE)

        self._worker: Optional[BatchWorker] = None
        self._nav_buttons: Dict[str, QPushButton] = {}

        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(232)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(16, 20, 16, 16)
        side_layout.setSpacing(4)

        brand = QLabel("Photoshop Toolkit")
        brand.setObjectName("brand")
        brand_sub = QLabel("Production automation")
        brand_sub.setObjectName("brandSub")
        side_layout.addWidget(brand)
        side_layout.addWidget(brand_sub)

        for key, title, _ in NAV_ITEMS:
            btn = QPushButton(title)
            btn.setObjectName("navBtn")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("active", "false")
            btn.clicked.connect(lambda checked=False, k=key: self._show_page(k))
            side_layout.addWidget(btn)
            self._nav_buttons[key] = btn

        side_layout.addStretch(1)
        self.status_label = QLabel("Checking Photoshop…")
        self.status_label.setWordWrap(True)
        side_layout.addWidget(self.status_label)

        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(28, 24, 28, 20)
        main_layout.setSpacing(8)

        self.stack = QStackedWidget()
        self.pages = {
            "resize": self._build_resize_page(),
            "export": self._build_export_page(),
            "comps": self._build_comps_page(),
            "actions": self._build_actions_page(),
            "layers": self._build_layers_page(),
            "watermark": self._build_watermark_page(),
            "srgb": self._build_srgb_page(),
            "border": self._build_border_page(),
            "text": self._build_text_page(),
            "about": self._build_about_page(),
        }
        for key, _, _ in NAV_ITEMS:
            self.stack.addWidget(self.pages[key])

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        controls = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("danger")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._cancel_job)
        controls.addStretch(1)
        controls.addWidget(self.cancel_btn)

        self.log = QPlainTextEdit()
        self.log.setObjectName("log")
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)
        self.log.setPlaceholderText("Job log will appear here…")

        main_layout.addWidget(self.stack, 1)
        main_layout.addWidget(self.progress)
        main_layout.addLayout(controls)
        main_layout.addWidget(QLabel("Activity log"))
        main_layout.addWidget(self.log)

        root.addWidget(sidebar)
        root.addWidget(main, 1)

        self._show_page("resize")
        self._refresh_ps_status()

    def _show_page(self, key: str) -> None:
        index = [k for k, _, _ in NAV_ITEMS].index(key)
        self.stack.setCurrentIndex(index)
        for k, btn in self._nav_buttons.items():
            btn.setProperty("active", "true" if k == key else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _page_header(self, title: str, desc: str) -> QVBoxLayout:
        wrap = QVBoxLayout()
        t = QLabel(title)
        t.setObjectName("pageTitle")
        d = QLabel(desc)
        d.setObjectName("pageDesc")
        d.setWordWrap(True)
        wrap.addWidget(t)
        wrap.addWidget(d)
        return wrap

    def _build_resize_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Batch Resize",
                "Resize every image in a folder. Lock aspect ratio or set exact width × height.",
            )
        )

        box, form = make_card("Source & output")
        self.resize_input = PathRow("Input folder")
        self.resize_output = PathRow("Output folder (empty = overwrite originals)")
        self.resize_recursive = QCheckBox("Include subfolders")
        form.addWidget(QLabel("Input"), 0, 0)
        form.addWidget(self.resize_input, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.resize_output, 1, 1)
        form.addWidget(self.resize_recursive, 2, 1)
        layout.addWidget(box)

        opts, grid = make_card("Dimensions")
        self.resize_width = QSpinBox()
        self.resize_width.setRange(1, 30000)
        self.resize_width.setValue(1920)
        self.resize_height = QSpinBox()
        self.resize_height.setRange(0, 30000)
        self.resize_height.setValue(0)
        self.resize_height.setSpecialValueText("Auto (keep aspect)")
        self.keep_aspect = QCheckBox("Keep aspect ratio (ignore height)")
        self.keep_aspect.setChecked(True)
        self.keep_aspect.toggled.connect(lambda on: self.resize_height.setEnabled(not on))
        self.resize_height.setEnabled(False)
        self.resize_resample = QComboBox()
        self.resize_resample.addItem("Automatic", 8)
        self.resize_resample.addItem("Preserve Details", 9)
        self.resize_resample.addItem("Bicubic Sharper", 5)
        self.resize_resample.addItem("Bicubic Smoother", 6)
        self.resize_resample.addItem("Bicubic", 4)
        self.resize_resample.addItem("Bilinear", 3)
        self.resize_resample.addItem("Nearest Neighbor", 2)
        grid.addWidget(QLabel("Width (px)"), 0, 0)
        grid.addWidget(self.resize_width, 0, 1)
        grid.addWidget(QLabel("Height (px)"), 0, 2)
        grid.addWidget(self.resize_height, 0, 3)
        grid.addWidget(self.keep_aspect, 1, 1, 1, 2)
        grid.addWidget(QLabel("Resample"), 2, 0)
        grid.addWidget(self.resize_resample, 2, 1, 1, 3)
        layout.addWidget(opts)

        run = QPushButton("Resize folder")
        run.setObjectName("primary")
        run.clicked.connect(self._run_resize)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_export_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Batch Export",
                "Open each file and save a delivery-ready JPEG or PNG copy. Ideal for PSD → client folders.",
            )
        )
        box, form = make_card("Folders")
        self.export_input = PathRow("Input folder")
        self.export_output = PathRow("Output folder")
        self.export_recursive = QCheckBox("Include subfolders")
        self.export_format = QComboBox()
        self.export_format.addItems(["JPEG", "PNG"])
        self.export_quality = QSpinBox()
        self.export_quality.setRange(0, 12)
        self.export_quality.setValue(10)
        self.export_quality.setToolTip("JPEG quality 0–12 (Photoshop scale)")
        form.addWidget(QLabel("Input"), 0, 0)
        form.addWidget(self.export_input, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.export_output, 1, 1)
        form.addWidget(self.export_recursive, 2, 1)
        form.addWidget(QLabel("Format"), 3, 0)
        form.addWidget(self.export_format, 3, 1)
        form.addWidget(QLabel("JPEG quality"), 4, 0)
        form.addWidget(self.export_quality, 4, 1)
        layout.addWidget(box)

        run = QPushButton("Export folder")
        run.setObjectName("primary")
        run.clicked.connect(self._run_export)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_comps_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Layer Comp Exporter",
                "Apply each layer comp in a PSD and export a flat image — design handoff without manual clicking.",
            )
        )
        box, form = make_card("Source PSD")
        self.comps_psd = PathRow("Layer Comps PSD", mode="file")
        self.comps_output = PathRow("Output folder")
        self.comps_format = QComboBox()
        self.comps_format.addItems(["PNG", "JPEG"])
        form.addWidget(QLabel("PSD"), 0, 0)
        form.addWidget(self.comps_psd, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.comps_output, 1, 1)
        form.addWidget(QLabel("Format"), 2, 0)
        form.addWidget(self.comps_format, 2, 1)
        layout.addWidget(box)

        try:
            from photoshop_scripting.paths import sample_path

            sample = sample_path("Layer Comps.psd")
            if sample.is_file():
                hint = QLabel(f"Sample available: {sample}")
                hint.setObjectName("pageDesc")
                hint.setWordWrap(True)
                layout.addWidget(hint)
                use = QPushButton("Use sample PSD")
                use.setObjectName("secondary")
                use.clicked.connect(lambda: self.comps_psd.setText(str(sample)))
                layout.addWidget(use, alignment=Qt.AlignLeft)
        except Exception:
            pass

        run = QPushButton("Export layer comps")
        run.setObjectName("primary")
        run.clicked.connect(self._run_comps)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_actions_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Run Action on Folder",
                "Play any action from the Actions panel on every image. Names must match exactly.",
            )
        )
        box, form = make_card("Action & files")
        self.action_input = PathRow("Input folder")
        self.action_name = QLineEdit()
        self.action_name.setPlaceholderText("e.g. Molten Lead")
        self.action_set = QLineEdit()
        self.action_set.setPlaceholderText("e.g. Default Actions")
        self.action_set.setText("Default Actions")
        self.action_save = QCheckBox("Save after action")
        self.action_save.setChecked(True)
        self.action_recursive = QCheckBox("Include subfolders")
        form.addWidget(QLabel("Input"), 0, 0)
        form.addWidget(self.action_input, 0, 1)
        form.addWidget(QLabel("Action name"), 1, 0)
        form.addWidget(self.action_name, 1, 1)
        form.addWidget(QLabel("Action set"), 2, 0)
        form.addWidget(self.action_set, 2, 1)
        form.addWidget(self.action_save, 3, 1)
        form.addWidget(self.action_recursive, 4, 1)
        layout.addWidget(box)

        run = QPushButton("Run action on folder")
        run.setObjectName("primary")
        run.clicked.connect(self._run_action)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_layers_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Export Layers to Files",
                "The most requested automation on Adobe forums: each art layer → its own PNG/JPEG, "
                "keeping the full document canvas size.",
            )
        )
        box, form = make_card("Source PSD")
        self.layers_psd = PathRow("Photoshop document", mode="file")
        self.layers_output = PathRow("Output folder")
        self.layers_format = QComboBox()
        self.layers_format.addItems(["PNG", "JPEG"])
        self.layers_visible_only = QCheckBox("Only currently visible layers")
        form.addWidget(QLabel("PSD"), 0, 0)
        form.addWidget(self.layers_psd, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.layers_output, 1, 1)
        form.addWidget(QLabel("Format"), 2, 0)
        form.addWidget(self.layers_format, 2, 1)
        form.addWidget(self.layers_visible_only, 3, 1)
        layout.addWidget(box)
        try:
            from photoshop_scripting.paths import sample_path

            sample = sample_path("Layer Comps.psd")
            if sample.is_file():
                use = QPushButton("Use sample PSD")
                use.setObjectName("secondary")
                use.clicked.connect(lambda: self.layers_psd.setText(str(sample)))
                layout.addWidget(use, alignment=Qt.AlignLeft)
        except Exception:
            pass
        run = QPushButton("Export layers")
        run.setObjectName("primary")
        run.clicked.connect(self._run_layers)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_watermark_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Batch Watermark",
                "Stamp copyright / brand text on every image — common for portfolios and client proofs.",
            )
        )
        box, form = make_card("Folder & text")
        self.wm_input = PathRow("Input folder")
        self.wm_output = PathRow("Output folder")
        self.wm_text = QLineEdit()
        self.wm_text.setText("© Copyright")
        self.wm_opacity = QSpinBox()
        self.wm_opacity.setRange(5, 100)
        self.wm_opacity.setValue(40)
        self.wm_size = QSpinBox()
        self.wm_size.setRange(8, 200)
        self.wm_size.setValue(28)
        self.wm_recursive = QCheckBox("Include subfolders")
        form.addWidget(QLabel("Input"), 0, 0)
        form.addWidget(self.wm_input, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.wm_output, 1, 1)
        form.addWidget(QLabel("Text"), 2, 0)
        form.addWidget(self.wm_text, 2, 1)
        form.addWidget(QLabel("Opacity %"), 3, 0)
        form.addWidget(self.wm_opacity, 3, 1)
        form.addWidget(QLabel("Font size"), 4, 0)
        form.addWidget(self.wm_size, 4, 1)
        form.addWidget(self.wm_recursive, 5, 1)
        layout.addWidget(box)
        run = QPushButton("Watermark folder")
        run.setObjectName("primary")
        run.clicked.connect(self._run_watermark)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_srgb_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Convert to sRGB",
                "Normalize color for web and client delivery (fixes “looks different in browser” reports).",
            )
        )
        box, form = make_card("Folders")
        self.srgb_input = PathRow("Input folder")
        self.srgb_output = PathRow("Output folder")
        self.srgb_format = QComboBox()
        self.srgb_format.addItems(["JPEG", "PNG"])
        self.srgb_quality = QSpinBox()
        self.srgb_quality.setRange(0, 12)
        self.srgb_quality.setValue(10)
        self.srgb_recursive = QCheckBox("Include subfolders")
        form.addWidget(QLabel("Input"), 0, 0)
        form.addWidget(self.srgb_input, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.srgb_output, 1, 1)
        form.addWidget(QLabel("Format"), 2, 0)
        form.addWidget(self.srgb_format, 2, 1)
        form.addWidget(QLabel("JPEG quality"), 3, 0)
        form.addWidget(self.srgb_quality, 3, 1)
        form.addWidget(self.srgb_recursive, 4, 1)
        layout.addWidget(box)
        run = QPushButton("Convert folder to sRGB")
        run.setObjectName("primary")
        run.clicked.connect(self._run_srgb)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_border_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Canvas Border / Padding",
                "Expand the canvas evenly on all sides — useful for mockups, social frames, and safe margins.",
            )
        )
        box, form = make_card("Padding")
        self.border_input = PathRow("Input folder")
        self.border_output = PathRow("Output folder")
        self.border_pad = QSpinBox()
        self.border_pad.setRange(0, 2000)
        self.border_pad.setValue(40)
        self.border_format = QComboBox()
        self.border_format.addItems(["PNG", "JPEG"])
        self.border_recursive = QCheckBox("Include subfolders")
        form.addWidget(QLabel("Input"), 0, 0)
        form.addWidget(self.border_input, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.border_output, 1, 1)
        form.addWidget(QLabel("Padding (px)"), 2, 0)
        form.addWidget(self.border_pad, 2, 1)
        form.addWidget(QLabel("Format"), 3, 0)
        form.addWidget(self.border_format, 3, 1)
        form.addWidget(self.border_recursive, 4, 1)
        layout.addWidget(box)
        run = QPushButton("Add canvas border")
        run.setObjectName("primary")
        run.clicked.connect(self._run_border)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_text_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "Text Layer Find / Replace",
                "Bulk-update names, prices, or locales across PSD templates — a staple localization ask.",
            )
        )
        box, form = make_card("Search folder of PSDs")
        self.text_input = PathRow("Input folder")
        self.text_output = PathRow("Output folder (optional copy)")
        self.text_find = QLineEdit()
        self.text_find.setPlaceholderText("Find text")
        self.text_replace = QLineEdit()
        self.text_replace.setPlaceholderText("Replace with")
        self.text_recursive = QCheckBox("Include subfolders")
        form.addWidget(QLabel("Input"), 0, 0)
        form.addWidget(self.text_input, 0, 1)
        form.addWidget(QLabel("Output"), 1, 0)
        form.addWidget(self.text_output, 1, 1)
        form.addWidget(QLabel("Find"), 2, 0)
        form.addWidget(self.text_find, 2, 1)
        form.addWidget(QLabel("Replace"), 3, 0)
        form.addWidget(self.text_replace, 3, 1)
        form.addWidget(self.text_recursive, 4, 1)
        layout.addWidget(box)
        run = QPushButton("Replace text in folder")
        run.setObjectName("primary")
        run.clicked.connect(self._run_text)
        layout.addWidget(run, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _build_about_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(
            self._page_header(
                "About",
                "Part of photoshop-scripting-python — open-source Photoshop automation for Python.",
            )
        )
        body = QLabel(
            "<p>This toolkit drives a <b>local</b> Photoshop install via COM (Windows).</p>"
            "<p>Tools map to the most common Adobe community requests:</p>"
            "<ul>"
            "<li><b>Resize / Export / Layer Comps / Actions</b> — everyday delivery</li>"
            "<li><b>Export Layers</b> — “layers to files” (top forum ask)</li>"
            "<li><b>Watermark</b> — proofs &amp; portfolio protection</li>"
            "<li><b>sRGB</b> — web color consistency</li>"
            "<li><b>Canvas Border</b> — padding / mockup frames</li>"
            "<li><b>Text Replace</b> — template localization</li>"
            "</ul>"
            "<p>CLI recipes live in <code>recipes/</code>. Legacy simple resizer: "
            "<code>tools/gui_tool_example/</code>.</p>"
            "<p>GitHub: "
            "<a href='https://github.com/lohriialo/photoshop-scripting-python' style='color:#0d99ff'>"
            "lohriialo/photoshop-scripting-python</a></p>"
        )
        body.setWordWrap(True)
        body.setOpenExternalLinks(True)
        layout.addWidget(body)

        refresh = QPushButton("Recheck Photoshop connection")
        refresh.setObjectName("secondary")
        refresh.clicked.connect(self._refresh_ps_status)
        layout.addWidget(refresh, alignment=Qt.AlignLeft)
        layout.addStretch(1)
        return page

    def _refresh_ps_status(self) -> None:
        try:
            from photoshop_scripting import is_photoshop_running

            if sys.platform.startswith("win"):
                if is_photoshop_running():
                    self.status_label.setText("Photoshop: connected")
                    self.status_label.setObjectName("statusOk")
                else:
                    self.status_label.setText("Photoshop: not running\n(will launch on run)")
                    self.status_label.setObjectName("statusWarn")
            else:
                self.status_label.setText(
                    f"Platform: {sys.platform}\nToolkit is Windows COM focused"
                )
                self.status_label.setObjectName("statusWarn")
        except Exception as exc:  # noqa: BLE001
            self.status_label.setText(f"Status error:\n{exc}")
            self.status_label.setObjectName("statusBad")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    def _set_busy(self, busy: bool) -> None:
        self.cancel_btn.setEnabled(busy)
        if not busy:
            self.progress.setValue(0)

    def _start_worker(self, job: str, params: dict) -> None:
        if self._worker and self._worker.isRunning():
            QMessageBox.warning(self, "Busy", "A job is already running.")
            return
        self.log.clear()
        self.log.appendPlainText(f"Starting job: {job}")
        self._set_busy(True)
        self._worker = BatchWorker(job, params)
        self._worker.progress.connect(self._on_progress)
        self._worker.log.connect(self.log.appendPlainText)
        self._worker.finished_ok.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._worker.start()

    def _on_progress(self, current: int, total: int, message: str) -> None:
        if total > 0:
            self.progress.setValue(int(current * 100 / total))

    def _on_finished(self, results: list) -> None:
        self._set_busy(False)
        self.progress.setValue(100)
        self.log.appendPlainText(f"Done. {len(results)} file(s) processed.")
        QMessageBox.information(self, "Complete", f"Processed {len(results)} file(s).")
        self._refresh_ps_status()

    def _on_failed(self, message: str) -> None:
        self._set_busy(False)
        self.log.appendPlainText(f"ERROR: {message}")
        QMessageBox.critical(self, "Job failed", message)
        self._refresh_ps_status()

    def _cancel_job(self) -> None:
        if self._worker and self._worker.isRunning():
            self._worker.cancel()
            self.log.appendPlainText("Cancel requested…")

    def _run_resize(self) -> None:
        folder = self.resize_input.text()
        if not folder:
            QMessageBox.warning(self, "Missing input", "Choose an input folder.")
            return
        try:
            files = collect_images(folder, recursive=self.resize_recursive.isChecked())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Input error", str(exc))
            return
        if not files:
            QMessageBox.warning(self, "No images", "No supported images found.")
            return
        height = None if self.keep_aspect.isChecked() else self.resize_height.value()
        out = self.resize_output.text() or None
        self._start_worker(
            "resize",
            {
                "files": files,
                "width": self.resize_width.value(),
                "height": height,
                "resample": self.resize_resample.currentData(),
                "output_dir": out,
            },
        )

    def _run_export(self) -> None:
        folder = self.export_input.text()
        out = self.export_output.text()
        if not folder or not out:
            QMessageBox.warning(self, "Missing paths", "Input and output folders are required.")
            return
        try:
            files = collect_images(folder, recursive=self.export_recursive.isChecked())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Input error", str(exc))
            return
        if not files:
            QMessageBox.warning(self, "No images", "No supported images found.")
            return
        fmt = self.export_format.currentText()
        job = "export_jpeg" if fmt == "JPEG" else "export_png"
        self._start_worker(
            job,
            {
                "files": files,
                "output_dir": out,
                "quality": self.export_quality.value(),
            },
        )

    def _run_comps(self) -> None:
        psd = self.comps_psd.text()
        out = self.comps_output.text()
        if not psd or not out:
            QMessageBox.warning(self, "Missing paths", "PSD path and output folder are required.")
            return
        if not Path(psd).is_file():
            QMessageBox.warning(self, "Missing file", f"PSD not found:\n{psd}")
            return
        self._start_worker(
            "layer_comps",
            {
                "psd_path": psd,
                "output_dir": out,
                "format": self.comps_format.currentText().lower(),
            },
        )

    def _run_action(self) -> None:
        folder = self.action_input.text()
        name = self.action_name.text().strip()
        aset = self.action_set.text().strip()
        if not folder or not name or not aset:
            QMessageBox.warning(self, "Missing fields", "Folder, action name, and set are required.")
            return
        try:
            files = collect_images(folder, recursive=self.action_recursive.isChecked())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Input error", str(exc))
            return
        if not files:
            QMessageBox.warning(self, "No images", "No supported images found.")
            return
        self._start_worker(
            "run_action",
            {
                "files": files,
                "action_name": name,
                "action_set": aset,
                "save": self.action_save.isChecked(),
            },
        )

    def _run_layers(self) -> None:
        psd = self.layers_psd.text()
        out = self.layers_output.text()
        if not psd or not out:
            QMessageBox.warning(self, "Missing paths", "PSD and output folder are required.")
            return
        if not Path(psd).is_file():
            QMessageBox.warning(self, "Missing file", f"PSD not found:\n{psd}")
            return
        self._start_worker(
            "export_layers",
            {
                "psd_path": psd,
                "output_dir": out,
                "format": self.layers_format.currentText().lower(),
                "visible_only": self.layers_visible_only.isChecked(),
            },
        )

    def _run_watermark(self) -> None:
        folder = self.wm_input.text()
        out = self.wm_output.text()
        text = self.wm_text.text().strip()
        if not folder or not out or not text:
            QMessageBox.warning(self, "Missing fields", "Input, output, and watermark text are required.")
            return
        try:
            files = collect_images(folder, recursive=self.wm_recursive.isChecked())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Input error", str(exc))
            return
        if not files:
            QMessageBox.warning(self, "No images", "No supported images found.")
            return
        self._start_worker(
            "watermark",
            {
                "files": files,
                "output_dir": out,
                "text": text,
                "opacity": float(self.wm_opacity.value()),
                "font_size": float(self.wm_size.value()),
            },
        )

    def _run_srgb(self) -> None:
        folder = self.srgb_input.text()
        out = self.srgb_output.text()
        if not folder or not out:
            QMessageBox.warning(self, "Missing paths", "Input and output folders are required.")
            return
        try:
            files = collect_images(folder, recursive=self.srgb_recursive.isChecked())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Input error", str(exc))
            return
        if not files:
            QMessageBox.warning(self, "No images", "No supported images found.")
            return
        fmt = "jpg" if self.srgb_format.currentText() == "JPEG" else "png"
        self._start_worker(
            "srgb",
            {
                "files": files,
                "output_dir": out,
                "format": fmt,
                "quality": self.srgb_quality.value(),
            },
        )

    def _run_border(self) -> None:
        folder = self.border_input.text()
        out = self.border_output.text()
        if not folder or not out:
            QMessageBox.warning(self, "Missing paths", "Input and output folders are required.")
            return
        try:
            files = collect_images(folder, recursive=self.border_recursive.isChecked())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Input error", str(exc))
            return
        if not files:
            QMessageBox.warning(self, "No images", "No supported images found.")
            return
        fmt = self.border_format.currentText().lower()
        self._start_worker(
            "border",
            {
                "files": files,
                "output_dir": out,
                "padding_px": self.border_pad.value(),
                "format": fmt,
            },
        )

    def _run_text(self) -> None:
        folder = self.text_input.text()
        find = self.text_find.text()
        if not folder or find == "":
            QMessageBox.warning(self, "Missing fields", "Input folder and find text are required.")
            return
        try:
            files = collect_images(folder, recursive=self.text_recursive.isChecked())
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Input error", str(exc))
            return
        # Prefer PSD/PSB for text work
        files = [f for f in files if f.suffix.lower() in {".psd", ".psb"}] or files
        if not files:
            QMessageBox.warning(self, "No files", "No images/PSDs found.")
            return
        out = self.text_output.text() or None
        self._start_worker(
            "text_replace",
            {
                "files": files,
                "find": find,
                "replace": self.text_replace.text(),
                "output_dir": out,
                "save": out is None,
            },
        )
