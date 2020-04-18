import logging
import os
import sys

import config_path
from PySide2.QtCore import QTranslator, QLocale
from PySide2.QtWidgets import QApplication

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import  QSystemTrayIcon


import gui
import logic

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.DEBUG)

    # Set working directory to root
    # https://pythonhosted.org/PyInstaller/runtime-information.html#run-time-information
    if getattr(sys, 'frozen', False):
        # application_path = os.path.dirname(sys.executable)

        # noinspection PyProtectedMember,PyUnresolvedReferences,PyProtectedMember
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(__file__)

    path = os.path.abspath(application_path)
    os.chdir(application_path)

    configuration_file_path = config_path.ConfigPath('pynfinitton', 'creatingfuture.eu', '.ini')

    device_manager = logic.DeviceManager(configuration_file_path)

    # If graphical
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load(QLocale(device_manager.locale), 'pynfinitton', '.',
                    directory=os.path.join(path, 'resources', 'translations'))
    app.installTranslator(translator)

    window = gui.MainWindow(device_manager)
    window.resize(800, 600)
    if device_manager.open_on_start:
        window.show()

    tray_icon_menu = gui.TrayIconMenu(window)

    tray_icon = QSystemTrayIcon(QIcon('resources/ui/light/app_icon.png'), window)
    tray_icon.setToolTip("Pynfinitton")
    tray_icon.setContextMenu(tray_icon_menu)
    tray_icon.show()

    sys.exit(app.exec_())
