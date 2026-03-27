"""Модуль для подключения к базе данных и создания транзакций"""
import fdb 
from .transactions import Transaction
from autodealerAPI.config import DatabaseConfig


class Connection:
    """
    Класс для простого подключения к базе данных
    """
    def __init__(self, cfg: DatabaseConfig) -> None:
        self.__cfg = cfg
        self.__connect = self.__create_connect()
        

    def __create_connect(self) -> fdb.Connection:
        try:
            con = fdb.connect(
                dsn=self.__cfg.db_path, 
                user=self.__cfg.username,
                password=self.__cfg.password
            )
            con.begin()
        except (AttributeError, TypeError):
            raise # TODO ловля .begin обращения | логгирование
        except Exception as exc:
            print(type(exc))
            raise 
        else:
            # TODO логгирование
            return con


    def transaction(self, is_readonly: bool) -> Transaction:
        """Открытие транзакции, в контексте которой будут выполняться команды

        Args:
            is_readonly (bool): Пометка - будет ли транзакция "только для чтения" 

        Raises:
            ConnectionError: Выбрасывается при отсутствия подключения к бд как такового

        Returns:
            Transaction: Класс транзакции для взаимодействия с внутренними командами
        """
        if not self.__connect.closed:
            raise ConnectionError("Отсутствует подключение к основной базе данных")
        return Transaction(self.__connect, is_readonly)
