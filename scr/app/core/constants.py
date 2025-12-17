import json
from pathlib import Path
from .dataclasses import AppConfig
from .exceptions import FileLoadError


def load_config(config_path: str = None) -> AppConfig:
    """
    Загружает конфигурацию из JSON файла
    """
    if config_path is None:
        current_dir = Path(__file__).parent.parent.parent.parent
        config_path = current_dir / "scr" / "config" / "settings.json"

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        return AppConfig(
            name=config_data["app"]["name"],
            default_font_size=config_data["app"]["default_font_size"],
            table_font_size=config_data["app"]["table_font_size"],
            max_recent_files=config_data["app"]["max_recent_files"],
            window_size=config_data["ui"]["window_size"],
            table_min_size=config_data["ui"]["table_min_size"],
            analysis_panel_width=config_data["ui"]["analysis_panel_width"],
            excel_ext=config_data["file_format"]["excel_ext"],
            has_headers=config_data["analysis"]["has_headers"],
            size_type_detect=config_data["analysis"]["size_type_detect"],
            date_formats=config_data["analysis"]["date_formats"]
        )
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        raise FileLoadError(f"Ошибка загрузки конфигурации: {str(e)}")


# Константы для удобства доступа
CONFIG = load_config()