import fdb
from contextlib import contextmanager
from .transaction_methods import TransactionMethods, TransactionMethodsReadonly


class Transaction:
    def __init__(self, connection: fdb.Connection) -> None:
        self.connection = connection
        self.transaction = self._create_transact()


    def _create_transact(self):
        trans = None
        try:
            trans = self.connection.trans()
        except Exception:
            if trans and not trans.closed:
                trans.close()
            raise
        else:
            return trans


    def close(self, commit: bool):
        if not self.transaction.closed:
            if commit:
                self.transaction.commit()
            self.transaction.close()


    def commit(self):
        if not self.transaction.closed:
            self.transaction.commit()
    

    def rollback(self):
        if not self.transaction.closed:
            self.transaction.rollback()


    @contextmanager
    def pool(self, readonly=False):
        if readonly:
            transact_api = TransactionMethodsReadonly(self.transaction)
        else:
            transact_api = TransactionMethods(self.transaction)

        try:
            yield transact_api
        except Exception:
            raise
        finally:
            self.close(commit=False if readonly else True)
