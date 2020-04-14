from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QStatusBar, QLabel


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Pynfinitton")

        with open('resources/pynfinitton.stylesheet', 'r') as fh:
            self.setStyleSheet(fh.read())

        self.setCentralWidget(widget)

        self.status_message = QLabel()
        self.status_message.setFixedWidth(200)
        self.status_message.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.status_message.setText("Infinitton device not found")

        self.setStatusBar(QStatusBar(self))
        self.statusBar().addPermanentWidget(self.status_message)
