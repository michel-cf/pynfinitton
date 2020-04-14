import os
import sys

from PIL import Image, ImageDraw, ImageQt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QAction

import gui

if __name__ == '__main__':

    # Set working directory to root
    # https://pythonhosted.org/PyInstaller/runtime-information.html#run-time-information
    if getattr(sys, 'frozen', False):
        # application_path = os.path.dirname(sys.executable)

        # noinspection PyProtectedMember,PyUnresolvedReferences,PyProtectedMember
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(__file__)

    os.chdir(application_path)

    width = 128
    height = 128
    image = Image.new('RGB', (width, height))
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=(200, 200, 0))
    dc.rectangle((0, height // 2, width // 2, height), fill=(0, 100, 100))

    app = QApplication(sys.argv)

    main_screen = QWidget()
    window = gui.MainWindow(main_screen)
    window.resize(800, 600)
    window.show()

    tray_icon_menu = QMenu()
    tray_icon_menu_open_action = QAction("Open")
    tray_icon_menu.addAction(tray_icon_menu_open_action)

    icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(image)))
    tray_icon = QSystemTrayIcon(icon, window)
    tray_icon.setToolTip("Pynfinitton")
    tray_icon.setContextMenu(tray_icon_menu)
    tray_icon.show()

    sys.exit(app.exec_())

