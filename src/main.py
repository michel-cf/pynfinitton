import logging
import os
import sys

import config_path
from PIL import Image, ImageDraw, ImageQt
from PySide2.QtCore import QTranslator, QLocale
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

import logic

import gui

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
    width = 128
    height = 128
    image = Image.new('RGB', (width, height))
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=(200, 200, 0))
    dc.rectangle((0, height // 2, width // 2, height), fill=(0, 100, 100))

    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load(QLocale(device_manager.locale), 'pynfinitton', '.', directory=os.path.join(path, 'resources', 'translations'))
    app.installTranslator(translator)

    window = gui.MainWindow(device_manager)
    window.resize(800, 600)
    window.show()

    tray_icon_menu = QMenu()
    tray_icon_menu_open_action = QAction("Open")
    tray_icon_menu.addAction(tray_icon_menu_open_action)
    tray_icon_menu_close_action = QAction("Close")
    tray_icon_menu.addAction(tray_icon_menu_close_action)

    icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(image)))
    tray_icon = QSystemTrayIcon(icon, window)
    tray_icon.setToolTip("Pynfinitton")
    tray_icon.setContextMenu(tray_icon_menu)
    tray_icon.show()

    sys.exit(app.exec_())

