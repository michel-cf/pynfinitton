import os
import sys

import pystray
from PIL import Image, ImageDraw
from PySide2.QtWidgets import QApplication, QWidget

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


    def setup(taskbar_icon: pystray.Icon):
        taskbar_icon.visible = True

        app = QApplication(sys.argv)

        main_screen = QWidget()
        window = gui.MainWindow(main_screen)
        window.resize(800, 600)
        window.show()

        app.exec_()
        taskbar_icon.stop()

    width = 16
    height = 16
    image = Image.new('RGB', (width, height))
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=(200, 200, 0))
    dc.rectangle((0, height // 2, width // 2, height), fill=(0, 100, 100))

    icon = pystray.Icon('Pynfinitton')
    icon.icon = image
    icon.run(setup)
