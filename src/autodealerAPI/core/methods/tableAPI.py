from fdb import DataError

from typing import Literal, Self, Optional
from pypika import Query, Table
from pypika.terms import LiteralValue
from fdb import Cursor


class TableRow:
    """Класс, философия которого - 1 экземпляр = 1 запись в базе данных"""
    def __init__(self, cursor: Cursor, NAME: str, PK_ID: Optional[int] = None) -> None:
        self._cursor = cursor
        self.NAME: str = NAME
        self.PK_ID: int | None = PK_ID


    @property
    def PK(self):
        return f"{self.NAME}_ID"
    
    @property
    def GEN(self):
        return f"GEN_{self.NAME}"


    def get_attributes(self, *fields) -> list[tuple[str, str]]:
        q = Query.from_(
            t := Table(self.NAME)
        ).select(
            *fields
        ).where(
            t.field(self.PK) == self.PK_ID
        )

        attributes = self._cursor.execute(str(q)).fetchone()
        
        if attributes is None:
            raise AttributeError("Таких полей не существует")
        return zip(fields, attributes)

    
    def update_attributes(self, **fields):
        q = Query.update(
            t := Table(self.NAME)
        ).where(
            t.field(self.PK) == self.PK_ID
        )

        for key, field in fields.items():
            q = q.set(key, field)

        self._cursor.execute(str(q))
        

    @classmethod
    def load(cls, cursor: Cursor, table: str, ID: int | None) -> Self:
        # Инициализация объекта
        obj = cls(
            cursor, 
            table,
            ID
        )

        # Установление ID, если не задан
        if ID is None:
            obj.PK_ID = obj._gen_id("last")

        # Поиск записи
        result = cursor.execute(
            obj.__oldRow_query()
        ).fetchone()
        
        # Проверка на существование
        if not result:
            raise DataError("Такой записи не существует!")

        # Возврат записи в бд для работы с ней
        return obj


    @classmethod
    def find(cls, cursor: Cursor, table: str, condition: str) -> Self:
        # Инициализация объекта
        obj = cls(
            cursor, 
            table
        )

        result = cursor.execute(
            obj.__oldRow_query(condition)
        ).fetchone()



    @classmethod
    def new(cls, cursor: Cursor, table: str, data: dict) -> Self:
        obj = cls(
            cursor, 
            table
        )
        
        obj.PK_ID = obj._gen_id("new")
        obj._cursor.execute(obj.__newRow_query(data))

        return obj

    
    def _gen_id(self, mode: Literal["new", "last"]) -> int:
        if mode == "new": 
            request = f"SELECT NEXT VALUE FOR {self.GEN} FROM RDB$DATABASE"
        elif mode == "last":
            request = f"SELECT GEN_ID({self.GEN}, 0) FROM RDB$DATABASE"
            
        response = self._cursor.execute(request).fetchone()
        if response is None:
            raise ValueError(f'Не удалось получить идентификатор для таблицы "{self.GEN}"')
        return int(response[0])
    

    def __newRow_query(self, data: dict):
        data[self.PK] = self.PK_ID
        
        query = Query.into(
            Table(self.NAME)
        ).columns(
            tuple(data.keys())
        ).insert(
            tuple(data.values())
        )

        return str(query)
    
    def __oldRow_query(self, criterion: str | None = None):
        query = Query.from_(
            table := Table(self.NAME)
        ).select(
            table.star
        )

        if criterion is None:
            query = query.where(
                table.field(self.PK) == self.PK_ID
            )
        else:
            query = query.where(
                LiteralValue(criterion)
            )

        return str(query)