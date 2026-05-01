from contextlib import AbstractContextManager
from types import TracebackType
from typing import Generic, Literal, Optional, Type, TypeVar, overload

import fdb

from autodealerAPI.core.methods.service import (
    TransactionBasic,
    TransactionHigh,
    TransactionLow,
)


T = TypeVar('T', TransactionHigh, TransactionLow, TransactionBasic)


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
        self._transaction = transaction
        self._read_only = read_only
        self._api = api


    def __enter__(self) -> T:
        """
        Вход в контекст: валидация состояния и инициализация API.
        """
        # 1. Проверка целостности соединения
        if self._transaction.closed:
            raise Exception("Транзакция закрыта!")

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
        if exc_type is not None:
            # Произошло исключение -> Откат
            if not self._transaction.closed:
                self._transaction.rollback()
                self._transaction.close()
        else:
            # Успешное выполнение -> Коммит (если не режим только для чтения)
            if not self._transaction.closed:
                if self._read_only:
                    self._transaction.rollback()
                else:
                    self._transaction.commit()
                self._transaction.close()

        return False


class Transaction:
    def __init__(self, connection: fdb.Connection) -> None:
        self.__connection: fdb.Connection = connection
        self.__transaction = self.__create_transact()


    def __create_transact(self) -> fdb.Transaction:
        try:
            trans: fdb.Transaction = self.__connection.trans()
            trans.begin()
        except (AttributeError, TypeError):
            raise
        except Exception:
            raise
        else:
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
        if self.__connection.closed:
            raise ConnectionAbortedError("Соединение закрыто, создание транзакции невозможно!")
        if self.__transaction.closed:
            raise ConnectionAbortedError("Транзакция закрыта, выполнение методов невозможно!")

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
