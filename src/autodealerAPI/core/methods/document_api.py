from fdb import DataError

from typing import Self
from pypika import Query, Table
from pypika.functions import CurDate
from fdb import Cursor

from autodealerAPI import AcceptedTables


class Document:
    """Класс, философия которого - 1 экземпляр = 1 запись в базе данных"""
    def __init__(self, cursor: Cursor, NAME: str) -> None:
        self._cursor = cursor
        self.NAME: str = NAME
        self.PK_ID: int | None = None
        
    @property
    def PRIMARY_KEY(self):
        return f"{self.NAME}_ID"


    @classmethod
    def load(cls, cursor: Cursor, *, schema: AcceptedTables, ID: int) -> Self:
        obj = cls(cursor, schema.name)
        obj.PK_ID = ID
        
        table = Table(obj.NAME)
        query = Query.from_(table).select(table.star).where(table.field(obj.PRIMARY_KEY) == obj.PK_ID)
        
        result = cursor.execute(str(query)).fetchone()
        if not result:
            raise DataError("Такой записи не существует!")

        return obj


    @classmethod
    def new(cls, cursor: Cursor, *, schema: AcceptedTables, valid_data: dict) -> Self:
        obj = cls(cursor, schema.name)
        obj.PK_ID = obj._gen_id()

        valid_data[obj.PRIMARY_KEY] = obj.PK_ID
        if valid_data[obj.PRIMARY_KEY] != -1:
            table = Table(obj.NAME)
            query = Query.into(table).columns(
                tuple(valid_data.keys())
            ).insert(
                tuple(valid_data.values())
            )
        else:
            raise ValueError("Первичный ключ модели не изменен с -1")
        
        cursor.execute(query)
        
        return obj

    
    def _gen_id(self) -> int:
        request = f"SELECT NEXT VALUE FOR GEN_{self.NAME} FROM RDB$DATABASE"
        response = self._cursor.execute(request).fetchone()
        if response is None:
            raise ValueError(f"Не удалось получить идентификатор для таблицы '{self.NAME}'")
        return int(response[0])
    