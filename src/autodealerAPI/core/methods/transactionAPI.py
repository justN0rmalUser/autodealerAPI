import fdb
from fdb import Cursor
from typing import Literal

from .tableAPI import TableRow
from ..build_types.models import AcceptedTables as Table
from ..build_types.builder import Build
from datetime import datetime


class TransactionBasic:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__transaction: fdb.Transaction = transaction

    def _cursor(self) -> Cursor:
        try:
            return self.__transaction.cursor()
        except Exception:
            # TODO logging
            raise
        
    
    def new(self, cursor: Cursor, *, schema: Build) -> TableRow:
        table_name, data = schema
        return TableRow.new(cursor, table=table_name, data=data)
        
    def load(self, cursor: Cursor, *, table_name: str, ID: int | None = None) -> TableRow:
        return TableRow.load(cursor, table=table_name, ID=ID)

    
class TransactionLow(TransactionBasic):
    def __init__(self, transaction) -> None:
        super().__init__(transaction)

    def new_document_registry(self):
        cursor = self._cursor()
        data = {
            "METATABLE_ID": 12,
            "CREATE_USER_ID": 1,
            "CREATE_DATE": datetime.now().date(),
            "CHANGE_USER_ID": 1,
            "CHANGE_DATE": datetime.now().date(),
            "DOCUMENT_TYPE_ID_CACHE": 7
        }
        builded_table = Build.table(schema=Table.DOCUMENT_REGISTRY, data=data)
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
            "DATE_ACCEPT": datetime.now().date(),
            "FLAG": 1
        }
        builded_table = Build.table(schema=Table.DOCUMENT_OUT, data=data)
        return self.new(cursor, schema=builded_table)

    def new_document_out_header(self, doc_reg: int, doc_out: int, number: int):
        cursor = self._cursor()
        data = {
            "DOCUMENT_REGISTRY_ID": doc_reg,
            "DOCUMENT_OUT_ID": doc_out,
            "DOCUMENT_TYPE_ID": 7,
            "USER_ID": 1,
            "NUMBER": number,
            "DATE_CREATE": datetime.now(),
            "STATE": 2,
            "MANAGER_ID": 1,
            "BARCODE": '20000004'
        }
        builded_table = Build.table(schema=Table.DOCUMENT_OUT_HEADER, data=data)
        return self.new(cursor, schema=builded_table)

    def new_document_action(self, doc_reg: int):
        cursor = self._cursor()
        data = {
            "DOCUMENT_REGISTRY_ID": doc_reg,
            "USER_ID": 1,
            "ACTION_DATETIME": datetime.now(),
            "STATE": 4
        }
        builded_table = Build.table(schema=Table.DOCUMENT_ACTION, data=data)
        return self.new(cursor, schema=builded_table)

    def new_document_cargo(self, doc_out: int, agent_id: Literal[8876, 8880]):
        cursor = self._cursor()
        data = {
            "DOCUMENT_OUT_ID": doc_out,
            "RECEIVER_ID": agent_id,
            "PAYER_ID": agent_id
        }
        builded_table = Build.table(schema=Table.DOCUMENT_CARGO, data=data)
        return self.new(cursor, schema=builded_table)

    def new_document_return_pvd_detail(self, doc_out_head: int):
        cursor = self._cursor()
        data = {
            "DOCUMENT_OUT_HEADER_ID": doc_out_head,
            "REASON": 'Отказ (Auto)'
        }
        builded_table = Build.table(schema=Table.DOCUMENT_RETURN_PVD_DETAIL, data=data)
        return self.new(cursor, schema=builded_table)

    def new_goods_out(self, 
        good_in: int, 
        doc_out: int, 
        shop_nom: int, 
        price: float, 
        count: float, 
        pos: int
    ):
        cursor = self._cursor()
        data = {
            "GOODS_IN_ID": good_in,
            "DOCUMENT_OUT_ID": doc_out,
            "SHOP_NOMENCLATURE_ID": shop_nom,
            "COST": price,
            "GOODS_COUNT": count,
            "GOODS_COUNT_FACT": count,
            "GUARANTE": 1,
            "POSITION_NUMBER": pos
        }
        builded_table = Build.table(schema=Table.GOODS_OUT, data=data)
        return self.new(cursor, schema=builded_table)
    
    
class TransactionHigh:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self._trans = TransactionLow(transaction)
        
        
    def create_document_out(self, partner_id: int, summa: float) -> dict[Literal[
        "DOCUMENT_REGISTRY",
        "DOCUMENT_OUT",
        "DOCUMENT_CARGO",
        "DOCUMENT_OUT_HEADER",
        "DOCUMENT_RETURN_PVD_DETAIL"], TableRow]:

        # создание документов
        DocReg = self._trans.new_document_registry()
        DocOut = self._trans.new_document_out(summa=summa, partner_id=partner_id)

        if not (isinstance(DocReg.PK_ID, int) and isinstance(DocOut.PK_ID, int)):
            raise TypeError("Первичные ключи не заданы")
        
        # получение значения NUMBER
        temp_cur = self._trans._cursor()
        req = temp_cur.execute('SELECT MAX("NUMBER") + 1 FROM DOCUMENT_OUT_HEADER WHERE DOCUMENT_TYPE_ID = 7').fetchone()
        temp_cur.close()
        if not req:
            raise ValueError("Номер документа не найден")
        num = req[0]
        
        # Карго
        DocCargo = self._trans.new_document_cargo(
            doc_out=DocOut.PK_ID, 
            agent_id=partner_id
        )

        # заголовок документа
        DocOutHead = self._trans.new_document_out_header(
            doc_reg=DocReg.PK_ID, 
            doc_out=DocOut.PK_ID, 
            number=num
        )

        if not isinstance(DocOutHead.PK_ID, int):
            raise TypeError("Первичный ключ DocOutHead не задан")
        
        DocRetPvdDet = self._trans.new_document_return_pvd_detail(DocOutHead.PK_ID)

        return {
            "DOCUMENT_REGISTRY": DocReg.PK_ID,
            "DOCUMENT_OUT": DocOut.PK_ID,
            "DOCUMENT_CARGO": DocCargo.PK_ID,
            "DOCUMENT_OUT_HEADER": DocOutHead.PK_ID,
            "DOCUMENT_RETURN_PVD_DETAIL": DocRetPvdDet.PK_ID
        }
    
    def fill_document_out(
            self, 
            raw_products: list[dict], 
            doc_out_id: int,
            doc_out_head_id: int
        ):
        cursor = self._trans._cursor()

        GET_GOODSIN = """
        SELECT
            GIN.GOODS_IN_ID, 
            GIN.SHOP_NOMENCLATURE_ID, 
            GIN.GOODS_COUNT
        FROM GOODS_IN AS GIN
        INNER JOIN SHOP_NOMENCLATURE USING(SHOP_NOMENCLATURE_ID)
        WHERE PRODUCER_ID = ? AND (SEARCH_VALUE_NUMBER_MANUFACTURE = ? OR CODE = ?) AND IS_SALED = 0
        ORDER BY GIN.GOODS_IN_ID DESC, GIN.SHOP_NOMENCLATURE_ID DESC;
        """
        
        products = []
        for product in map(Build.product, raw_products):
            req = cursor.execute(
                GET_GOODSIN, 
                (
                    product["firm_id"], 
                    product["code"], 
                    product["code"]
                )
            ).fetchall()
            
            if req is None:
                raise("Ничего не найдено")
            
            good_found = False
            for goods_in, shop_nom_id, free_count in req:
                if product["count"] <= free_count:
                    products.append(
                        (
                            goods_in,
                            shop_nom_id,
                            product["price"],
                            product["count"]
                        )
                    )
                    good_found = True
                    break

            if not good_found:
                raise Exception("Никакой товар не подошел")

        docs = []
        for i, product in enumerate(products, start=1):
            goods_in, shop_nom_id, price, count = product
            docs.append(
                self._trans.new_goods_out(
                    good_in=goods_in,
                    doc_out=doc_out_id, 
                    shop_nom=shop_nom_id, 
                    price=price, 
                    count=count, 
                    pos=i
                )
            )
        DocHead = self._trans.load(cursor, "DOCUMENT_OUT_HEADER", ID=doc_out_head_id)
        DocHead.update_attributes(STATE=4)
        
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