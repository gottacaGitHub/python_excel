from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton,
    QCheckBox, QFileDialog
)

from ...core.constants import CONFIG


class FileSelector(QWidget):

    file_selected = pyqtSignal(str, bool)
    headers_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_file = None
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(8)
        self.select_btn = QPushButton("Выбрать файл")
        self.select_btn.setFixedWidth(140)
        self.headers_checkbox = QCheckBox("Заголовки в первой строке")
        self.headers_checkbox.setChecked(CONFIG.has_headers)
        layout.addWidget(self.select_btn)
        layout.addStretch(1)
        layout.addWidget(self.headers_checkbox)
        self.setLayout(layout)

    def _connect_signals(self):
        self.select_btn.clicked.connect(self._select_file)
        self.headers_checkbox.toggled.connect(self.headers_changed)

    def _select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите Excel файл",
            "",
            "Excel файлы (*.xlsx *.xls)"
        )

        if file_path:
            self.file_selected.emit(file_path,
                                    self.headers_checkbox.isChecked())

    def set_enabled(self, enabled: bool):
        self.select_btn.setEnabled(enabled)
        self.headers_checkbox.setEnabled(enabled)

    def get_current_file(self):
        return self._current_file