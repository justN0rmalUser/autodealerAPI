"""API для взаимодейтвия с таблицей"""

from typing import Any, Literal, Self

from fdb import Cursor, DataError

from autodealerAPI.utils.functions.gen_sql import (
    find_row_query,
    get_attributes_query,
    new_row_query,
    old_row_query,
    update_fields_query
)


class TableRow:
    """Класс, философия которого - 1 экземпляр = 1 запись в базе данных"""

    def __init__(self, cursor: Cursor, name: str) -> None:
        self.cursor = cursor
        self.name: str = name
        self.pk_id: int = None  # type: ignore

    @property
    def pk(self) -> str:
        """Первичный ключ"""
        return f"{self.name}_ID"

    @property
    def gen(self) -> str:
        """Генератор"""
        return f"GEN_{self.name}"

    def get_attributes(self, *fields) -> dict[str, Any]:
        """Получение необходимых полей в записи

        Raises:
            AttributeError: Ошибка отсутствия нужных полей

        Returns:
            dict[str, Any]: словарь со значениями полей
        """
        query = get_attributes_query(
            self.name,
            pk_name=self.pk,
            pk_id=self.pk_id,
            fields=fields
        )

        attributes = self.cursor.execute(query).fetchone()

        if attributes is None:
            raise AttributeError("Таких полей не существует")
        return dict(list(zip(fields, attributes)))

    def update_fields(self, **fields) -> None:
        """Изменение полей в записи"""
        query = update_fields_query(
            self.name,
            pk_name=self.pk,
            pk_id=self.pk_id,
            **fields
        )

        self.cursor.execute(query)

    @classmethod
    def load(cls, cursor: Cursor, table: str, pk_id: int | None) -> Self:
        """Загрузка имеющийся записи в бд

        Args:
            cursor (Cursor): курсор
            table (str): таблица
            ID (int | None): первичный ключ, идентификатор

        Raises:
            DataError: в случае ненахода записи

        Returns:
            TableRow: Имеющаяся запись в бд
        """
        # Инициализация объекта
        obj = cls(cursor, table)

        # Установление ID, если не задан
        if pk_id is None:
            obj.pk_id = obj._gen_id("last")
        else:
            obj.pk_id = pk_id

        # Генерация запроса sql
        query = old_row_query(
            obj.name,
            pk_name=obj.pk,
            pk_id=obj.pk_id
        )

        # Выполнение поиска записи
        result = cursor.execute(query).fetchone()

        # Проверка на существование
        if not result:
            raise DataError("Такой записи не существует!")

        return obj

    @classmethod
    def new(cls, cursor: Cursor, table: str, data: dict) -> Self:
        """Новая запись

        Args:
            cursor (Cursor): курсор
            table (str): имя таблицы
            data (dict): валидированные данные

        Returns:
            TableRow: экземпляр с новыми данными в бд
        """
        # Создание класса
        obj = cls(cursor, table)

        # Создание нового ID для записи в БД
        obj.pk_id = obj._gen_id("new")

        # Установка корректного первичного ключа
        data[obj.pk] = obj.pk_id

        # Генерация запроса SQL
        query = new_row_query(
            obj.name,
            data=data
        )

        # Непосредственный запрос в базу данных
        obj.cursor.execute(query)

        return obj

    @staticmethod
    def find(cursor: Cursor, table: str, condition: str):
        """Функция поиска с условием

        Args:
            cursor (Cursor): Курсор
            table (str): таблица в которой поиск
            condition (str): условие

        Returns:
            Cursor obj: итератор на найденные данные
        """
        # Генерация запроса sql
        query = find_row_query(
            table,
            criterion=condition
        )

        # Непосредственный запрос в БД с получением подходящих результатов
        result = cursor.execute(query).iter()

        return result

    def _gen_id(self, mode: Literal["new", "last"]) -> int:
        if mode == "new":
            request = f"SELECT NEXT VALUE FOR {self.gen} FROM RDB$DATABASE"
        elif mode == "last":
            request = f"SELECT GEN_ID({self.gen}, 0) FROM RDB$DATABASE"
        else:
            raise ValueError("Неизвестный тип взаимодействия с генератором ID")

        response = self.cursor.execute(request).fetchone()
        if response is None:
            raise ValueError(f'Не удалось получить идентификатор для таблицы "{self.gen}"')
        return int(response[0])
