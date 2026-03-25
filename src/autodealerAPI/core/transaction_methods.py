import fdb


class TransactionProperty:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.transaction = transaction

    def cursor(self):
        return self.transaction.cursor()

    def close_all_cursors(self):
        pass

class TransactionMethodsReadonly(TransactionProperty):
    def __init__(self, transaction) -> None:
        super().__init__(transaction)


class TransactionMethods(TransactionMethodsReadonly):
    def __init__(self, transaction) -> None:
        super().__init__(transaction)
 

