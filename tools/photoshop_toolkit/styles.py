"""Photoshop-inspired dark theme for the toolkit."""

APP_STYLE = """
* {
    font-family: "Segoe UI", "SF Pro Text", "Helvetica Neue", sans-serif;
    font-size: 13px;
}

QMainWindow, QWidget#central {
    background-color: #1b1b1f;
    color: #e8e8ed;
}

QFrame#sidebar {
    background-color: #121216;
    border-right: 1px solid #2a2a32;
}

QLabel#brand {
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.3px;
    padding: 4px 0 2px 0;
}

QLabel#brandSub {
    color: #8b8b9a;
    font-size: 11px;
    padding-bottom: 12px;
}

QPushButton#navBtn {
    text-align: left;
    padding: 10px 14px;
    border: none;
    border-radius: 8px;
    color: #c4c4d0;
    background: transparent;
    font-weight: 500;
}

QPushButton#navBtn:hover {
    background-color: #23232b;
    color: #ffffff;
}

QPushButton#navBtn[active="true"] {
    background-color: #0d99ff22;
    color: #0d99ff;
    border: 1px solid #0d99ff55;
}

QLabel#pageTitle {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    padding-bottom: 2px;
}

QLabel#pageDesc {
    color: #9a9aab;
    font-size: 12px;
    padding-bottom: 14px;
}

QGroupBox {
    border: 1px solid #2e2e38;
    border-radius: 10px;
    margin-top: 12px;
    padding: 16px 12px 12px 12px;
    background-color: #222228;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #b8b8c8;
}

QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QPlainTextEdit {
    background-color: #16161b;
    border: 1px solid #34343f;
    border-radius: 6px;
    padding: 7px 10px;
    color: #f0f0f5;
    selection-background-color: #0d99ff;
}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QPlainTextEdit:focus {
    border: 1px solid #0d99ff;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #1e1e24;
    color: #e8e8ed;
    selection-background-color: #0d99ff;
    border: 1px solid #34343f;
}

QCheckBox {
    spacing: 8px;
    color: #d0d0dc;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #4a4a58;
    background: #16161b;
}

QCheckBox::indicator:checked {
    background: #0d99ff;
    border-color: #0d99ff;
}

QPushButton#primary {
    background-color: #0d99ff;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton#primary:hover {
    background-color: #3aafff;
}

QPushButton#primary:disabled {
    background-color: #2a4a66;
    color: #89a;
}

QPushButton#secondary {
    background-color: #2a2a34;
    color: #e8e8ed;
    border: 1px solid #3c3c48;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 500;
}

QPushButton#secondary:hover {
    background-color: #343440;
}

QPushButton#danger {
    background-color: #3a2226;
    color: #ff8a9a;
    border: 1px solid #6a3038;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 600;
}

QPushButton#danger:hover {
    background-color: #4a2a30;
}

QProgressBar {
    border: 1px solid #34343f;
    border-radius: 6px;
    background: #16161b;
    text-align: center;
    color: #ddd;
    height: 18px;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #0d99ff, stop:1 #5cc8ff);
    border-radius: 5px;
}

QPlainTextEdit#log {
    background-color: #0f0f12;
    border: 1px solid #2a2a32;
    border-radius: 8px;
    font-family: "Cascadia Code", "Consolas", "Menlo", monospace;
    font-size: 11px;
    color: #a8d4a8;
}

QLabel#statusOk {
    color: #5dca7a;
    font-weight: 600;
}

QLabel#statusBad {
    color: #ff7b8a;
    font-weight: 600;
}

QLabel#statusWarn {
    color: #e0b44c;
    font-weight: 600;
}

QScrollArea {
    border: none;
    background: transparent;
}

QFrame#card {
    background-color: #222228;
    border: 1px solid #2e2e38;
    border-radius: 10px;
}
"""
