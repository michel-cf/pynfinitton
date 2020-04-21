import math
import os

from PIL import Image, ImageQt
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget


class IconGridWidget(QWidget):

    def __init__(self, parent, icons_path, icon_width_count: int = 8):
        QWidget.__init__(self, parent)

        self.setFixedWidth(75 * icon_width_count)

        self._icons_path = icons_path
        self._icon_width_count = icon_width_count

    def set_icons_path(self, icons_path):
        self._icons_path = icons_path

    def paintEvent(self, event: QtGui.QPaintEvent):
        print('paint')
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)

        icon_number = 0
        for icon in os.listdir(self._icons_path):
            icon = os.path.join(self._icons_path, icon)
            if os.path.isfile(icon):
                pixmap = QtGui.QPixmap()
                image = Image.open(icon)
                pixmap.convertFromImage(ImageQt.ImageQt(image.resize((72, 72))))
                x = (icon_number % self._icon_width_count) * 75 + 1
                y = math.floor(icon_number / self._icon_width_count) * 75 + 1

                painter.drawPixmap(x, y, 72, 72,
                                   pixmap, 0, 0, 72, 72)

                icon_number += 1
