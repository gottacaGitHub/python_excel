from abc import ABC, abstractmethod
from typing import List, Any
from ..core.dataclasses import ExcelFileInfo


class AbstractExcelLoader(ABC):
    """Загрузчик Excel"""

    @abstractmethod
    def load_file(self, file_path: str, has_headers: bool = True) -> ExcelFileInfo:
        """
        Загружает файл

        Args:
            file_path: Путь к файлу
            has_headers: заголовки в первой строке

        Returns:
            ExcelFileInfo: Информация о файле

        Raises:
            FileLoadError: Если файл не загружен
        """
        pass

    @staticmethod
    def validate_file_ext(file_path: str, allow_ext: List[str]) -> bool:
        """
        Проверяет расширение

        Args:
            file_path: Путь к файлу
            allow_ext: Список расширений

        Returns:
            bool: True если допустимо
        """
        return any(file_path.lower().endswith(ext.replace('*', ''))
                   for ext in allow_ext)

    @staticmethod
    def extract_value(cell_value: Any) -> Any:
        """
        Извлекает значение из ячейки и проверяет их

        Args:
            cell_value: Значение ячейки

        Returns:
            Проверенное значение
        """
        if (isinstance(cell_value, str) and not cell_value.strip()) or cell_value is None:
            return ""
        return cell_value