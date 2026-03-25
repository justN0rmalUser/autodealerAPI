import fdb


class TransactionProperty:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__transaction = transaction

    def __cursor(self):
        try:
            return self.__transaction.cursor()
        except Exception:
            # TODO logging
            raise

    
    def _commit(self):
        self.__transaction.commit()



class TransactionMethodsReadonly(TransactionProperty):
    def __init__(self, transaction) -> None:
        super().__init__(transaction)

    
    def insert_state(self):
        pass

    
class TransactionMethods(TransactionMethodsReadonly):
    def __init__(self, transaction) -> None:
        super().__init__(transaction)
 

