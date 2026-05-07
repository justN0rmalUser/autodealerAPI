"""API взаимодействия с транзакциями"""

from datetime import datetime, timedelta, date
from typing import Literal
import logging
from time import sleep

import fdb
from fdb import Cursor

from autodealerAPI.types.builder import Build
from autodealerAPI.types.models import AcceptedTables as Table
from autodealerAPI.core.methods.table_api import TableRow
from autodealerAPI.utils.functions.standard import parse_date_interval
from autodealerAPI.utils.literals.sqls import (
    GOODS_IN,
    Other
)


logger = logging.getLogger(__name__)


class TransactionBasic:
    """Атомарное взаимодействие с транзакциями
    редко используется пользователем"""
    def __init__(self, transaction: fdb.Transaction) -> None:
        logger.debug(f"Инициализация экземпляра объекта <{self.__class__.__qualname__}>")
        self.__transaction: fdb.Transaction = transaction

    def _cursor(self) -> Cursor:
        logger.debug("Создание курсора")
        return self.__transaction.cursor()

    def timestamp(self):
        """Timestamp для базы данных"""
        ts = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
        logger.debug(f"Создание таймштампа: <{ts}>")
        return ts

    def new(
        self,
        cursor: Cursor,
        *,
        schema: tuple[str, dict]
    ) -> TableRow:
        """Создание нового документа

        Args:
            cursor (Cursor): Курсор для взаимодействия
            schema (tuple[str, dict]): Схема базы таблицы с валидацией

        Returns:
            TableRow: Объект записи
        """
        table_name, data = schema
        return TableRow.new(
            cursor,
            table=table_name,
            data=data
        )

    def load(
        self,
        cursor: Cursor,
        *,
        table_name: str,
        ID: int | None = None
    ) -> TableRow:
        """Загрузка имеющийся записи в базе данных по первичному ключу

        Args:
            cursor (Cursor): Курсор для взаимодействия
            table_name (str): Имя таблицы
            ID (int | None, optional): Первичный ключ.
                При значении по умолчанию -> выбирается последняя запись в БД.

        Returns:
            TableRow: Объект записи
        """
        return TableRow.load(
            cursor,
            table=table_name,
            pk_id=ID
        )

    def find(
        self,
        cursor: Cursor,
        *,
        table_name: str,
        condition: str
    ) -> Cursor:
        """Поиск значений по условию

        Args:
            cursor (Cursor): Курсор для взаимодействия
            table_name (str): Имя таблицы
            condition (str): Условие в SQL формате

        Returns:
            Cursor: итератор на таблицу
        """
        return TableRow.find(
            cursor,
            table=table_name,
            condition=condition
        )


class TransactionLow(TransactionBasic):
    """Готово, но несвязное API для транзакции"""
    def __init__(self, transaction) -> None:
        logger.debug(f"Инициализация экземпляра объекта <{self.__class__.__qualname__}>")
        super().__init__(transaction)

    def new_document_registry(self):
        cursor = self._cursor()
        data = {
            "METATABLE_ID": 12,
            "CREATE_USER_ID": 1,
            "CREATE_DATE": self.timestamp(),
            "CHANGE_USER_ID": 1,
            "CHANGE_DATE": self.timestamp(),
            "DOCUMENT_TYPE_ID_CACHE": 7
        }
        builded_table = Build.table(
            schema=Table.DOCUMENT_REGISTRY,
            data=data
        )
        return self.new(cursor, schema=builded_table)

    def new_document_out(self, summa: float, partner_id: int):
        cursor = self._cursor()
        data = {
            "DOCUMENT_TYPE_ID": 7,
            "ORGANIZATION_ID": 1,
            "ORGANIZATION_CONTACT_ID": 4458,
            "ORGANIZATION_REQUISITE_ID": 2,
            "CLIENT_ID": partner_id,
            "SUMMA": summa,
            "DATE_ACCEPT": self.timestamp(),
            "FLAG": 1
        }
        builded_table = Build.table(
            schema=Table.DOCUMENT_OUT,
            data=data
        )
        return self.new(cursor, schema=builded_table)

    def new_document_out_header(
        self,
        doc_reg: int,
        doc_out: int,
        number: int
    ):
        cursor = self._cursor()
        data = {
            "DOCUMENT_REGISTRY_ID": doc_reg,
            "DOCUMENT_OUT_ID": doc_out,
            "DOCUMENT_TYPE_ID": 7,
            "USER_ID": 1,
            "NUMBER": number,
            "DATE_CREATE": self.timestamp(),
            "STATE": 2,
            "MANAGER_ID": 1,
            "BARCODE": '20000004'
        }
        builded_table = Build.table(
            schema=Table.DOCUMENT_OUT_HEADER,
            data=data
        )
        return self.new(cursor, schema=builded_table)

    def new_document_action(self, doc_reg: int):
        cursor = self._cursor()
        data = {
            "DOCUMENT_REGISTRY_ID": doc_reg,
            "USER_ID": 1,
            "ACTION_DATETIME": self.timestamp(),
            "STATE": 4
        }
        builded_table = Build.table(
            schema=Table.DOCUMENT_ACTION,
            data=data
        )
        return self.new(cursor, schema=builded_table)

    def new_document_cargo(self, doc_out: int, agent_id: Literal[8876, 8880]):
        logger.debug("Старт функции <new_document_cargo>")
        
        cursor = self._cursor()
        data = {
            "DOCUMENT_OUT_ID": doc_out,
            "RECEIVER_ID": agent_id,
            "PAYER_ID": agent_id
        }
        table_name, valid_data = Build.table(
            schema=Table.DOCUMENT_CARGO,
            data=data
        )

        logger.info(f"Создание документа: <{Table.DOCUMENT_CARGO.name}>")
        logger.debug("Возврат значений <new_document_cargo>")
        return TableRow.new(cursor, table=table_name, data=valid_data)

    def new_document_return_pvd_detail(self, doc_out_head: int):
        logger.debug("Старт функции <new_document_return_pvd_detail>")
        
        cursor = self._cursor()
        data = {
            "DOCUMENT_OUT_HEADER_ID": doc_out_head,
            "REASON": 'Отказ (Auto)'
        }
        table_name, valid_data = Build.table(
            schema=Table.DOCUMENT_RETURN_PVD_DETAIL,
            data=data
        )
        
        logger.info(f"Создание документа: <{Table.DOCUMENT_RETURN_PVD_DETAIL.name}>")
        logger.debug("Возврат значений <new_document_return_pvd_detail>")
        return TableRow.new(cursor, table=table_name, data=valid_data)

    def new_goods_out(
        self,
        cursor: Cursor,
        good_in: int,
        doc_out: int,
        shop_nom: int,
        price: float,
        count: float,
        pos: int
    ):
        logger.debug("Старт функции <new_goods_out>")

        data = {
            "GOODS_IN_ID": good_in,
            "DOCUMENT_OUT_ID": doc_out,
            "SHOP_NOMENCLATURE_ID": shop_nom,
            "COST": price,
            "DISCOUNT": 0,
            "GOODS_COUNT": count,
            "GOODS_COUNT_FACT": count,
            "GUARANTE": 1,
            "POSITION_NUMBER": pos
        }

        table_name, valid_data = Build.table(
            schema=Table.GOODS_OUT,
            data=data
        )

        logger.debug("Возврат значений <new_goods_out>")
        return TableRow.new(cursor, table=table_name, data=valid_data)


class TransactionHigh:
    """Полноценное и абстрактное взаимодействие с базой данных"""
    def __init__(self, transaction: fdb.Transaction) -> None:
        logger.debug(f"Инициализация экземпляра объекта <{self.__class__.__name__}>")
        self._trans = TransactionLow(transaction)

    def create_document_out(
        self,
        partner_id: Literal[8876, 8880],
        summa: float
    ) -> dict[
        Literal[
            "DOCUMENT_REGISTRY",
            "DOCUMENT_OUT",
            "DOCUMENT_CARGO",
            "DOCUMENT_OUT_HEADER",
            "DOCUMENT_RETURN_PVD_DETAIL"
        ], int
    ]:
        """Цикл создания документов возврата поставщику (1/2)

        Raises:
            TypeError: Внутренняя проверка - заданы ли первичные ключи
            ValueError: Ошибка поиска последнего подходящего номера для док-та

        Returns:
            dict: словарь используемых (созданных) идентификаторов в БД
        """
        logger.debug("Старт функции <create_document_out>")

        # создание документов
        logger.info(f"Создание основных документов в системе: <{Table.DOCUMENT_REGISTRY.name}>, <{Table.DOCUMENT_OUT.name}>")
        doc_reg = self._trans.new_document_registry()
        doc_out = self._trans.new_document_out(
            summa=summa,
            partner_id=partner_id
        )

        if not self._is_all_registered(doc_reg, doc_out):
            logger.critical(err := "Первичные ключи не заданы")
            raise TypeError(err)

        # Карго
        doc_cargo = self._trans.new_document_cargo(
            doc_out=doc_out.pk_id,
            agent_id=partner_id
        )

        # заголовок документа
        doc_out_head = self._trans.new_document_out_header(
            doc_reg=doc_reg.pk_id,
            doc_out=doc_out.pk_id,
            number=self._get_number_for_out_head()
        )

        if not self._is_all_registered(doc_out_head):
            logger.critical(err := "Первичный ключ doc_out_head не задан")
            raise TypeError(err)
        
        doc_ret_pvd_det = self._trans.new_document_return_pvd_detail(
            doc_out_head.pk_id
        )

        ids = {
            "DOCUMENT_REGISTRY": doc_reg.pk_id,
            "DOCUMENT_OUT": doc_out.pk_id,
            "DOCUMENT_CARGO": doc_cargo.pk_id,
            "DOCUMENT_OUT_HEADER": doc_out_head.pk_id,
            "DOCUMENT_RETURN_PVD_DETAIL": doc_ret_pvd_det.pk_id
        }
        logger.debug(f"Возврат значений <create_document_out>: {ids}")
        return ids

    def fill_document_out(
        self,
        raw_products: list[dict],
        doc_out_id: int,
        doc_out_head_id: int,
        search_date_interval: str=f"{date.today()-timedelta(days=62)}|{date.today()+timedelta(days=1)}"
    ) -> list[int]:
        """Заполнение документа возврата поставщику (2/2)

        Args:
            raw_products (list[dict]): Список полученных товаров
            doc_out_id (int): ID документа возврата
            doc_out_head_id (int): ID заголовочного документа возврата

        Raises:
            ValueError: Отсутствует SHOP_NOMENCLATURE_ID для нужного товара
            Exception: Остаток товара не соответствует действительности

        Returns:
            list[int]: Список ID записей товаров
        """
        logger.debug("Старт функции <fill_document_out>")
        
        update_cursor = cursor = self._trans._cursor()

        # matched_products - список обработанных значений; docs - созданные записи в БД
        matched_products: list[dict[str, int | bool]] = []
        docs = []

        for product in map(Build.product, raw_products):
            logger.info("Старт итерации")
            logger.debug(f"Текущие данные итерации: <{product}>")

            # Установка значений
            candidates_goods_in: tuple[tuple[int, int, str, int]] = self._get_goodsin(
                product["shop_nom_ids"],
                product["price"],
                search_date_interval
            )

            # Проверка на наличие в БД сделанной записи
            if candidates_goods_in is None:
                logger.warning(f"Запись возможно уже есть в базе данных, данные: <{product}>")
                continue
            
            # поиск первого подходящего товара
            for goods_in_id, snid, code, firm in candidates_goods_in:
                # Высчитывание остатка для этого GOODS_IN
                logger.info(f"Проверка: <{goods_in_id, snid, code, firm}>")
                remainder = self._count_of_free_cells(goods_in_id)

                # Соответствует ли количество продукта необходимому остатку
                if product["count"] <= remainder:
                    tproduct = {
                        "goods_in_id": goods_in_id,
                        "shop_nom_id": snid,
                        "count": product["count"],
                        "price": product["price"],
                        "is_sold_out": product["count"] == remainder
                    }

                    logger.info(f"Добавление: <{tproduct}>")
                    matched_products.append(tproduct)
                
                    logger.debug("Завершение цикла подбора")
                    break
            else:
                # если ни одно значение не подошло, то ошибка
                logger.critical(err := "Доступного остатка товара недостаточно для выполнения операции!")

        # Была ли хоть одна запись
        if not matched_products:
            logger.warning(err := "Документы пустые, все товары введены")
            raise Exception(err)

        logger.info("Старт создания записей в базе данных")
        # Внесение в БД
        for i, product in enumerate(matched_products, start=1):
            # Внесение в документ на позицию i
            docs.append(self._trans.new_goods_out(
                cursor,
                good_in=product["goods_in_id"],
                doc_out=doc_out_id,
                shop_nom=product["shop_nom_id"],
                price=product["price"],
                count=product["count"],
                pos=i
            ).pk_id)
            
            sleep(0.5)
            logger.info(f"Документ добавлен: <{docs[i-1]}>")

            # Обновление GOODS_IN если товар распродан
            if product["is_sold_out"]:
                logger.info("Обновление <IS_SALED> для записи")
                self._trans.load(
                    update_cursor,
                    table_name=Table.GOODS_IN.name,
                    ID=product["goods_in_id"]
                ).update_fields(
                    IS_SALED=1,
                )

        # Обновление DOCUMENT_OUT_HEADER
        logger.info(f"Установка статуса готовности для <{Table.DOCUMENT_OUT_HEADER.name}>")
        self._trans.load(
            update_cursor,
            table_name=Table.DOCUMENT_OUT_HEADER.name,
            ID=doc_out_head_id
        ).update_fields(
            STATE=4,
        )
        
        logger.info("Цикл внесения товаров пройден успешно.")

        # Закрытие и возврат документов
        cursor.close()
        
        logger.debug("Возврат значений <fill_document_out>")
        return docs

    # def create_calculation(self, *,
    #     title: str,
    #     descript: str,
    #     metatable_id: int,
    #     document_type_id: int
    # ) -> int:
    #     """Создает пустую калькуляцию в системе

    #     Args:
    #         _title (str): Наименование док-та
    #         _descript (str): Описание док-та
    #         _metatable_id (int): Принадлежность записи к системе
    #         _document_type_id (int): Принадлежность документа к системе

    #     Returns:
    #         doc_calc_id (int): ID созданной калькуляции
    #     """
    #     # cur = self._trans._cursor()
    #     doc_calc_id: int = self.__tr.document_calculation(
    #         _title=_title,
    #         _descript=_descript,
    #         _doc_reg_id=_doc_reg_id,
    #         _document_type_id=_document_type_id
    #     )
    #     return doc_calc_id

    # def fill_calculation(self, *,
    #     shop_nomeclature_id: int,
    #     doc_calc_id: int,
    #     count: int,
    #     price: int,
    #     pos: int
    # ) -> None:
    #     """Вносит в калькуляцию

    #     Args:
    #         shop_nomeclature_id (int): ID товара, который нужно внести
    #         doc_calc_id (int): ID документа, куда будет внесен товар
    #         count (int): Количество единиц товара
    #         price (int): Цена товара за штуку
    #         pos (int): Позиция в документе

    #     Returns:
    #         None
    #     """

    def _get_goodsin(
        self, 
        shop_nom_id: tuple[int] | None,
        price: float,
        search_date_interval: str
    ) -> tuple[tuple[int, int, str, int], ]:
        # Проверка shop_nom_id
        logger.debug("Старт функции <_get_goodsin>")
        
        if not shop_nom_id:
            logger.error(err := "Такой товар не найден")
            return None

        # Курсор для взаимодействия
        cursor = self._trans._cursor()
        start, end = parse_date_interval(search_date_interval)
        gin_sql_abs = GOODS_IN.GET_GOODS_IN_ID_BY_SHOP_NOM_ABSOLUTE.format(snids=shop_nom_id if len(shop_nom_id) > 1 else '('+str(shop_nom_id[0])+')')
        gin_sql_close = GOODS_IN.GET_GOODS_IN_ID_BY_SHOP_NOM_CLOSE.format(snids=shop_nom_id if len(shop_nom_id) > 1 else '('+str(shop_nom_id[0])+')')

        small_price = (price // 10 * 10)
        big_price = (price // 10 * 11)
        
        # Поиск нерасходованных товаров
        logger.info("Поиск наиболее подходящих GOODS_IN_ID по SHOP_NOMECLATURE_ID")
        goods_in_abs = cursor.execute(
            gin_sql_abs,
            (end, start, price, 0)
        ).fetchall()

        goods_in_close = cursor.execute(
            gin_sql_close,
            (end, start, big_price, small_price, 0)
        ).fetchall()
        
        logger.info("Поиск GOODS_IN_ID, которые были реализованны/возвращены по SHOP_NOMECLATURE_ID")
        goods_in_saled_abs = cursor.execute(
            gin_sql_abs,
            (end, start, price, 1)
        ).fetchone()

        goods_in_saled_close = cursor.execute(
            gin_sql_close,
            (end, start, big_price, small_price, 1)
        ).fetchall()

        # Проверка наличия
        if goods_in_abs:
            candidates_goods_in = tuple((int(gin), int(snid), code, int(firm)) for gin, snid, code, firm in goods_in_abs)
            logger.info(f"GOODS_IN_ID найдены: {candidates_goods_in}")
            logger.debug("Возврат значений <_get_goodsin>")
            return candidates_goods_in

        if goods_in_saled_abs:
            logger.info(f"GOODS_IN_ID не найдены, но есть пометка, что товар распродан: <{goods_in_saled_abs}>")
            logger.debug("Возврат значений <_get_goodsin>")
            return None
        
        if goods_in_close:
            candidates_goods_in = tuple((int(gin), int(snid), code, int(firm)) for gin, snid, code, firm in goods_in_close)
            logger.info(f"GOODS_IN_ID найдены: {candidates_goods_in}")
            logger.debug("Возврат значений <_get_goodsin>")
            return candidates_goods_in

        if goods_in_saled_close:
            logger.info(f"GOODS_IN_ID не найдены, но есть пометка, что товар распродан: <{goods_in_saled_close}>")
            logger.debug("Возврат значений <_get_goodsin>")
            return None

        logger.warning(f"Никакие GOODS_IN_ID не найдены: {shop_nom_id}")
        

    def _count_of_free_cells(self, goods_in_id: int) -> int:
        logger.debug("Старт функции <_count_of_free_cells>")
        
        # Курсор для краткого взаимодействия с БД
        temp_cursor = self._trans._cursor()

        # Получение результата
        res = int(
            temp_cursor.execute(
                Other.GET_FREE_CELLS,
                (goods_in_id, )
            ).fetchone()[0]  # type: ignore ## значение как минимум нуль
        )
        logger.info(f"Количество свободных слотов: <{res}>")

        # Закрытие курсора
        temp_cursor.close()

        logger.debug("Возврат значений <_count_of_free_cells>")
        return res

    def _get_number_for_out_head(self):
        temp_cursor = self._trans._cursor()

        req = (
            temp_cursor
            .execute(Other.GET_NUMBER_FOR_DOC_OUT)
            .fetchone()
        )

        temp_cursor.close()

        if not req:
            raise ValueError("Номер документа не найден")
        return int(req[0])
    
    def _is_all_registered(self, *docs: TableRow):
        for doc in docs:
            if not isinstance(doc.pk_id, int) or doc.pk_id == -1:
                return False
        return True
