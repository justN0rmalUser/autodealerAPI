from contextlib import AbstractContextManager
from types import TracebackType
from typing import Generic, Literal, Optional, Type, TypeVar, overload
import logging

import fdb

from autodealerAPI.core.methods.service import (
    TransactionBasic,
    TransactionHigh,
    TransactionLow,
)


T = TypeVar('T', TransactionHigh, TransactionLow, TransactionBasic)
logger = logging.getLogger(__name__)


class TransactionSession(AbstractContextManager, Generic[T]):
    """
    Контекстный менеджер для управления транзакцией БД.
    Обеспечивает атомарность операций и корректное закрытие ресурсов.
    """
    def __init__(
        self,
        transaction: fdb.Transaction,
        api: T,
        read_only: bool
    ) -> None:
        logger.debug(f"Инициализация экземпляра объекта <{self.__class__.__name__}>")
        self._transaction = transaction
        self._read_only = read_only
        self._api = api


    def __enter__(self) -> T:
        """
        Вход в контекст: валидация состояния и инициализация API.
        """
        logger.debug("Старт функции <__enter__>")

        logger.debug("Вход в контекст.")
        if self._transaction.closed:
            raise Exception("Транзакция закрыта!")

        logger.debug("Возврат значения")
        return self._api

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> Literal[False]:
        """
        Выход из контекста: фиксация или откат в зависимости от статуса выполнения.
        Возвращает False, чтобы исключения не подавлялись.
        """
        logger.debug("Старт функции <__exit__>")
        
        if exc_type is not None:
            # Произошло исключение -> Откат
            logger.warning("Выброшена ошибка, происходит откат действий!")
            if not self._transaction.closed:
                self._transaction.rollback()
                self._transaction.close()
        else:
            # Успешное выполнение -> Коммит (если не режим только для чтения)
            logger.info('Программа завершена без "исключений"')
            if not self._transaction.closed:
                if self._read_only:
                    self._transaction.rollback()
                    logger.info("Откат действий по параметру пользователя")
                else:
                    self._transaction.commit()
                    logger.info("Коммит по параметру пользователя")
                logger.info("Закрытие транзакции")
                self._transaction.close()
        
        logger.debug("Функция <__exit__> завершена")
        return False


class Transaction:
    def __init__(self, connection: fdb.Connection) -> None:
        logger.debug(f"Инициализация экземпляра объекта <{self.__class__.__name__}>")
        self.__connection: fdb.Connection = connection
        self.__transaction = self.__create_transact()


    def __create_transact(self) -> fdb.Transaction:
        logger.debug("Старт функции <__create_transact>")

        try:
            logger.info("Создание транзакции.")
            trans: fdb.Transaction = self.__connection.trans()
            trans.begin()
        except (AttributeError, TypeError):
            logger.error("Неправильные данные; база не найдена")
            raise
        except Exception as exc:
            logger.critical(f"Неизвестная ошибка: <{type(exc)}> {exc}", exc_info=True)
            raise
        else:
            logger.info("Транзакция создана без ошибок!")

            logger.debug("Возврат значения")
            return trans


    @overload
    def start_transaction(self, *, type_api: Literal["high"], read_only: bool) -> TransactionSession[TransactionHigh]: ...
    @overload
    def start_transaction(self, *, type_api: Literal["low"], read_only: bool) -> TransactionSession[TransactionLow]: ...
    @overload
    def start_transaction(self, *, type_api: Literal["basic"], read_only: bool) -> TransactionSession[TransactionBasic]: ...

    def start_transaction(self, *, type_api: Literal["high", "low", "basic"], read_only: bool = False) -> TransactionSession:
        """Функция-генератор, которая позволяет взаимодействовать с одной транзакцией с автозакрытием и коммитом

        Yields:
            Generator[TransactionHigh | TransactionLow]: API (методы) для записи в базу данных
        """
        logger.debug("Старт функции <start_transaction>")
        
        if self.__connection.closed:
            logger.error(err := ConnectionAbortedError("Соединение закрыто, создание транзакции невозможно!"))
            raise err
        if self.__transaction.closed:
            logger.error(err := ConnectionAbortedError("Транзакция закрыта, выполнение методов невозможно!"))
            raise err

        logger.info(f"Тип API: <{type_api}>.")
        match type_api:
            case "high":
                return TransactionSession[TransactionHigh](
                    transaction=self.__transaction,
                    api=TransactionHigh(self.__transaction),
                    read_only=read_only
                )
            case "low":
                return TransactionSession[TransactionLow](
                    transaction=self.__transaction,
                    api=TransactionLow(self.__transaction),
                    read_only=read_only
                )
            case "basic":
                return TransactionSession[TransactionBasic](
                    transaction=self.__transaction,
                    api=TransactionBasic(self.__transaction),
                    read_only=read_only
                )
