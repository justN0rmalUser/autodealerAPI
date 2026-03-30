import fdb
from fdb import Cursor
from autodealerAPI.core.datatyping.sql_types import InsertUpdateConfig, GenPrimaryIdConfig
from pypika import Query
from pypika.functions import CurDate


class TransactionBackService:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__transaction: fdb.Transaction = transaction


    def _cursor(self) -> Cursor:
        try:
            return self.__transaction.cursor()
        except Exception:
            # TODO logging
            raise

    
    def __insert_query(self, table: InsertUpdateConfig) -> str:
        return str(Query.into(table.name).columns(*table.columns.keys()).insert(*table.columns.values()))
    
    
    def __gen_id_query(self, table: GenPrimaryIdConfig) -> str:
        return f"SELECT NEXT VALUE FOR {table.gen_name} FROM RDB$DATABASE"
    
    
    def __gen_id(self, table: GenPrimaryIdConfig, *, cur: Cursor | None=None) -> int:
        if not cur:
            cur = self._cursor()
            
        request = cur.execute(self.__gen_id_query(table)).fetchone()
        
        if request is None:
            raise ValueError(f"Не удалось получить идентификатор для таблицы '{table.gen_name}'")
        
        return request[0]
    
    
    def __insert(self, table: InsertUpdateConfig, *, cur: Cursor | None=None):
        if not cur:
            cur = self._cursor()
        
        cur.execute(self.__insert_query(table))

    
class TransactionLow(TransactionBackService):
    def __init__(self, transaction: fdb.Transaction) -> None:
        super().__init__(transaction)
 

    def directory_registry(self, _metatable_id: int) -> int:
        """Внутренняя регистрация элемента в directory_registry

        Args:
            _metatable_id (int): Мета таблица с ID вида записи
            
        Returns:
            DIRECTORY_REGISTRY_ID: (int): ID таблицы DIRECTORY_REGISTRY
        """
        cursor: Cursor = self._cursor()
        
        cfg_gen_DOC_REG = GenPrimaryIdConfig(gen_name="GEN_DIRECTORY_REGISTRY")
        id_DOC_REG: int = self.__gen_id(table=cfg_gen_DOC_REG, cur=cursor)
        
        cfg_DOC_REG = InsertUpdateConfig(
            name="DIRECTORY_REGISTRY",
            columns={
                "DIRECTORY_REGISTRY_ID": id_DOC_REG,
                "METATABLE_ID": _metatable_id,
                "CREATE_USER_ID": 1,
                "CREATE_DATE": CurDate(),
                "CHANGE_USER_ID": 1,
                "CHANGE_DATE": CurDate(),
            }
        )
        
        self.__insert(table=cfg_DOC_REG, cur=cursor)
        
        cursor.close()
        return id_DOC_REG
        
        
    def document_registry(self, *, _metatable_id: int, document_type_id: int) -> int:
        """Регистрация документа во внутренней системе
        
        Args:
            _metatable_id (int): Мета таблица с ID вида записи
            document_type_id (int): Мета таблица с ID вида док-та

        Returns:
            DOCUMENT_REGISTRY_ID (int): ID таблицы DOCUMENT_REGISTRY
        """
        cursor: Cursor = self._cursor()

        cfg_gen_DOC_REG = GenPrimaryIdConfig(gen_name="GEN_DOCUMENT_REGISTRY")
        id_DOC_REG: int = self.__gen_id(table=cfg_gen_DOC_REG, cur=cursor)

        cfg_DOC_REG = InsertUpdateConfig(
            name="DOCUMENT_REGISTRY",
            columns={
                "DOCUMENT_REGISTRY_ID": id_DOC_REG,
                "METATABLE_ID": _metatable_id,
                "CREATE_USER_ID": 1,
                "CREATE_DATE": CurDate(),
                "CHANGE_USER_ID": 1,
                "CHANGE_DATE": CurDate(),
                "DOCUMENT_TYPE_ID_CACHE": document_type_id,
            },
        )

        self.__insert(table=cfg_DOC_REG, cur=cursor)

        cursor.close()
        return id_DOC_REG


    def document_calculation(self, *, title: str, descript: str, doc_reg_id: int, document_type_id: int) -> int:
        """Создание калькуляции в системе

        Args:
            title (str): Наименование документа
            descript (str): Описание документа
            doc_reg_id (int): Ссылка на позицию в DOCUMENT_REGISTRY
            document_type_id (int): Мета таблица с ID вида док-та

        Returns:
            SERVICE_CALCULATION_ITEM_ID (int): ID таблицы SERVICE_CALCULATION_ITEM
        """
        cursor: Cursor = self._cursor()

        cfg_gen_CALC = GenPrimaryIdConfig(gen_name="GEN_SERVICE_CALCULATION_ITEM")
        id_CALC: int = self.__gen_id(table=cfg_gen_CALC, cur=cursor)

        cfg_CALC = InsertUpdateConfig(
            name="SERVICE_CALCULATION_ITEM",
            columns={
                "SERVICE_CALCULATION_ITEM_ID": id_CALC,
                "NAME": title,
                "PRICE_NORM_ID": 6,
                "NOTES": descript,
                "DATE_CREATE": CurDate(),
                "DOCUMENT_REGISTRY_ID": doc_reg_id,
                "DOCUMENT_TYPE_ID": document_type_id,
                "FLAG": 16,
                "DISCOUNT_WORK": 0,
                "DISCOUNT_GOODS": 0,
            },
        )

        self.__insert(table=cfg_CALC, cur=cursor)

        cursor.close()
        return id_CALC

    # =========================================================================
    # GOODS_CALCULATION
    # =========================================================================
    def goods_calculation(
        self, *, calc_id: int, sin_id: int, count: float, price: float, pos: int
    ) -> None:
        cursor: Cursor = self._cursor()

        cfg_GOODS = InsertUpdateConfig(
            name="SERVICE_CALCULATION_GOODS",
            columns={
                "SERVICE_CALCULATION_ITEM_ID": calc_id,
                "SHOP_NOMENCLATURE_ID": sin_id,
                "DISCOUNT": 0,
                "GOODS_COUNT": count,
                "COST": price,
                "DISCOUNT_FIX": 0,
                "POSITION_NUMBER": pos,
            },
        )

        self.__insert(table=cfg_GOODS, cur=cursor)

        cursor.close()

    # =========================================================================
    # FIND_SHOPNOM_ID
    # =========================================================================
    def find_shopnom_id(self, *, firm: int, code: str) -> int | None:
        cursor: Cursor = self._cursor()

        query = """
            SELECT SHOP_NOMENCLATURE_ID 
            FROM SHOP_NOMENCLATURE
            WHERE PRODUCER_ID = ? AND CODE = ?
        """

        try:
            result = cursor.execute(query, (firm, code)).fetchone()
            cursor.close()
            return result[0] if result else None
        except Exception:
            # TODO logging
            cursor.close()
            return None


    def new_nomenclature(self, *, dir_reg: int, name: str, shop_tree: int, code: str, firm_id: int, cost: float, margin: float, firm_value: str) -> int:
        cursor: Cursor = self._cursor()

        search_text: str = f"{name.upper().replace(' ', '')} {name.upper().replace(' ', '')} {firm_value.upper().replace(' ', '')} "
        search_nums: str = f"{code.replace(' ', '')} {code.replace(' ', '')} "

        cfg_gen_NOM = GenPrimaryIdConfig(gen_name="GEN_SHOP_NOMENCLATURE")
        id_NOM: int = self.__gen_id(table=cfg_gen_NOM, cur=cursor)
        
        cfg_NOM = InsertUpdateConfig(
            name="SHOP_NOMENCLATURE",
            columns={
                "SHOP_NOMENCLATURE_ID": id_NOM,
                "DIRECTORY_REGISTRY_ID": dir_reg,
                "SHOP_NOMENCLATURE_TREE_ID": shop_tree,
                "SHORTNAME": name,
                "FULLNAME": name,
                "CODE": code,
                "NUMBER_MANUFACTURE": code,
                "GOODS_TYPE_ID": 1,
                "UNIT_ID": 1,
                "TAX_SCHEMES_ID": 2,
                "PRODUCER_ID": firm_id,
                "DEFAULT_COST": cost,
                "DEFAULT_MARGIN": margin,
                "DEFAULT_COUNT": 1,
                "BARCODE_TYPE": 14,
                "DEFAULT_COUNT_IN": 1,
                "TAX_SCHEMES_MATERIAL_ID": 2,
                "SEARCH_VALUE_TEXT": search_text,
                "SEARCH_VALUE_NUMS": search_nums,
                "SEARCH_VALUE_NUMBER_MANUFACTURE": code
            }
        )
        
        cfg_ATTR = InsertUpdateConfig(
            name="SHOP_NOMENCLATURE_ATTRIBUTE",
            columns={
                "DIRECTORY_REGISTRY_ID": dir_reg
            }
        )
        
        cfg_PRICE = InsertUpdateConfig(
            name="SHOP_PRICE",
            columns={
                "SHOP_PRICE_LIST_ID": 3,
                "SHOP_NOMENCLATURE_ID": id_NOM,
                "PRICE_POSITION": 1,
                "PRICE1": cost,
            },
        )
        
        self.__insert(table=cfg_NOM, cur=cursor)
        self.__insert(table=cfg_ATTR, cur=cursor)
        self.__insert(table=cfg_PRICE, cur=cursor)
        
        cursor.close()
        return id_NOM


class TransactionHigh(TransactionBackService):
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__tr = TransactionLow(transaction)
        
        
    def create_calculation(self, *, 
        title: str,
        descript: str,
        metatable_id: int,
        document_type_id: int
    ) -> int:
        """Создает пустую калькуляцию в системе

        Args:
            title (str): Наименование док-та
            descript (str): Описание док-та
            metatable_id (int): Принадлежность записи к системе
            document_type_id (int): Принадлежность документа к системе
            
        Returns:
            doc_calc_id (int): ID созданной калькуляции
        """
        doc_reg_id: int = self.__tr.document_registry(
            _metatable_id=metatable_id, 
            document_type_id=document_type_id
        )
        doc_calc_id: int = self.__tr.document_calculation(
            title=title, 
            descript=descript, 
            doc_reg_id=doc_reg_id, 
            document_type_id=document_type_id
        )
        return doc_calc_id
    
    
    def fill_calculation(self, *, 
        shop_nomeclature_id: int,
        doc_calc_id: int,
        count: int,
        price: int,
        pos: int
    ) -> None:
        """Вносит в калькуляцию

        Args:
            shop_nomeclature_id (int): ID товара, который нужно внести
            doc_calc_id (int): ID документа, куда будет внесен товар
            count (int): Количество единиц товара
            price (int): Цена товара за штуку
            pos (int): Позиция в документе

        Returns:
            None
        """
        