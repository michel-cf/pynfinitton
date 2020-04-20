import math

from PIL import Image, ImageDraw, ImageQt
from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtGui import QMouseEvent, QPaintEvent, QPainter, QPixmap
from PySide2.QtWidgets import QDialog, QGridLayout, QWidget


class DrawWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._image = Image.new('RGB', (72, 72))
        self._draw_image = ImageDraw.Draw(self._image)

    def mousePressEvent(self, event: QMouseEvent):
        x_relative = math.floor(event.x() / self.width() * 72)
        y_relative = math.floor(event.y() / self.height() * 72)

        self._draw_image.point((x_relative, y_relative), (255, 255, 0)) #, 100))
        print('%s:%s' % (x_relative, y_relative))

        self.update()

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.scale(self.width() / 72, self.height() / 72)
        painter.setPen(Qt.NoPen)

        pixmap = QPixmap()
        pixmap.convertFromImage(ImageQt.ImageQt(self._image))
        painter.drawPixmap(0, 0, 72, 72, pixmap)


class IconEditor(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(QCoreApplication.translate('icon-editor', 'Icon editor', 'title'))

        layout = QGridLayout()

        self._draw_widget = DrawWidget(self)
        self._draw_widget.setFixedSize(200, 200)
        layout.addWidget(self._draw_widget, 0, 0)

        self.setLayout(layout)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
