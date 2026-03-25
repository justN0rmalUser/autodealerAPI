from dataclasses import dataclass
from ..exceptions.config_exceptions import IncompleteConfigurationError
import decimal
import json
from pathlib import Path
from typing import Self


@dataclass(frozen=True)
class DatabaseConfig:
    db_path: str = "C:\\Program Files (x86)\\AutoDealer\\AutoDealer\\Database\\AutoDealer.fdb"
    username: str = "SYSDBA"
    password: str = "masterkey"

    @classmethod
    def from_json(cls, path: Path | str, *, path_key: str, user_key: str, pass_key: str) -> Self:
        """Парсит значения для инициализации связи с базой данных

        Args:
            path (Path | str): Путь к конфиг-файлу 
            path_key (str): Ключ с расположением базы данных
            user_key (str): Ключ с именем взаимодействующего с БД пользователя
            pass_key (str): Ключ с паролем к пользователю

        Returns:
            config (DatabaseConfig): конфиг с найденными данными

        """

        def get_state(name, src: dict):
            if state := src.get(name):
                return str(state)
            else:
                for key in src:
                    if isinstance(src[key], dict):
                        state = get_state(name, src[key])
                        if state:
                            return state
            

        if not isinstance(path, Path):
            path = Path(path)

        with open(path, encoding="utf-8") as FILE:
            dict_cfg = json.load(fp=FILE)
        

        cfg = {
            path_key: get_state(path_key, dict_cfg),
            user_key: get_state(user_key, dict_cfg),
            pass_key: get_state(pass_key, dict_cfg)
        }
  
        err_data = [key for key in cfg if cfg[key] is None]
        if any(err_data):
            raise IncompleteConfigurationError(err_data)
        else:
            return cls(db_path=cfg[path_key], username=cfg[user_key], password=cfg[pass_key])