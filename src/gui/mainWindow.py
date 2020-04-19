import functools
import math
from typing import List, Optional

from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtWidgets import QMainWindow, QStatusBar, QLabel, QWidget, QGridLayout, QPushButton, QHBoxLayout

import gui
import logic


class MainWindow(QMainWindow):
    def __init__(self, device_manager: logic.DeviceManager):
        QMainWindow.__init__(self)
        self.setWindowTitle("Pynfinitton")

        self._device_manager = device_manager
        self._keys: List[Optional[QPushButton]] = [None] * 15
        self._action_widget: Optional[gui.ActionWidget] = None

        with open('resources/pynfinitton.stylesheet', 'r') as fh:
            self.setStyleSheet(fh.read())

        self.setCentralWidget(self.create_window(self))

        self.status_message = QLabel()
        self.status_message.setFixedWidth(350)
        self.status_message.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.setStatusBar(QStatusBar(self))
        self.statusBar().addPermanentWidget(self.status_message)

        self.check_device_state()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def create_window(self, parent) -> QWidget:
        window = QWidget(parent)
        layout = QHBoxLayout()

        layout.addWidget(self.create_device_widget(window))

        self._action_widget = gui.ActionWidget(window, self._device_manager)
        layout.addWidget(self._action_widget)

        window.setLayout(layout)
        return window

    def create_device_widget(self, parent) -> QWidget:
        device_widget = QWidget(parent)
        layout = QGridLayout()
        for key_index in range(15):
            key_widget = QPushButton(str(key_index), device_widget,
                                     clicked=functools.partial(self._key_clicked, key_index))
            key_widget.setFixedSize(72, 72)
            self._keys[key_index] = key_widget
            layout.addWidget(key_widget, key_index % 5, math.floor(key_index / 5))

        device_widget.setLayout(layout)
        return device_widget

    def check_device_state(self):
        if self._device_manager.is_connected():
            if self._device_manager.is_active():
                self.status_message.setText(QCoreApplication.translate('device', 'Infinitton device is active'))
            else:
                self.status_message.setText(QCoreApplication.translate('device', 'Infinitton device connected'))
        else:
            self.status_message.setText(QCoreApplication.translate('device', 'Infinitton device not found'))

    def get_device_manager(self):
        return self._device_manager

    def _key_clicked(self, key_index):
        self._action_widget.select(key_index)
