from PIL import Image
from PySide2.QtWidgets import QWidget, QPushButton, QFileDialog, QGridLayout, QScrollArea

from gui.icon_picker.widgets import drawWidget


class ImportTab(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        layout = QGridLayout()

        pan_zoom = QScrollArea()
        self._selection_area = drawWidget.DrawWidget(pan_zoom)

        pan_zoom.setWidget(self._selection_area)
        layout.addWidget(pan_zoom, 0, 0, 4, 1)

        self._import_button = QPushButton('Import icon', self, clicked=self._on_import_button_click)
        layout.addWidget(self._import_button, 0, 1, 1, 4)

        self._zoom_in_button = QPushButton('Zoom in', self, clicked=self._on_zoom_in_click)
        layout.addWidget(self._zoom_in_button, 1, 1, 1, 2)

        self._zoom_out_button = QPushButton('Zoom out', self, clicked=self._on_zoom_out_click)
        layout.addWidget(self._zoom_out_button, 1, 3, 1, 2)

        self.setLayout(layout)

    def _on_import_button_click(self):
        import_dialog = QFileDialog(self, 'Import icon')
        import_dialog.setFileMode(QFileDialog.ExistingFile)
        import_dialog.setNameFilter('Images (*.png *.jpg)')
        if import_dialog.exec():
            if len(import_dialog.selectedFiles()) == 1:
                self._import_file_name = import_dialog.selectedFiles()[0]

                self._image = Image.open(self._import_file_name)
                self._selection_area.set_image(self._image)

    def _on_zoom_in_click(self):
        self._selection_area.zoom_in()

    def _on_zoom_out_click(self):
        self._selection_area.zoom_out()

