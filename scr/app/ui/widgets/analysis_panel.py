from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QGroupBox
)
from PyQt5.QtCore import Qt
from ...core.dataclasses import AnalysisResult, ColumnType


class AnalysisPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._clear()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(2, 2, 2, 2)
        self.summary_label = QLabel("Выберите файл")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(self.summary_label)
        self.analysis_table = QTableWidget()
        self.analysis_table.setColumnCount(5)
        self.analysis_table.setHorizontalHeaderLabels([
            "Столбец", "Тип", "Пустых", "Min", "Mean"
        ])
        self.analysis_table.horizontalHeader().setStretchLastSection(True)
        self.analysis_table.verticalHeader().setVisible(False)
        self.analysis_table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.analysis_table, 1)

        self.setLayout(layout)

    def update_analysis(self, analysis_result: AnalysisResult):
        summary = f"{analysis_result.file_name}\n"
        summary += f"Строк: {analysis_result.data_rows_count}, "
        summary += f"Столбцов: {analysis_result.count_column}"

        if analysis_result.has_headers:
            summary += " (с заголовками)"

        self.summary_label.setText(summary)
        stats = analysis_result.statistic
        self.analysis_table.setRowCount(len(stats))

        for i, stat in enumerate(stats):
            name_item = QTableWidgetItem(stat.name[:20] + ("..." if len(stat.name) > 20 else ""))
            name_item.setToolTip(stat.name)
            self.analysis_table.setItem(i, 0, name_item)
            type_item = QTableWidgetItem(stat.column_type.value)
            self.analysis_table.setItem(i, 1, type_item)
            empty_item = QTableWidgetItem(str(stat.empty_count))
            if stat.empty_count > 0:
                empty_item.setForeground(Qt.red)
            self.analysis_table.setItem(i, 2, empty_item)
            if stat.column_type in [ColumnType.INTEGER, ColumnType.FLOAT]:
                min_item = QTableWidgetItem(
                    f"{stat.min_value:.2f}" if stat.min_value is not None else "-"
                )
                self.analysis_table.setItem(i, 3, min_item)
                mean_item = QTableWidgetItem(
                    f"{stat.mean_value:.2f}" if stat.mean_value is not None else "-"
                )
                self.analysis_table.setItem(i, 4, mean_item)
            else:
                for col in [3, 4]:
                    self.analysis_table.setItem(i, col, QTableWidgetItem("-"))
        self.analysis_table.resizeColumnsToContents()

    def _clear(self):
        self.summary_label.setText("Выберите файл")
        self.analysis_table.setRowCount(0)