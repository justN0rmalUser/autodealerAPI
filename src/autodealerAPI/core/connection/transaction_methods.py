import fdb
from autodealerAPI.utils.sql_types import InsertQueryConfig, GenPrimaryIdConfig
from pypika import Query


class TransactionBackService:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__transaction: fdb.Transaction = transaction


    def _cursor(self) -> fdb.Cursor:
        try:
            return self.__transaction.cursor()
        except Exception:
            # TODO logging
            raise

    
    def _generate_insert_query(self, table: InsertQueryConfig) -> str:
        return str(Query.into(table.name).columns(*table.colomns.keys()).insert(*table.colomns.values()))
    
    
    def _gen_id_query(self, table: GenPrimaryIdConfig) -> str:
        return f"SELECT NEXT VALUE FOR {table.gen_name} FROM RDB$DATABASE"


class TransactionMethodsReadonly(TransactionBackService):
    def __init__(self, transaction: fdb.Transaction) -> None:
        super().__init__(transaction)

    
class TransactionMethods(TransactionMethodsReadonly):
    def __init__(self, transaction: fdb.Transaction) -> None:
        super().__init__(transaction)
 

    def insert_state(self):
        pass
