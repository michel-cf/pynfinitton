import math
from typing import Optional, Tuple

from PIL import Image, ImageQt,ImageDraw
from PySide2 import QtGui
from PySide2.QtCore import Qt, QRect
from PySide2.QtWidgets import QWidget


class DrawWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._image: Optional[Image.Image] = None
        self._working_image: Optional[Image.Image] = None

        self._zoom = 1.0

    # For testing only
    def mousePressEvent(self, event: QtGui.QMouseEvent):
        pos_real = self.convert_to_real((event.x(), event.y()))

        draw_image = ImageDraw.ImageDraw(self._working_image)
        draw_image.point(pos_real, (255, 0, 0, 255))
        print('Mouse press %s:%s' % pos_real)

        self.update()

    def convert_to_real(self, xy: Tuple[int, int]) -> Tuple[int, int]:
        return math.floor(xy[0] / self._zoom), math.floor(xy[1] / self._zoom)

    def zoom_in(self):
        self._zoom *= 1.25
        self._zoomed()

    def zoom_out(self):
        self._zoom *= 0.8
        self._zoomed()

    def zoom(self) -> float:
        return self._zoom

    def set_image(self, image: Image.Image):
        self._image = image
        if image is not None:
            print('Image size: %s:%s' % (image.width, image.height))
            self._working_image = Image.new('RGBA', image.size)
        self._zoomed()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self._image is None:
            painter.drawRect(0, 0, self.width(), self.height())
        else:
            rect = event.rect()
            # print('Draw image part %s:%s %s:%s' % (rect.x(), rect.y(), rect.width(), rect.height()))
            partial = self.__transform_for_paint(self._image, rect)
            working_partial = self.__transform_for_paint(self._working_image, rect)

            pixmap = QtGui.QPixmap()
            for x in range(0, rect.width(), 20):
                for y in range(0, rect.height(), 20):
                    block = partial.crop((x, y, x + 20, y + 20))
                    pixmap.convertFromImage(ImageQt.ImageQt(block))
                    painter.drawPixmap(rect.x() + x, rect.y() + y, pixmap)

                    working_block = working_partial.crop((x, y, x + 20, y + 20))
                    pixmap.convertFromImage(ImageQt.ImageQt(working_block))
                    painter.drawPixmap(rect.x() + x, rect.y() + y, pixmap)

    def __transform_for_paint(self, image: Image.Image, rect: QRect) -> Image.Image:
        return image.crop((rect.x() / self._zoom,
                           rect.y() / self._zoom,
                           (rect.x() + rect.width()) / self._zoom,
                           (rect.y() + rect.height()) / self._zoom)).resize((rect.width(), rect.height()))

    def _zoomed(self):
        self._zoom = round(self._zoom, 2)
        image = self._image
        if image is not None:
            self.setFixedSize(image.width * self._zoom, image.height * self._zoom)
