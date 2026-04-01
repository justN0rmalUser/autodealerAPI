import fdb
from fdb import Cursor
from .document_api import Document
from autodealerAPI import AcceptedTables
from datetime import datetime
from ..serializing.sql import SubQuery


class TransactionBasic:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__transaction: fdb.Transaction = transaction

    def _cursor(self) -> Cursor:
        try:
            return self.__transaction.cursor()
        except Exception:
            # TODO logging
            raise
        
    
    def new(self, cursor: Cursor, *, schema: AcceptedTables, data: dict) -> Document:
        valid = schema.value.model_validate(data)
        return Document.new(cursor, schema=schema, valid_data=valid)
        
    def load(self, cursor: Cursor, *, schema: AcceptedTables, ID: int) -> Document:
        return Document.load(cursor, schema=schema, ID=ID)

    
class TransactionLow(TransactionBasic):
    def __init__(self, transaction: fdb.Transaction) -> None:
        super().__init__(transaction)
 
    
    def new_directory_registry(self): ...

    def new_document_registry(self):
        cursor = self._cursor()
        
        data = {
            "METATABLE_ID": 12,
            "CREATE_USER_ID": 1,
            "CREATE_DATE": datetime.date(datetime.now()),
            "CHANGE_USER_ID": 1,
            "CHANGE_DATE": datetime.date(datetime.now()),
            "DOCUMENT_TYPE_ID_CACHE": 7
        }
        return self.new(cursor, schema=AcceptedTables.DOCUMENT_REGISTRY, data=data)
    
    def new_document_out(self, summa: float, partner_id: int):
        cursor = self._cursor()
        
        data = {
            "DOCUMENT_TYPE_ID": 7,
            "ORGANIZATION_ID": 1,
            "ORGANIZATION_CONTACT_ID": 4458,
            "ORGANIZATION_REQUISITE_ID": 2,
            "CLIENT_ID": partner_id,
            "SUMMA": summa,
            "DATE_ACCEPT": datetime.date(datetime.now()),
            "FLAG": 1
        }
        return self.new(cursor, schema=AcceptedTables.DOCUMENT_OUT, data=data)
        
    def new_document_out_header(self, doc_reg: int, doc_out: int):
        cursor = self._cursor()
        
        data = {
            "DOCUMENT_REGISTRY_ID": doc_reg,
            "DOCUMENT_OUT_ID": doc_out,
            "DOCUMENT_TYPE_ID": 7,
            "USER_ID": 1,
            "NUMBER": SubQuery.NUMBER(),
            "DATE_CREATE": datetime.now(),
            "STATE": 2,
            "MANAGER_ID": 1,
            "BARCODE": '20000004'
        }
        return self.new(cursor, schema=AcceptedTables.DOCUMENT_OUT_HEADER, data=data)

    def new_document_action(self, doc_reg: int):
        cursor = self._cursor()
        
        data = {
            "DOCUMENT_REGISTRY_ID": doc_reg,
            "USER_ID": 1,
            "ACTION_DATETIME": datetime.now(),
            "STATE": 4
        }
        return self.new(cursor, schema=AcceptedTables.DOCUMENT_ACTION, data=data)

    def new_document_return_pvd_detail(self, doc_out_head: int):
        cursor = self._cursor()
        
        data = {
            "DOCUMENT_OUT_HEADER_ID": doc_out_head,
            "REASON": 'Отказ (Auto)'
        }
        return self.new(cursor, schema=AcceptedTables.DOCUMENT_RETURN_PVD_DETAIL, data=data)

    def new_goods_out(self, 
        good_in: int, 
        doc_out: int, 
        shop_nom: int, 
        price: float, 
        count: int, 
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
        return self.new(cursor, schema=AcceptedTables.GOODS_OUT, data=data)
    
    
class TransactionHigh:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__tr = TransactionLow(transaction)
        
        
    def create_calculation(self, *, 
        _title: str,
        _descript: str,
        _metatable_id: int,
        _document_type_id: int
    ) -> int:
        """Создает пустую калькуляцию в системе

        Args:
            _title (str): Наименование док-та
            _descript (str): Описание док-та
            _metatable_id (int): Принадлежность записи к системе
            _document_type_id (int): Принадлежность документа к системе
            
        Returns:
            doc_calc_id (int): ID созданной калькуляции
        """
        _doc_reg_id: int = self.__tr.new(
            _metatable_id=_metatable_id, 
            _document_type_id=_document_type_id
        )
        doc_calc_id: int = self.__tr.document_calculation(
            _title=_title, 
            _descript=_descript, 
            _doc_reg_id=_doc_reg_id, 
            _document_type_id=_document_type_id
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
        