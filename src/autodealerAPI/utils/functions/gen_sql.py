"""Используемые независимые SQL"""

from pypika import Query, Table
from pypika.terms import LiteralValue


def new_row_query(table_name: str, *, data: dict) -> str:
    """Генерация SQL запроса для создания новой строчки в базе данных

    Args:
        table_name (str): Имя таблицы
        data (dict): Валидированные данные вида `КОЛОНКА: Значение`

    Returns:
        str: Запрос, готовый к использованию
    """
    query = (
        Query.into(Table(table_name))
        .columns(tuple(data.keys()))
        .insert(tuple(data.values()))
    )

    return str(query)


def old_row_query(table_name: str, *, pk_name: str, pk_id: int) -> str:
    """Генерация SQL запроса для получения уже имеющийся строчки в базе данных по первичному ключу

    Args:
        table_name (str): Имя таблицы
        pk_name (str): Имя первичного ключа
        pk_id (int): Значение первичного ключа

    Returns:
        str: Запрос, готовый к использованию
    """
    query = (
        Query.from_(table := Table(table_name))
        .select(table.star)
        .where(table.field(pk_name) == pk_id)
    )

    return str(query)


def find_row_query(table_name: str, *, criterion: str) -> str:
    """Генерация SQL запроса для получения строк таблицы, которые соответствуют условию (criterion)

    Args:
        table_name (str): Имя таблицы
        criterion (str): Условие, SQL-инъекция в WHERE

    Returns:
        str: Запрос, готовый к использованию
    """
    query = (
        Query.from_(table := Table(table_name))
        .select(table.star)
        .where(LiteralValue(criterion))
    )

    return str(query)


def update_fields_query(table_name: str, *, pk_name: str, pk_id: int, **fields) -> str:
    """Генерация SQL запроса для обновления конкретных полей (fields) в данной строке в БД

    Args:
        table_name (str): Имя таблицы
        pk_name (str): Имя первичного ключа
        pk_id (int): Значение первичного ключа
        fields (kwargs): Поле и значение, на которое нужно обновить вида `ПОЛЕ=Значение`

    Returns:
        str: Запрос, готовый к использованию
    """
    q = (
        Query.update(table := Table(table_name))
        .where(table.field(pk_name) == pk_id)
    )

    for key, value in fields.items():
        q = q.set(key, value)

    return str(q)


def get_attributes_query(table_name: str, *, pk_name: str, pk_id: int, fields: tuple) -> str:
    """Генерация SQL запроса для получения конкретных полей (fields) в данной строке в БД

    Args:
        table_name (str): Имя таблицы
        pk_name (str): Имя первичного ключа
        pk_id (int): Значение первичного ключа
        fields (tuple): Список имен колонок

    Returns:
        str: Запрос, готовый к использованию
    """
    q = (
        Query.from_(table:= Table(table_name))
        .select(*fields)
        .where(table.field(pk_name) == pk_id)
    )

    return str(q)
