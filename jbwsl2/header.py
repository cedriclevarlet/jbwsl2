import os
import webbrowser
from typing import Callable

from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QTextEdit, QFormLayout, QVBoxLayout, QFileDialog

import jbwsl2


class HeaderWidget(QWidget):
    callables = {}
    default_dir_label = 'Click to define...'
    module_path = os.path.dirname(jbwsl2.__file__)

    def __init__(self,
                 project_path: str, tmp_path: str,
                 on_project_change: Callable[[str], None],
                 on_tmp_change: Callable[[str], None]):
        super().__init__()

        # Load images
        QDir.addSearchPath('images', os.path.join(self.module_path, 'images'))

        # Hero
        title_container = QHBoxLayout()
        title = QLabel('Jetbrains WSL2 invalid interpolation fix v1.0')
        title.setObjectName('title')

        credits = QLabel('by Cédric Le Varlet')
        credits.mousePressEvent = self.open_browser
        credits.setObjectName('credits')
        credits.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        title_container.addWidget(title, 0)
        title_container.addWidget(credits, 0)
        title_container.addStretch()

        description = QTextEdit()
        description.insertHtml("""
<p>This tool aims to provide a temporary solution to IDEA-242051, It is provided as-is and does not come with any guarantee. Use this at your own risk!</p>
 
<p>
Instructions:<br/>
1. In the first input field, select the directory containing your docker-compose.yml file (<b>example: \\\\wsl$\\home\\john\\my-project\\</b>).<br/>
2. In the second input field, select Jetbrain's tmp directory. (<b>example: C:\\Users\\john\\AppData\\Local\\JetBrains\\IntelliJIdea2021.1\\tmp</b>)<br/>
3. You may now run application from within your editor.
</p> 

<p>Version 1.1 will include support for nested docker-compose files which are not in your project's base directory.</p>
""")
        description.setReadOnly(True)
        description.setObjectName('description')
        description.setFixedHeight(158)

        support_label = QLabel("If this was useful to you, please consider supporting me on Ko-fi!")

        support = QLabel()
        support_image = QPixmap('images:support.png')
        support.setPixmap(support_image)
        support.setObjectName('support')
        support.setScaledContents(True)
        support.mousePressEvent = self.open_browser
        support.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Config
        project_title = QLabel('Project directory:')
        project_title.setStyleSheet("""
            font-weight: bold;
        """)
        project_label = QLabel(project_path if project_path is not None else self.default_dir_label)
        project_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        project_label.setObjectName('project')

        tmp_title = QLabel('Jetbrains tmp dir: ')
        tmp_title.setAccessibleName('title')
        tmp_title.setStyleSheet("""
            font-weight: bold;
        """)
        tmp_label = QLabel(tmp_path if tmp_path is not None else self.default_dir_label)
        tmp_label.setObjectName('tmp')
        tmp_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Register events
        self.callables['tmp'] = on_tmp_change
        self.callables['project'] = on_project_change

        project_label.mousePressEvent = self.on_project_change
        tmp_label.mousePressEvent = self.on_tmp_change

        # Define layout
        table_layout = QFormLayout()
        table_layout.setSpacing(10)
        table_layout.addRow(project_title, project_label)
        table_layout.addRow(tmp_title, tmp_label)

        container = QVBoxLayout()
        container.addLayout(title_container)
        container.addWidget(description)
        container.addWidget(support_label, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        container.addWidget(support, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        container.addLayout(table_layout)

        self.setObjectName('header')
        self.setStyleSheet("""
            QFormLayout {
                border: 0 solid black;
                border-radius: 15px 15px 0 0;
                height: 100px;
                background: #FFF;
                padding: 10px 10px;
            }
            
            QLabel#title {
                font-weight:bold;
                font-weight: bold;
                font-size: 16pt;
            }
            
            QLabel#credits {
                background-color: #FFF;
                border-radius: 5px;
                padding: 5px;
            }
            
            QLabel#support {
                margin-bottom: 20px;
            }
            
            QTextEdit#description {
                padding-left: 20px;
                background-color: transparent;
                border: none;
                margin-top: 10px;
                margin-bottom: 20px;
            }
            
            QLabel#tmp, QLabel#project {
                font-weight: normal;
                padding: 10px;
                border-radius: 15px;
                background: #FFF url("images:folder.png") no-repeat;
                background-position: right center;
                background-origin: content;
            }
        """)

        self.project_label = project_label
        self.tmp_label = tmp_label

        self.setLayout(container)

    def open_browser(self, event):
        try:
            webbrowser.open('https://ko-fi.com/cedriclevarlet/')
        except:
            pass

    def on_tmp_change(self, event):
        directory = QFileDialog.getExistingDirectory(directory=os.path.join(
            os.environ.get('USERPROFILE'),
            'AppData',
            'Local',
            'JetBrains'
        ) if self.tmp_label.text() == self.default_dir_label else self.tmp_label.text())

        if not directory:
            return

        self.tmp_label.setText(directory)
        self.callables['tmp'](directory)

    def on_project_change(self, event):
        directory = QFileDialog.getExistingDirectory(
            directory=None if self.project_label.text() == self.default_dir_label else self.project_label.text())

        if not directory:
            return

        self.project_label.setText(directory)
        self.callables['project'](directory)
