"""Модуль для подключения к базе данных и создания транзакций"""
import fdb 
from .transactions import Transaction
from autodealerAPI.config import DatabaseConfig
from typing import Literal, overload, TYPE_CHECKING
from .transactions import TransactionSession, TransactionHigh, TransactionLow, TransactionBasic


class Connection:
    """
    Класс для простого подключения к базе данных
    """
    def __init__(self, config: DatabaseConfig) -> None:
        self.__cfg = config
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


    def transaction(self) -> Transaction:
        """Открытие транзакции, в контексте которой будут выполняться команды

        Raises:
            ConnectionError: Выбрасывается при отсутствия подключения к бд как такового

        Returns:
            Transaction: Класс транзакции для взаимодействия с внутренними командами
        """
        if not self.__connect.closed:
            raise ConnectionError("Отсутствует подключение к основной базе данных")
        return Transaction(self.__connect)
    
    
    @overload
    def single_transaction(self, *, type_api: Literal["high"], read_only: bool = False) -> TransactionSession[TransactionHigh]: ...
    @overload
    def single_transaction(self, *, type_api: Literal["low"], read_only: bool = False) -> TransactionSession[TransactionLow]: ...
    @overload
    def single_transaction(self, *, type_api: Literal["basic"], read_only: bool = False) -> TransactionSession[TransactionBasic]: ...
    
    def single_transaction(self, *, type_api: Literal["high", "low", "basic"], read_only: bool = False) -> TransactionSession:
        """Открытие транзакции "из коробки"

        Args:
            type_api (Literal[&quot;high&quot;, &quot;low&quot;]): Уровень взаимодействия с бд
            read_only (bool, optional): Тип транзакции. По умолчанию False.

        Returns:
            Контекстный менеджер
        """
        tr = Transaction(self.__connect)
        if type_api == "high":
            return tr.start_transaction(type_api="high", read_only=read_only)
        if type_api == "low":
            return tr.start_transaction(type_api="low", read_only=read_only)
        if type_api == "basic":
            return tr.start_transaction(type_api="basic", read_only=read_only)    
