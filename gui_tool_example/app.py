from comtypes.client import GetActiveObject, CreateObject

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIntValidator

import os
import sys
import time

from resizer_ui import Ui_Dialog

class MainUIClass(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()

        # thread
        self.myworker = WorkerThread()
        # self.photoshop = GetActiveObject("Photoshop.Application")
        self.filestoprocess = []

        # aspect ratio is maintained by default
        self.ui.height_text.setReadOnly(True)

        # To allow only int
        self.onlyInt = QIntValidator()
        self.ui.height_text.setValidator(self.onlyInt)
        self.ui.width_text.setValidator(self.onlyInt)
        self.ui.resolution_text.setValidator(self.onlyInt)

        # UI buttons clicked handler
        self.ui.browse_btn.clicked.connect(self.browse_folder)
        self.ui.resize_btn.clicked.connect(self.resize_image)
        self.ui.reset_btn.clicked.connect(self.reset_input)
        self.ui.aspect_ratio_checkbox.stateChanged.connect(self.aspect_ratio)

    def browse_folder(self):
        in_folder = QFileDialog.getExistingDirectory()
        self.ui.browse_text.setText(QDir.toNativeSeparators(in_folder))

    def reset_input(self):
        self.ui.browse_text.setText("")
        self.ui.height_text.setText("")
        self.ui.width_text.setText("")
        self.ui.resolution_text.setText("")
        self.ui.aspect_ratio_checkbox.setChecked(True)
        self.ui.resample_combobox.setCurrentIndex(0)


    def aspect_ratio(self):
        print("state changed")
        if self.ui.aspect_ratio_checkbox.isChecked():
            print("checked")
            self.ui.height_text.setText("")
            # self.ui.height_text.setDisabled()
            self.ui.height_text.setReadOnly(True)
        else:
            print("unchecked")
            self.ui.height_text.setReadOnly(False)


    def resize_image(self):
        try:
            in_dir = self.ui.browse_text.text()
            in_height = self.ui.height_text.text()
            in_width = self.ui.width_text.text()
            in_resolution = self.ui.resolution_text.text()
            in_resample = self.ui.resample_combobox.currentIndex()

            if in_dir is not "":
                if os.path.isdir(in_dir):
                    if self.ui.aspect_ratio_checkbox.isChecked():
                        if in_width is not "":
                            for filename in os.listdir(in_dir):
                                if filename.lower().endswith(".png") \
                                        or filename.lower().endswith(".jpg") \
                                        or filename.lower().endswith(".jpeg") \
                                        or filename.lower().endswith(".tif") \
                                        or filename.lower().endswith(".tiff") \
                                        or filename.lower().endswith(".gif"):
                                    self.filestoprocess.append(os.path.join(in_dir, filename))
                                    continue
                                else:
                                    continue
                            if len(self.filestoprocess) > 0:
                                # Got all files to process, process in thread
                                self.myworker.process_args(self.filestoprocess, in_width, in_resolution, in_resample)
                                self.myworker.start()
                            else:
                                print("No files in selected directory")
                        else:
                            if in_width is "":
                                print("Width is empty")
                    else:
                        if in_width is not "" and in_height is not "":
                            for filename in os.listdir(in_dir):
                                if filename.lower().endswith(".png") \
                                        or filename.lower().endswith(".jpg") \
                                        or filename.lower().endswith(".jpeg") \
                                        or filename.lower().endswith(".tif") \
                                        or filename.lower().endswith(".tiff") \
                                        or filename.lower().endswith(".gif"):
                                    self.filestoprocess.append(os.path.join(in_dir, filename))
                                    continue
                                else:
                                    continue
                            if len(self.filestoprocess) > 0:
                                # Got all files to process, process in thread
                                print("2")
                                self.myworker.process_args2(self.filestoprocess, in_width, in_height, in_resolution,
                                                            in_resample)
                                self.myworker.start()
                            else:
                                print("No files in selected directory")
                        else:
                            if in_width is "":
                                print("Width is empty")
                            if in_height is "":
                                print("Height is empty")
                else:
                    print("Input directory does not exist")
            else:
                print("Input directory is empty")

        except Exception as erro:
            print(erro)


    # prompt before application exit, overidding the default closeEvent()
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class WorkerThread(QThread):
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

        self.filestoprocess = []
        self.in_width = 0
        self.in_height = 0
        self.in_resample = 0
        self.in_resolution = 0

    def process_args(self, files, width, resolution, resample):
        self.filestoprocess = files
        self.in_width = int(width)
        self.in_resolution = resolution
        self.in_resample = resample

    def process_args2(self, files, width, height, resolution, resample):
        self.filestoprocess = files
        self.in_width = int(width)
        self.in_height = int(height)
        self.in_resolution = resolution
        self.in_resample = resample

    def run(self):
        try:
            self.psapp = GetActiveObject("Photoshop.Application")
            # We don't want any Photoshop dialogs displayed during automated execution
            psDisplayNoDialogs = 3  # from enum PsDialogModes
            self.psapp.displayDialogs = psDisplayNoDialogs

            psAutomatic = 8  # from enum PsResampleMethod
            psPreserveDetails = 9  # from enum PsResampleMethod
            psBicubicSmoother = 6  # from enum PsResampleMethod
            psBicubicSharper = 5  # from enum PsResampleMethod
            psBicubicAutomatic = 7  # from enum PsResampleMethod
            psNearestNeighbor = 2  # from enum PsResampleMethod
            psBilinear = 3  # from enum PsResampleMethod

            psBicubic = 4  # from enum PsResampleMethod
            psNoResampling = 1  # from enum PsResampleMethod

            for file in self.filestoprocess:
                print("thread: " + file)
                docRef = self.psapp.Open(file)

                # if height is given, don't maintain aspect ratio
                if int(self.in_height) > 0:
                    docRef.ResizeImage(self.in_width, self.in_height, None, psAutomatic)
                    # time.sleep(3)

                # maintain aspect ratio
                else:
                    doc_width = docRef.Width
                    doc_height = docRef.Height
                    # maintain aspect ratio
                    new_height = (doc_height / doc_width) * self.in_width
                    docRef.ResizeImage(self.in_width, new_height, None, psAutomatic)

                docRef.Save()
                docRef.Close()
                # to prevent application busy COM error
                time.sleep(1)
        except Exception as thread_err:
            print(thread_err)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainUIClass()
    ui.show()
    app.exec_()

