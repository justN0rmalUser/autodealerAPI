import fdb
from fdb import Cursor
from .document_api import Document


class TransactionBasic:
    def __init__(self, transaction: fdb.Transaction) -> None:
        self.__transaction: fdb.Transaction = transaction

    def _cursor(self) -> Cursor:
        try:
            return self.__transaction.cursor()
        except Exception:
            # TODO logging
            raise
        
    
    # def new(self, table: config: BaseModel) -> Document:
    #     return Document.new(self._cursor())
        
        
    # def load(self, config: object) -> Document:
    #     metadata: dict = getattr(config, '__meta__')
        
    #     return Document.load(
    #         self._cursor(),
    #         name=metadata["TABLE_NAME"],
    #         gen_name=metadata["GEN_NAME"],
    #         seq_name=metadata["PRIMARY_KEY"],
    #         seq_value=config.ID
    #     )
        

    
class TransactionLow(TransactionBasic):
    def __init__(self, transaction: fdb.Transaction) -> None:
        super().__init__(transaction)
        
    
    def 
 


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
        