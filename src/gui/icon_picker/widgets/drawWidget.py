import math

from PIL import Image, ImageDraw, ImageQt
from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget


class DrawWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._image = Image.new('RGB', (72, 72))
        self._draw_image = ImageDraw.Draw(self._image)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        x_relative = math.floor(event.x() / self.width() * 72)
        y_relative = math.floor(event.y() / self.height() * 72)

        self._draw_image.point((x_relative, y_relative), (255, 255, 0))
        print('%s:%s' % (x_relative, y_relative))

        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.scale(self.width() / 72, self.height() / 72)
        painter.setPen(Qt.NoPen)

        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(ImageQt.ImageQt(self._image))
        painter.drawPixmap(0, 0, 72, 72, pixmap)
