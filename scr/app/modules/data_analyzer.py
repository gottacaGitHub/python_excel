import statistics
from typing import List, Any

from .types import TypeDetector
from ..core.dataclasses import AnalysisResult, ColumnStatistics, ColumnType, ExcelFileInfo
from ..core.exceptions import AnalysisError


class DataAnalyzer:
    """Анализатор данных Excel файлов"""

    def __init__(self):
        self.type_detector = TypeDetector()

    def analyze(self, file_info: ExcelFileInfo, has_headers: bool = True) -> AnalysisResult:
        """
        Анализирует данные из Excel файла

        Args:
            file_info: Информация о файле
            has_headers: Первую строка как заголовки

        Returns:
            AnalysisResult: Результаты анализа
        """
        try:
            if has_headers:
                data_row = file_info.data
                headers = file_info.headers
            else:
                data_row = file_info.data
                headers = [f"Column_{i+1}" for i in range(file_info.count_column)]

            if not data_row:
                return AnalysisResult(
                    file_name=file_info.file_name,
                    sheet_name=file_info.sheet_name,
                    total_rows=0,
                    count_column=0,
                    has_headers=has_headers,
                    column_name=headers
                )

            trans_data = self._transpose_data(data_row, file_info.count_column)

            statistic_list = []
            for i, (header, column_values) in enumerate(zip(headers, trans_data)):
                column_stats = self._analyze_column(header, column_values)
                statistic_list.append(column_stats)

            return AnalysisResult(
                file_name=file_info.file_name,
                sheet_name=file_info.sheet_name,
                total_rows=file_info.count_row,
                count_column=file_info.count_column,
                has_headers=has_headers,
                column_name=headers,
                statistic=statistic_list
            )

        except Exception as e:
            raise AnalysisError(f"Ошибка при анализе данных: {str(e)}")

    def _transpose_data(self, data: List[List[Any]], num_column: int) -> List[List[Any]]:
        """
        Транспонирует данные для анализа по столбцам

        Args:
            data: Список строк
            num_column: Количество столбцов

        Returns:
            List[List[Any]]: Данные по столбцам
        """
        column = [[] for _ in range(num_column)]

        for row in data:
            for i in range(num_column):
                if i < len(row):
                    column[i].append(row[i])
                else:
                    column[i].append("")

        return column

    def _analyze_column(self, column_name: str, column_data: List[Any]) -> ColumnStatistics:
        """
        Анализирует столбец

        Args:
            column_name: Имя столбца
            column_data: Данные столбца

        Returns:
            ColumnStatistics: Статистика по столбцу
        """
        column_type = self.type_detector.detect_column_type(column_data)
        empty_count = sum(1 for value in column_data
                          if value is None or value == "")

        stats = ColumnStatistics(
            name=column_name,
            column_type=column_type,
            empty_count=empty_count,
            count_row=len(column_data) - empty_count
        )

        if self.type_detector.is_numeric_type(column_type):
            numeric_values = self._extract_numeric_values(column_data, column_type)
            if numeric_values:
                try:
                    stats.min_value = min(numeric_values)
                    stats.max_value = max(numeric_values)
                    stats.mean_value = statistics.mean(numeric_values)
                except (ValueError, TypeError):
                    pass

        return stats

    def _extract_numeric_values(self, column_data: List[Any], column_type: ColumnType) -> List[float]:
        """
        Извлекает числа из столбца

        Args:
            column_data: Данные столбца
            column_type: Тип столбца

        Returns:
            List[float]: Список числовых значений
        """
        numeric_values = []

        if not self.type_detector.is_numeric_type(column_type):
            return numeric_values

        for value in column_data:
            if value is None or value == "":
                continue

            try:
                if column_type == ColumnType.INTEGER:
                    numeric_values.append(int(float(value)))
                elif column_type == ColumnType.FLOAT:
                    numeric_values.append(float(value))
            except (ValueError, TypeError):
                continue

        return numeric_values

    def get_analyze(self, analysis_result: AnalysisResult) -> str:
        """
        Данные файла

        Args:
            analysis_result: Результат анализа

        Returns:
            str: данные по файлу
        """
        return (f"Файл: {analysis_result.file_name}\n"
                f"Лист: {analysis_result.sheet_name}\n"
                f"Строк с данными: {analysis_result.total_rows}\n"
                f"Столбцов: {analysis_result.count_column}")