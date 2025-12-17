import re
from datetime import datetime
from typing import Any, List, Set
from collections import Counter
from ..core.dataclasses import ColumnType
from ..core.constants import CONFIG


class TypeDetector:
    """Детектор типов данных в столбцах"""

    INTEGER_REGEX = re.compile(r'^-?\d+$')
    FLOAT_REGEX = re.compile(r'^-?\d+\.\d+$')

    def __init__(self, date_formats: List[str] = None):
        self.date_formats = date_formats or CONFIG.date_formats

    def detect_column_type(self, column_data: List[Any]) -> ColumnType:
        """
        Определяет тип данных
        Если встречается хотя бы два разных типа (не считая пустых) - возвращает MIXED.

        Args:
            column_data: Список значений

        Returns:
            ColumnType: Тип
        """
        if not column_data:
            return ColumnType.EMPTY

        size = min(CONFIG.size_type_detect, len(column_data))
        column = column_data[:size]

        unique_types: Set[ColumnType] = set()

        for cell in column:
            cell_type = self._detect_cell_type(cell)
            if cell_type != ColumnType.EMPTY:
                unique_types.add(cell_type)

        if not unique_types:
            return ColumnType.EMPTY
        elif len(unique_types) == 1:
            return next(iter(unique_types))
        else:
            return ColumnType.MIXED

    def _detect_cell_type(self, cell_value: Any) -> ColumnType:
        """
        Определяет тип данных в ячейке

        Args:
            cell_value: Значение ячейки

        Returns:
            ColumnType: Тип данных ячейки
        """
        if cell_value is None or cell_value == "":
            return ColumnType.EMPTY

        if isinstance(cell_value, bool):
            return ColumnType.BOOLEAN

        if isinstance(cell_value, (int, float)):
            if isinstance(cell_value, int):
                return ColumnType.INTEGER
            elif isinstance(cell_value, float):
                return ColumnType.FLOAT

        if isinstance(cell_value, str):
            return ColumnType.STRING

        if isinstance(cell_value, datetime):
            return ColumnType.DATETIME

        return ColumnType.UNKNOWN


    def is_numeric_type(self, column_type: ColumnType) -> bool:
        """
        Проверяет, является ли тип числовым

        Args:
            column_type: Тип столбца

        Returns:
            bool: True если числовой тип
        """
        return column_type in (ColumnType.INTEGER, ColumnType.FLOAT)

    def can_calculate_statistics(self, column_type: ColumnType) -> bool:
        """
        Проверяет, можно ли рассчитать статистику для типа столбца

        Args:
            column_type: Тип столбца

        Returns:
            bool: True если можно рассчитать min/max/mean
        """
        return column_type in (ColumnType.INTEGER, ColumnType.FLOAT)