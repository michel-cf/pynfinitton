from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog

from gui.icon_picker.widgets import iconGridWidget


class IconPickTab(QWidget):

    def __init__(self, parent, config_path, can_be_changed: bool = True):
        QWidget.__init__(self)

        layout = QVBoxLayout()

        self._config_path = config_path
        self._import_file_name = None

        self._icon_grid = iconGridWidget.IconGridWidget(self, config_path)
        self._icon_grid.setMinimumHeight(200)
        layout.addWidget(self._icon_grid)

        if can_be_changed:
            self._import_button = QPushButton('Import icon', self, clicked=self._on_import_button_click)
            layout.addWidget(self._import_button)

        self.setLayout(layout)

    def _on_import_button_click(self):
        import_dialog = QFileDialog(self, 'Import icon')
        import_dialog.setFileMode(QFileDialog.ExistingFile)
        import_dialog.setNameFilter('Images (*.png *.jpg)')
        if import_dialog.exec():
            if len(import_dialog.selectedFiles()) == 0:
                self._import_file_name = import_dialog.selectedFiles()[0]

