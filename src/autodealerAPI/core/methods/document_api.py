from fdb import DataError
from datetime import date

from typing import TYPE_CHECKING
from pypika import Query, Table
from pypika.functions import CurDate

from ..datatyping.document_types import DirectoryRegistry, DocumentRegistry, DocumentConfig
from ..datatyping.product_types import Product


if TYPE_CHECKING:
    from fdb import Cursor


class Document:
    """Класс, философия которого - 1 экземпляр = 1 запись в базе данных"""
    def __init__(self, cursor: Cursor) -> None:
        self._cursor = cursor
        self.NAME = None
        self.GEN_NAME = None
        self.PRIMARY_KEY = None
        self.PRIMARY_KEY_ID = None
        
    @classmethod
    def load(cls, cursor: Cursor, *, config):
        obj = cls(cursor)
        obj.NAME = name
        obj.GEN_NAME = gen_name
        obj.PRIMARY_KEY = seq_name
        obj.PRIMARY_KEY_ID = seq_value
        
        table = Table(obj.NAME)
        query = Query.from_(table).select(table.star).where(table.field(obj.PRIMARY_KEY) == obj.ID)
        
        result = cursor.execute(str(query)).fetchone()
        if not result:
            raise DataError("Такой записи не существует!")
        else:
            result_body = result[0]
        return obj
    
    @classmethod
    def new(cls, cursor: Cursor, *, data: DocumentConfig):
        return obj
    
    
    def _gen_id(self) -> int:
        request = "SELECT NEXT VALUE FOR ? FROM RDB$DATABASE"
        response = self._cursor.execute(request, (self.GEN_NAME, )).fetchone()
        if response is None:
            raise ValueError(f"Не удалось получить идентификатор для таблицы '{self.GEN_NAME}'")
        return int(response[0])
    


class _DirectoryRegistry(Document):
    name = "DIRECTORY_REGISTRY"
    gen_name = "GEN_DIRECTORY_REGISTRY"
    id_name = "DIRECTORY_REGISTRY_ID"
    
    def __init__(self, cursor: Cursor) -> None:
        super().__init__(cursor)
        self.ID = None
        self.METATABLE_ID = None
        self.CREATE_USER_ID = 1
        self.CREATE_DATE = date.today()
        self.CHANGE_USER_ID = 1
        self.CHANGE_DATE = date.today()
        
        
    @classmethod
    def load(cls, cursor: Cursor, *, ID: int):
        table = Table(cls.name)
        query = Query.from_(table).select(table.star).where(table.field(cls.id_name) == ID)
        
        result = cursor.execute(str(query)).fetchone()
        if not result:
            raise DataError("Такой записи не существует!")
        else:
            result_body = result[0]
            
        obj = cls(cursor)
        
        obj.ID = result_body[0]
        obj.METATABLE_ID = result_body[1]
        obj.CREATE_USER_ID = result_body[2]
        obj.CREATE_DATE = result_body[3]
        obj.CHANGE_USER_ID = result_body[4]
        obj.CHANGE_DATE = result_body[5]
        
        return obj
    
    
    @classmethod
    def new(cls, cursor: Cursor, *, propertys: DocsConfig.DirectoryRegistry):
        obj = cls(cursor)
        obj.ID = obj._gen_id(obj.gen_name)
        obj.METATABLE_ID = propertys.METATABLE_ID
        
        table = Table(obj.name)
        query = table.insert(
            obj.ID,
            obj.METATABLE_ID,
            obj.CREATE_USER_ID,
            CurDate(),
            obj.CHANGE_USER_ID,
            CurDate()
        )
        
        obj._cursor.execute(str(query))
        return obj
        
