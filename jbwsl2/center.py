import os
import re
from typing import Optional

from PyQt6 import QtCore
from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from jbwsl2.header import HeaderWidget
from jbwsl2.overview import OverviewWidget


class CentralWidget(QWidget):
    files = []
    watching = False
    tmp_path = None
    project_path = None
    watcher = None

    def __init__(self, project_path: Optional[str], tmp_path: Optional[str]):
        super().__init__()

        self.set_project_path(project_path)
        self.set_tmp_path(tmp_path)
        self.watcher = QFileSystemWatcher()

        self.overview = OverviewWidget()

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(HeaderWidget(self.project_path, self.tmp_path, self.set_project_path, self.set_tmp_path), 0)
        layout.addWidget(self.overview, 1)

        self.setLayout(layout)

        self.watch()

    def set_project_path(self, path: str):
        if path is None:
            return

        self.project_path = path
        self.watch()

    def set_tmp_path(self, path: str):
        if path is None:
            return

        self.tmp_path = path
        self.watch()

    def watch(self):
        if self.tmp_path is None or self.project_path is None or self.watcher is None:
            return

        self.watcher.removePaths(self.watcher.directories())
        self.watcher.addPath(self.tmp_path)
        self.watcher.directoryChanged.connect(self.on_file_change)

        self.overview.set_input("Listening...\n")

    @QtCore.pyqtSlot(str)
    def on_file_change(self, file: str):
        latest_file = max([os.path.join(file, basename) for basename in os.listdir(self.tmp_path)],
                          key=os.path.getctime)

        attempt = 0

        if latest_file in self.files:
            return

        self.files.append(latest_file)

        self.overview.set_input("{}New file: {}...\n".format(self.overview.input.toPlainText(), latest_file))
        invalid_path_component = self.project_path.replace('\\', '/')

        while attempt < 3:
            try:
                f = open(latest_file, 'r+')
                content = f.read()

                match = re.search(r'(\"\/\/wsl[\$]*\/[a-zA-Z\- 0-9\.\:\/]*\")', content)
                if not match:
                    return

                # search for wrongly formatted path
                result = re.sub(r'(\$)\1+', r'\1', content)
                result = re.sub(
                    r'(\"\/\/wsl[\$]*\/[a-zA-Z\- 0-9\.\:\/]*\")',
                    lambda match: './{}'.format(match.group().replace('"', '').replace(invalid_path_component, '').lstrip('/')),
                    result
                )

                f.seek(0)
                f.write(result)
                f.truncate()
                f.close()

                self.overview.set_input("{}Invalid path detected: {}...\n".format(
                    self.overview.input.toPlainText(), match.group()
                ))

                self.overview.set_output(result)
                break
            except Exception as e:
                print(str(e))
                attempt += 1