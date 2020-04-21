
from PySide2.QtWidgets import QGridLayout, QWidget

from .widgets import drawWidget


class IconEditor(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        layout = QGridLayout()

        self._draw_widget = drawWidget.DrawWidget(self)
        self._draw_widget.setFixedSize(200, 200)
        layout.addWidget(self._draw_widget, 0, 0)

        self.setLayout(layout)
