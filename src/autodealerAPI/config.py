import json
import logging
import logging.handlers
from configparser import ConfigParser
from pathlib import Path

from pydantic import BaseModel

from .exceptions.config_exceptions import IncompleteConfigurationError

__all__ = [
    "DatabaseConfig",
    "setup_logging"
]


def _find_value(key: str, data: dict) -> str | None:
    if key in data:
        value = data[key]
        if isinstance(value, str):
            return value.strip()
        elif isinstance(value, (int, float, bool)):
            return str(value)
    for v in data.values():
        if isinstance(v, dict):
            result = _find_value(key, v)
            if result:
                return result


def _get_config(cfg: dict, *, path_key: str, user_key: str, pass_key: str):
    config_data: dict[str, str | None] = {
        'db_path': _find_value(path_key, cfg),
        'username': _find_value(user_key, cfg),
        'password': _find_value(pass_key, cfg)
    }

    missing_keys = [k for k, v in config_data.items() if v is None]
    if missing_keys:
        raise IncompleteConfigurationError(missing_keys)
    return config_data


class DatabaseConfig(BaseModel):
    db_path: str
    username: str
    password: str

    @classmethod
    def from_json(
        cls,
        path: Path | str,
        *,
        path_key: str,
        user_key: str,
        pass_key: str
    ) -> 'DatabaseConfig':

        # Инициализация и алгоритм поиска
        path = Path(path)
        with open(path, encoding="utf-8") as f:
            dict_cfg = json.load(f)

        config_data = _get_config(
            dict_cfg,
            path_key=path_key,
            user_key=user_key,
            pass_key=pass_key
        )

        return cls(**config_data)  # pyright: ignore[reportArgumentType]

    @classmethod
    def from_ini(
        cls,
        path: Path | str,
        *,
        path_key: str,
        user_key: str,
        pass_key: str
    ) -> 'DatabaseConfig':

        # Инициализация и алгоритм поиска
        raw_cfg = ConfigParser()
        raw_cfg.read(path)
        dict_cfg = {section: dict(raw_cfg.items(section)) for section in raw_cfg.sections()}

        config_data = _get_config(
            dict_cfg,
            path_key=path_key,
            user_key=user_key,
            pass_key=pass_key
        )

        return cls(**config_data)  # pyright: ignore[reportArgumentType]

    def __init__(
        self,
        db_path: str = "C:\\Program Files (x86)\\AutoDealer\\AutoDealer\\Database\\AutoDealer.fdb",  # ignore = E501
        username: str = "SYSDBA",
        password: str = "masterkey"
    ):
        super().__init__(db_path=db_path, username=username, password=password)


def setup_logging(
    log_file: str | Path,
    level: int = logging.DEBUG
):
    filepath = Path(log_file) if not isinstance(log_file, Path) else log_file

    if filepath.suffix != ".log":
        raise FileNotFoundError(f"Суффикс не подходит: {filepath.suffix}")
    if not filepath.exists():
        filepath.touch()


    formatter = logging.Formatter(
        fmt="[%(asctime)s] <%(name)s>: %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.handlers.RotatingFileHandler(
        filename=filepath,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    lib_logger = logging.getLogger("autodealerAPI")
    lib_logger.setLevel(level)
    lib_logger.addHandler(file_handler)
    lib_logger.propagate = False  # ⬅️ ключевая строка
