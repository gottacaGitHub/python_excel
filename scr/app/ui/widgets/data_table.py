from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from ...core.dataclasses import ExcelFileInfo


class DataTable(QTableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_file_info = None
        self._setup_ui()

    def _setup_ui(self):
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setVisible(False)

    def load_data(self, file_info: ExcelFileInfo, has_headers: bool = True):
        self.clear()
        self._current_file_info = file_info

        if has_headers:
            data_rows = file_info.data
            headers = file_info.headers
        else:
            data_rows = file_info.data
            headers = []
        self.setRowCount(len(data_rows))
        self.setColumnCount(len(headers) if headers else
                            (max(len(row) for row in data_rows) if data_rows else 0))
        if headers:
            self.setHorizontalHeaderLabels(headers)
        else:
            self.setHorizontalHeaderLabels(
                [f"Col {i+1}" for i in range(self.columnCount())]
            )
        for row_idx, row_data in enumerate(data_rows):
            for col_idx, cell_value in enumerate(row_data):
                if col_idx < self.columnCount():
                    item = QTableWidgetItem(str(cell_value) if cell_value else "")
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.setItem(row_idx, col_idx, item)
        self.resizeColumnsToContents()

        return self.rowCount(), self.columnCount()

    def clear(self):
        """Очистка таблицы"""
        self.setRowCount(0)
        self.setColumnCount(0)
        self._current_file_info = None