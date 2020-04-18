from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QMainWindow, QStatusBar, QLabel, QWidget

import logic


class MainWindow(QMainWindow):
    def __init__(self, device_manager: logic.DeviceManager):
        QMainWindow.__init__(self)
        self.setWindowTitle("Pynfinitton")

        self._device_manager = device_manager

        with open('resources/pynfinitton.stylesheet', 'r') as fh:
            self.setStyleSheet(fh.read())

        self.setCentralWidget(self.create_window())

        self.status_message = QLabel()
        self.status_message.setFixedWidth(350)
        self.status_message.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.setStatusBar(QStatusBar(self))
        self.statusBar().addPermanentWidget(self.status_message)

        self.check_device_state()

    def create_window(self):
        window = QWidget()

        return window

    def check_device_state(self):
        if self._device_manager.is_connected():
            if self._device_manager.is_active():
                self.status_message.setText(QCoreApplication.translate('device', 'Infinitton device is active'))
            else:
                self.status_message.setText(QCoreApplication.translate('device', 'Infinitton device connected'))
        else:
            self.status_message.setText(QCoreApplication.translate('device', 'Infinitton device not found'))
