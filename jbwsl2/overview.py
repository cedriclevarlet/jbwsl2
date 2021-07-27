from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout


class OverviewWidget(QWidget):
    def __init__(self):
        super().__init__()

        stylesheet = """
            QPlainTextEdit {
                border: 1px solid #FFF;
                border-radius: 10px;
                background-color: rgba(244,211,94,.4);
            }
        """

        self.input = QPlainTextEdit()
        self.output = QPlainTextEdit()

        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.output)

        self.setStyleSheet(stylesheet)

        self.setLayout(layout)

    def set_input(self, text: str):
        self.input.setPlainText(text)

    def set_output(self, text: str):
        self.output.setPlainText(text)