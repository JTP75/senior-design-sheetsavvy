import asyncio
import os.path

from PySide6.QtCore import QRunnable, QThreadPool
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QFileDialog

from src.gui.main_window import *


# pyside6-uic src/gui/sheetsavvy_main_window.ui -o src/gui/main_window.py

DEFAULT_SAVE_LOCATION = os.path.expanduser("~/Documents/SheetSavvyScores/")
ARCHIVE_LOCATION = "src/archive/"

class _AsyncWorker(QRunnable):
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
    def run(self):
        asyncio.run(self.coro)

class SheetSavvyUX(MainWindow,QMainWindow):

    threadpool: QThreadPool
    device_table_model: QStandardItemModel

    ready_to_save: bool

    si: any
    smg: any

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QPixmap(f"{ARCHIVE_LOCATION}musicxml_file.png"))
        self.save_file_image_label.setAlignment(Qt.AlignCenter)

        self.threadpool = QThreadPool()

        self.device_table_model = QStandardItemModel()
        self.device_info_list.setModel(self.device_table_model)
        self.update_device_table(False, "NA", "NA")
        self.gridLayout.setColumnStretch(0,200)
        self.gridLayout.setColumnStretch(1,200)
        self.link_buttons()

        self.set_ready_to_save(False)

        self.si = None
        self.smg = None

    def link_buttons(self):
        self.reset_button.clicked.connect(self.click_reset_button)
        self.save_button.clicked.connect(self.click_save_as_button)

    # update elements #

    def update_device_table(self, is_connected: bool, status: str, port: str):
        title_text = "Device" if is_connected else "Device (Disconnected)"
        port_text = f"Port: {port}"
        status_text = f"Status: {status}"
        self.device_table_model.setRowCount(3)
        self.device_table_model.setColumnCount(1)
        self.device_table_model.setItem(0,0,QStandardItem(title_text))
        self.device_table_model.setItem(1,0,QStandardItem(port_text))
        self.device_table_model.setItem(2,0,QStandardItem(status_text))

    def set_ready_to_save(self, ready: bool):
        self.ready_to_save = ready
        self.save_button.setEnabled(ready)
        pm = QPixmap(f"{ARCHIVE_LOCATION}musicxml_file.png") if ready else QPixmap(f"{ARCHIVE_LOCATION}musicxml_file_closed.png")
        self.save_file_image_label.setPixmap(pm.scaled(120, 120, Qt.KeepAspectRatio))

    # ui button linking #

    def click_reset_button(self):
        if not self.si: return
        port_found = self.si.check_com_list()
        if port_found:
            worker = _AsyncWorker(self.si.read_in_serial())
            self.threadpool.start(worker)
        else:
            self.update_device_table(False,"N/A", "N/A")

    def click_save_as_button(self):
        file_name,_ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            DEFAULT_SAVE_LOCATION,
            "XML Files (*.xml);;MusicXML Files (*.musicxml)"
        )
        if file_name:
            self.smg.save_as(file_name)

    # backend calls #

    def send_ready_to_save(self, ready: bool):
        self.set_ready_to_save(ready)
        self.update_device_table(True,"Idle", self.si.port)

    def send_device_state(self, state: str):
        if state == "disconnected":
            self.update_device_table(False, "N/A", "N/A")
        elif state == "idle":
            self.update_device_table(True, "Idle", self.si.port)
        elif state == "countoff":
            self.update_device_table(True, "Counting off...", self.si.port)
        elif state == "recording":
            self.update_device_table(True, "Recording...", self.si.port)
        elif state == "sending":
            self.update_device_table(True, "Sending data...", self.si.port)