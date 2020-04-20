from typing import Optional

from PySide2.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from gui import iconEditor
import logic


class ActionWidget(QWidget):

    _icon_editor: Optional[iconEditor.IconEditor] = None

    def __init__(self, parent: QWidget, manager: logic.DeviceManager):
        QWidget.__init__(self)

        self._manager = manager
        self._key_task = None

        self._action_widget = QWidget(self)
        self._action_widget.hide()
        layout = QGridLayout()

        self._icon_button = QPushButton(self._action_widget, clicked=self._icon_clicked)
        self._icon_button.setFixedSize(72, 72)
        layout.addWidget(self._icon_button, 0, 0)

        self._title = QLabel(self._action_widget)
        layout.addWidget(self._title, 0, 1)

        layout.addWidget(QLabel('Name'), 1, 0)
        self._name = QLineEdit(self._action_widget)
        layout.addWidget(self._name, 1, 1)

        self._action_widget.setLayout(layout)

        layout_container = QHBoxLayout()
        layout_container.addWidget(self._action_widget)
        self.setLayout(layout_container)

    def select(self, key_index):
        if key_index is not None:
            self._title.setText('Key ' + str(key_index))

            self._key_task = self._manager.config_screen.get_key_task(key_index)
            if self._key_task is None:
                self._name.setText(self._manager.make_unique_task_name('Task'))
            else:
                self._name.setText(self._key_task.name)

            self._action_widget.show()
        else:
            self._action_widget.hide()

    def _icon_clicked(self):
        if ActionWidget._icon_editor is None:
            ActionWidget._icon_editor = iconEditor.IconEditor(None)

        ActionWidget._icon_editor.show()
