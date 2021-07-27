import sys

from PyQt6.QtWidgets import QApplication

from jbwsl2 import MainWindow


def run():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    run()
