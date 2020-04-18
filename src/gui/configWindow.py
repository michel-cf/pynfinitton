from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QCheckBox, QComboBox

import logic
from gui import mainWindow


class ConfigWindow(QDialog):
    # noinspection SpellCheckingInspection
    LOCALES = {
        'en': 'English',
        'nl': 'Nederlands'
    }

    def __init__(self, gui_window: mainWindow.MainWindow, device_manager: logic.DeviceManager):
        QDialog.__init__(self, gui_window)
        self.setModal(True)
        self.setWindowTitle(QCoreApplication.translate('configs', 'Configs', 'title'))
        self._device_manager = device_manager

        layout = QGridLayout()
        layout.addWidget(QLabel(QCoreApplication.translate('configs', 'Open on startup'), self), 0, 0)
        self._open_on_startup = QCheckBox(self)
        self._open_on_startup.setChecked(device_manager.open_on_start)
        self._open_on_startup.stateChanged.connect(self._open_on_startup_changed)
        layout.addWidget(self._open_on_startup, 0, 1)

        layout.addWidget(QLabel(QCoreApplication.translate('configs', 'Locale'), self), 1, 0)
        self._locale_select = QComboBox(self)
        self._locale_select.setToolTip(QCoreApplication.translate('configs', 'Restart required'))
        for locale_key, locale_value in ConfigWindow.LOCALES.items():
            self._locale_select.addItem(locale_value, userData=locale_key)
        self._locale_select.setCurrentIndex(self._locale_select.findData(device_manager.locale))
        self._locale_select.currentIndexChanged.connect(self._locale_changed)
        layout.addWidget(self._locale_select, 1, 1)

        self.setLayout(layout)

    def _open_on_startup_changed(self, state):
        self._device_manager.open_on_start = state == Qt.Checked

    def _locale_changed(self, index):
        self._device_manager.locale = self._locale_select.itemData(index)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
