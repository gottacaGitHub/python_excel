from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict, Union
from enum import Enum


class ColumnType(Enum):
    """Типы данных столбцов"""
    INTEGER = "Целое число"
    FLOAT = "Дробное число"
    STRING = "Текст"
    DATETIME = "Дата/время"
    BOOLEAN = "Логический"
    EMPTY = "Пустой"
    MIXED = "Смешанный"
    UNKNOWN = "Неизвестный"


@dataclass
class ColumnStatistics:
    """Статистика по столбцу"""
    name: str
    column_type: ColumnType
    empty_count: int = 0
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    mean_value: Optional[float] = None
    count_row: int = 0


@dataclass
class AnalysisResult:
    """Результат анализа данных"""
    file_name: str
    sheet_name: str
    total_rows: int
    count_column: int
    has_headers: bool
    column_name: List[str] = field(default_factory=list)
    statistic: List[ColumnStatistics] = field(default_factory=list)

    @property
    def data_rows_count(self) -> int:
        """Количество строк с данными (без заголовка)"""
        if self.has_headers:
            return max(0, self.total_rows - 1)
        return self.total_rows


@dataclass
class ExcelFileInfo:
    """Информация о загруженном файле"""
    file_path: str
    file_name: str
    sheet_name: str
    headers: List[str]
    data: List[List[Any]]
    count_row: int
    count_column: int


@dataclass
class AppConfig:
    """Конфигурация приложения"""
    name: str
    default_font_size: int
    table_font_size: int
    max_recent_files: int
    window_size: List[int]
    table_min_size: List[int]
    analysis_panel_width: int
    excel_ext: List[str]
    has_headers: bool
    size_type_detect: int
    date_formats: List[str]
