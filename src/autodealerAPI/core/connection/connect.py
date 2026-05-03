"""Модуль для подключения к базе данных и создания транзакций"""
from typing import Literal, overload
import logging
from contextlib import contextmanager

import fdb

from autodealerAPI.config import DatabaseConfig

from .transactions import (
    Transaction,
    TransactionBasic,
    TransactionHigh,
    TransactionLow,
    TransactionSession,
)


logger = logging.getLogger(__name__)


class Connection:
    """
    Класс для простого подключения к базе данных
    """
    def __init__(self, config: DatabaseConfig) -> None:
        logger.debug(f"Инициализация экземпляра объекта <{self.__class__.__name__}>")
        self.__cfg = config
        self.__connect = self.__create_connect()

    def __create_connect(self) -> fdb.Connection:
        logger.debug("Старт функции <__create_connect>")
        
        logger.info("Подключение к базе данных.")
        try:
            con = fdb.connect(
                dsn=self.__cfg.db_path,
                user=self.__cfg.username,
                password=self.__cfg.password
            )
            con.begin()
        except (AttributeError, TypeError):
            logger.error("Неправильные данные; база не найдена")
            raise
        except Exception as exc:
            logger.critical(f"Неизвестная ошибка: <{type(exc)}> {exc}", exc_info=True)
            raise
        else:
            logger.info("Подключение установлено!")
            
            logger.debug("Возврат значения")
            return con

    def close(self) -> None:
        if not self.__connect.closed:
            self.__connect.close()
            logger.info("Подключение закрыто.")
            return
        logger.critical("Подключение не закрыто!")
        
    def transaction(self) -> Transaction:
        """Открытие транзакции, в контексте которой будут выполняться команды

        Raises:
            ConnectionError: Выбрасывается при отсутствия подключения к бд как такового

        Returns:
            Transaction: Класс транзакции для взаимодействия с внутренними командами
        """
        logger.debug("Старт функции <transaction>")

        if self.__connect.closed:
            logger.error(err := ConnectionError("Отсутствует подключение к основной базе данных"))
            raise err
        
        logger.debug(f"Создание экземпляра объекта <{Transaction.__qualname__}>")
        return Transaction(self.__connect)


    @overload
    def single_transaction(self, *, type_api: Literal["high"], read_only: bool = False) -> TransactionSession[TransactionHigh]: ...
    @overload
    def single_transaction(self, *, type_api: Literal["low"], read_only: bool = False) -> TransactionSession[TransactionLow]: ...
    @overload
    def single_transaction(self, *, type_api: Literal["basic"], read_only: bool = False) -> TransactionSession[TransactionBasic]: ...

    @contextmanager
    def single_transaction(self, *, type_api: Literal["high", "low", "basic"], read_only: bool = False) -> TransactionSession:
        """Открытие транзакции "из коробки"

        Args:
            type_api (Literal["high", "low", "basic"]): Уровень взаимодействия с бд
            read_only (bool, optional): Тип транзакции. По умолчанию False.

        Returns:
            Контекстный менеджер
        """
        logger.debug("Старт функции <single_transaction>")
        
        if self.__connect.closed:
            logger.error(err := ConnectionError("Отсутствует подключение к основной базе данных"))
            raise err

        tr = Transaction(self.__connect)

        try:
            yield tr.start_transaction(type_api=type_api, read_only=read_only)
        finally:
            self.close()
            logger.debug("Функция <single_transaction> завершена")        
