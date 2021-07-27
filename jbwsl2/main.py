import argparse
import os
import re

from PyQt6.QtWidgets import QMainWindow

from jbwsl2.center import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        stylesheet = """
            QMainWindow {
                background-color: #FAF0CA;
            }
        """

        self.setWindowTitle("Jetbrains WSL2 invalid interpolation v1.0 by Cédric Le Varlet")
        self.setGeometry(0, 0, 1000, 800)

        self.setStyleSheet(stylesheet)

        params = self.get_parameters()
        self.setCentralWidget(CentralWidget(*params))

    def get_parameters(self):
        # retrieve variables
        self.parser = argparse.ArgumentParser(description='Run application')
        self.parser.add_argument('-p', '--project', type=str, default=None, help="""
        The path to your project
        """)
        self.parser.add_argument('-c', '--classpath', type=str, default=None, help="""
        If no tmp path is provided, the jetbrains classpath may be used to automatically determine the tmp path.
        """)
        self.parser.add_argument('-t', '--tmp', type=str, default=None, help="""
        The jetbrains tmp directory path. 
        Example: C:\\Users\\{user}\\AppData\\Local\\JetBrains\\IntelliJIdea{version}\\tmp
        """)

        args = self.parser.parse_args()

        if args.classpath is not None:
            return (
                args.project,
                os.path.join(
                    re.search(r'([A-Za-z]:\\[A-Za-z\\]*JetBrains\\[A-Za-z\.0-9]*)', args.classpath).group(0),
                    'tmp'
                )
            )

        return args.project, args.tmp
