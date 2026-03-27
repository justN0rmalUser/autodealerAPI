import fdb
from typing import Generator
from contextlib import contextmanager
from .transaction_methods import TransactionMethods, TransactionMethodsReadonly


class Transaction:    
    def __init__(self, connection: fdb.Connection, readonly: bool=False) -> None:
        self.__connection: fdb.Connection = connection
        self.__transaction: fdb.Transaction = self.__create_transact()
        self.__RO: bool = readonly


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


    def close(self, commit: bool) -> None:
        if not self.__transaction.closed:
            if commit:
                self.__transaction.commit()
            else:
                self.__transaction.rollback()
            self.__transaction.close()
            
 
    @contextmanager
    def pool(self) -> Generator[TransactionMethods | TransactionMethodsReadonly]:
        """Функция-генератор, которая позволяет взаимодействовать с одной транзакцией с автозакрытием и коммитом

        Yields:
            Generator[TransactionMethods | TransactionMethodsReadonly]: API (методы) для записи в базу данных
        """
        if self.__transaction.closed or self.__connection.closed:
            raise Exception("Транзакция закрыта!") if self.__transaction.closed else Exception("Соединение закрыто!")
        
        if self.__RO:
            transact_api = TransactionMethodsReadonly(self.__transaction)  
        else:
            transact_api = TransactionMethods(self.__transaction)

        try:
            yield transact_api
        except Exception:
            raise
        finally:
            self.close(commit=False if self.__RO else True)
