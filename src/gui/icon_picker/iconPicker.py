import os

from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QDialog, QGridLayout, QVBoxLayout, QTabWidget

from . import iconPickTab, iconEditor


class IconPicker(QDialog):

    def __init__(self, parent, icon_path):
        QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(QCoreApplication.translate('icon-picker', 'Icon picker', 'title'))
        self.setFixedWidth(75 * 8 + 44)

        if not os.path.exists(icon_path) or not os.path.isdir(icon_path):
            os.mkdir(icon_path)
            if not os.path.exists(icon_path) or not os.path.isdir(icon_path):
                raise IOError('Icon folder not available')

        self._icon_path = icon_path

        self._icon_pick_tab_user = iconPickTab.IconPickTab(self, icon_path)
        self._icon_pick_tab_built_in = iconPickTab.IconPickTab(self, os.path.join(os.getcwd(), 'resources', 'icons'),
                                                               False)
        self._icon_editor_tab = iconEditor.IconEditor(self)

        layout = QVBoxLayout()
        tabs = QTabWidget(self)
        tabs.addTab(self._icon_pick_tab_user, 'Icon picker')
        tabs.addTab(self._icon_pick_tab_built_in, 'Built in icons')
        tabs.addTab(self._icon_editor_tab, 'Icon editor')

        layout.addWidget(tabs)
        self.setLayout(layout)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
