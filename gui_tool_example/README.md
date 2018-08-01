# GUI tool example with Photoshop Scripting in Python
This example demonstrates how to use a GUI toolkit like PyQt to build your own custom tool/utility which can then interact with Photoshop via COM on Windows.

![](https://i.imgur.com/6l3kXw8.png "Photoshop Bulk Image Resizer")

# Requiremments:
- `Python 3.x`
- `PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5`
- `http://www.pyinstaller.org/`

# Convert .ui to .py with pyuic5
- `pyuic5 <path to resizer_ui.ui> -o <outputpath to resizer_ui.py>`

# Compile the app to executable using pyInstaller
- `pyinstaller <path to appplication main app.py>`
