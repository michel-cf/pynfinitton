from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QMenu, QAction

from . import mainWindow


class TrayIconMenu(QMenu):

    def __init__(self, gui_window: mainWindow.MainWindow):
        super().__init__(None)
        self._open_action = QAction(QCoreApplication.translate('tray_icon', 'Open'))
        self.addAction(self._open_action)
        self._settings_action = QAction(QCoreApplication.translate('tray_icon', 'Settings'))
        self.addAction(self._settings_action)
        self._close_action = QAction(QCoreApplication.translate('tray_icon', 'Close'))
        self.addAction(self._close_action)

