from .product_types import Product
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, overload, Generic, TypeVar, Any
from pypika import Query, Table, Columns
from pypika.functions import CurDate


T = TypeVar('T', Product, Any)

if TYPE_CHECKING:
    from fdb import Cursor
    from autodealerAPI.core.datatyping.enums.document_enums import Metatable


class Document(ABC):
    def __init__(self, cursor: Cursor):
        self.cursor = cursor
        
    @abstractmethod
    @property
    def __table_name(self): ...

    @abstractmethod
    @property
    def __gen_name(self): ...

    def __gen_id(self) -> int:
        request = "SELECT NEXT VALUE FOR ? FROM RDB$DATABASE"
        response = self.cursor.execute(request, (self.__gen_name, )).fetchone()
        if response is None:
            raise ValueError(f"Не удалось получить идентификатор для таблицы '{self.__gen_name}'")
        return int(response[0])
    
    @abstractmethod
    def __create_record(self): ...


class DirectoryRegistry(Document):
    def __init__(self, cursor: Cursor, metatable_id: int | Metatable) -> None:
        super().__init__(cursor)
        self.__metatable_id = metatable_id
        
        self.ID = self.__gen_id()
        self.__create_record()

    @property
    def __table_name(self):
        return "DIRECTORY_REGISTRY"
    @property
    def __gen_name(self):
        return "GEN_DIRECTORY_REGISTRY"
    
    def __create_record(self):
        t = Table(self.__table_name)
        columns = Columns(
            ("DIRECTORY_REGISTRY_ID", "INTEGER"),
            ("METATABLE_ID", "INTEGER"),
            ("CREATE_USER_ID", "INTEGER"),
            ("CREATE_DATE", "TIMESTAMP"),
            ("CHANGE_USER_ID", "INTEGER"),
            ("CHANGE_DATE", "TIMESTAMP")
        )
        query = str(Query.into(t).columns(columns).insert(
            self.ID,
            self.__metatable_id,
            1,
            CurDate(),
            1,
            CurDate()
        ))

        if not self.cursor.connection:
            raise ConnectionError("Соединение закрыто")
        
        self.cursor.execute(query) 