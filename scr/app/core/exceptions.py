class BaseError(Exception):
    """Базовое исключение приложения"""
    pass


class FileLoadError(BaseError):
    """Ошибка загрузки файла"""
    pass


class FileFormatError(FileLoadError):
    """Неподдерживаемый формат файла"""
    pass


class FileError(FileLoadError):
    """Файл поврежден или не может быть прочитан"""
    pass


class EmptyFileError(FileLoadError):
    """Файл не содержит данных"""
    pass


class AnalysisError(BaseError):
    """Ошибка при анализе данных"""
    pass