from typing import Optional

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QMessageBox, QSplitter
)

from .widgets.analysis_panel import AnalysisPanel
from .widgets.data_table import DataTable
from .widgets.file_selector import FileSelector
from ..core.constants import CONFIG
from ..core.dataclasses import ExcelFileInfo, AnalysisResult
from ..core.exceptions import (
    FileLoadError, FileFormatError,
    FileError, EmptyFileError, AnalysisError
)
from ..modules.data_analyzer import DataAnalyzer
from ..modules.excel_loader import ExcelLoader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._current_file_info: Optional[ExcelFileInfo] = None
        self._current_analysis: Optional[AnalysisResult] = None
        self.excel_loader = ExcelLoader()
        self.data_analyzer = DataAnalyzer()
        self._setup_ui()
        self._connect_signals()
        self._apply_styles()
        self.setWindowTitle(CONFIG.name)
        self.resize(*CONFIG.window_size)

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        central_widget.setLayout(main_layout)
        control_panel = QHBoxLayout()
        self.file_selector = FileSelector()
        control_panel.addWidget(self.file_selector)
        main_layout.addLayout(control_panel)
        splitter = QSplitter(Qt.Horizontal)
        self.data_table = DataTable()
        splitter.addWidget(self.data_table)
        self.analysis_panel = AnalysisPanel()
        splitter.addWidget(self.analysis_panel)
        splitter.setSizes([int(self.width() * 0.7),
                           int(self.width() * 0.3)])

        main_layout.addWidget(splitter, 1)

    def _connect_signals(self):
        self.file_selector.file_selected.connect(self._on_file_selected)
        self.file_selector.headers_changed.connect(self._on_headers_changed)

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QTableWidget { 
                background-color: white; 
                alternate-background-color: #f9f9f9;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 4px;
                border: 1px solid #7f8c8d;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QLabel { padding: 2px; }
        """)

    @pyqtSlot(str, bool)
    def _on_file_selected(self, file_path: str, has_headers: bool):
        try:
            self.file_selector.set_enabled(False)
            file_info = self.excel_loader.load_file(file_path, has_headers)
            self._current_file_info = file_info
            rows, columns = self.data_table.load_data(file_info, has_headers)
            analysis_result = self.data_analyzer.analyze(file_info, has_headers)
            self._current_analysis = analysis_result
            self.analysis_panel.update_analysis(analysis_result)

        except (FileFormatError, EmptyFileError, FileError,
                FileLoadError, AnalysisError) as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            self._clear_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")
            self._clear_data()
        finally:
            self.file_selector.set_enabled(True)

    @pyqtSlot(bool)
    def _on_headers_changed(self, has_headers: bool):
        if self._current_file_info:
            file_path = self.file_selector.get_current_file()
            if file_path:
                self._on_file_selected(file_path, has_headers)

    def _clear_data(self):
        self._current_file_info = None
        self._current_analysis = None
        self.data_table.clear()
        self.analysis_panel._clear()