from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime


class AbsModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class DIRECTORY_REGISTRY_schema(AbsModel):
	DIRECTORY_REGISTRY_ID: int = -1
	METATABLE_ID: int 
	CREATE_USER_ID: int 
	CREATE_DATE: str | datetime 
	CHANGE_USER_ID: int 
	CHANGE_DATE: str | datetime 

class SERVICE_CALCULATION_ITEM_schema(AbsModel):
	SERVICE_CALCULATION_ITEM_ID: int = -1
	SERVICE_CALCULATION_TREE_ID: int | None = None 
	NAME: str 
	CLIENT_ID: int  
	MODEL_LINK_ID: int | None = None 
	RT_MODEL_ID: int | None = None 
	RT_DOC_ID: int | None = None 
	DISCOUNT_CARD_ID: int | None = None 
	PRICE_NORM_ID: int  
	DISCOUNT_WORK: str | None = None 
	DISCOUNT_GOODS: str | None = None 
	MARK: int | None = None 
	AC_MODEL_ID: int | None = None 
	AC_MAP: int | None = None 
	DATE_CREATE: str | datetime
	DOCUMENT_REGISTRY_ID: int 
	DOCUMENT_TYPE_ID: int  
	FLAG: int 
	RMI_CAR_SELECT: str | None = None 

class SERVICE_CALCULATION_GOODS_schema(AbsModel):
	SERVICE_CALCULATION_GOODS_ID: int = -1
	SERVICE_CALCULATION_ITEM_ID: int
	SHOP_NOMENCLATURE_ID: int
	DISCOUNT: str 
	GOODS_COUNT: Decimal 
	COST: Decimal 
	DISCOUNT_FIX: Decimal | None = None 
	POSITION_NUMBER: int

class SHOP_NOMENCLATURE_schema(AbsModel):
	SHOP_NOMENCLATURE_ID: int = -1
	DIRECTORY_REGISTRY_ID: int 
	SHOP_NOMENCLATURE_TREE_ID: int
	SHORTNAME: str  
	FULLNAME: str  
	CODE: str
	NUMBER_MANUFACTURE: str 
	NUMBER_ORIGINAL: str  
	GOODS_TYPE_ID: int 
	UNIT_ID: int 
	TAX_SCHEMES_ID: int 
	MARGIN1: Decimal | None = None 
	MARGIN2: Decimal | None = None 
	MARGIN3: Decimal | None = None 
	MARGIN4: Decimal | None = None 
	MARGIN5: Decimal | None = None 
	MARGIN6: Decimal | None = None 
	COUNTRY_ID: int | None = None 
	PRODUCER_ID: int  
	TARE_ID: int | None = None 
	PACKING_ID: int | None = None 
	MATERIAL_ID: int | None = None 
	STOCK_MIN: Decimal | None = None 
	STOCK_MAX: Decimal | None = None 
	OLE: str | None = None 
	DEFAULT_COST: Decimal  
	DEFAULT_MARGIN: Decimal | None = None 
	DEFAULT_COUNT: Decimal 
	BAR_CODE: str | None = None 
	AC_DOC_ID: int | None = None 
	UID: int | None = None 
	BARCODE_TYPE: int | None = None 
	PRICE_ANALYSIS_GOODS_ID: int | None = None 
	MARK: int | None = None 
	DEFAULT_COUNT_IN: Decimal | None = None 
	MAX_DISCOUNT: Decimal | None = None 
	ABC_EXCLUDE: int | None = 0
	XYZ_EXCLUDE: int | None = 0
	MERGE_FLAG: int | None = None 
	TAX_SCHEMES_MATERIAL_ID: int 
	SEARCH_VALUE_TEXT: str | None = None 
	SEARCH_VALUE_NUMS: str | None = None 
	SEARCH_VALUE_BAR_CODE: str | None = None 
	MARKING: int = 0
	TCD_ARTICLE_NUMBER: str | None = None 
	TCD_GENERIC_ARTICLE_ID: int | None = None 
	TCD_LEGACY_ARTICLE_ID: int | None = None 
	SEARCH_VALUE_NUMBER_MANUFACTURE: str | None = None 
	SEARCH_VALUE_NUMBER_ORIGINAL: str | None = None 
	MARKING_GOODS_TYPE_ID: int | None = None 
	BARCODE_EXTRA: str | None = None 
	SEARCH_VALUE_BARCODE_EXTRA: str | None = None 

class SHOP_NOMENCLATURE_ATTRIBUTE_schema(AbsModel):
	DIRECTORY_REGISTRY_ID: int 

class SHOP_PRICE_schema(AbsModel):
	SHOP_PRICE_ID: int = -1
	SHOP_PRICE_GROUP_ID: int  
	SHOP_PRICE_LIST_ID: int 
	SHOP_NOMENCLATURE_ID: int 
	PRICE_POSITION: str | None = None 
	PRICE1: Decimal 
	PRICE2: Decimal | None = None 
	PRICE3: Decimal | None = None 
	PRICE4: Decimal | None = None 
	PRICE5: Decimal | None = None 
	PRICE6: Decimal | None = None 
	NOTES: str | None = None 

class DOCUMENT_REGISTRY_schema(AbsModel):
	DOCUMENT_REGISTRY_ID: int = -1
	METATABLE_ID: int 
	CREATE_USER_ID: int 
	CREATE_DATE: str | datetime 
	CHANGE_USER_ID: int 
	CHANGE_DATE: str | datetime 
	LOCK_USER_ID: int | None = None
	CLOUD_ID: int | None = None
	CLOUD_UPLOAD_TIME: str | None = None
	CLOUD_UPLOAD_VERSION: int | None = None
	DOCUMENT_TYPE_ID_CACHE: int | None = None

class DOCUMENT_OUT_HEADER_schema(AbsModel):
	DOCUMENT_OUT_HEADER_ID: int = -1
	DOCUMENT_OUT_TREE_ID: int | None = None
	DOCUMENT_REGISTRY_ID: int
	DOCUMENT_OUT_ID: int
	DOCUMENT_TYPE_ID: int 
	USER_ID: int 
	PREFIX: str | None = None
	NUMBER: int 
	SUFFIX: str | None = None
	DATE_CREATE: str | datetime 
	MARK: int | None = None
	STATE: int
	MANAGER_ID: int = 1
	BARCODE: str 
	CONTRACT_ID: int | None = None
	DOCUMENT_MARKING_STAGE: str | None = None
	DOCUMENT_MARKING_REASON: str | None = None

class DOCUMENT_ACTION_schema(AbsModel):
	DOCUMENT_ACTION_ID: int = -1
	DOCUMENT_REGISTRY_ID: int 
	USER_ID: int 
	ACTION_DATETIME: str | datetime 
	STATE: int 
	SUMMA: Decimal | None = None 

class DOCUMENT_OUT_schema(AbsModel):
	DOCUMENT_OUT_ID: int = -1
	DOCUMENT_TYPE_ID: int 
	DOCUMENT_IN_ID: int | None = None 
	SOURCE_DOCUMENT_OUT_ID: int | None = None
	ORGANIZATION_ID: int  
	ORGANIZATION_CONTACT_ID: int
	ORGANIZATION_REQUISITE_ID: int 
	CLIENT_ID: int  
	CLIENT_CONTACT_ID: int | None = None
	CLIENT_REQUISITE_ID: int | None = None
	SOURCE_INFO_ID: int | None = None
	DIVISION_COUNT: int | None = None
	RETURN_COUNT: int | None = None
	SUMMA: Decimal 
	DATE_ACCEPT: str  
	DATE_PAYMENT: str | None = None 
	DISCOUNT: str | None = None 
	DISCONT_CARD_ID: int | None = None 
	FLAG: int 
	BASIS_DOC: str | None = None
	BASIS_NUMBER: str | None = None
	BASIS_DATE: str | datetime | None = None
	SUMMA_BONUS: Decimal | None = None
	ROUND_VALUE: int | None = None

class DOCUMENT_RETURN_PVD_DETAIL_schema(AbsModel):
	DOCUMENT_RETURN_PVD_DETAIL_ID: int = -1
	DOCUMENT_OUT_HEADER_ID: int 
	REASON: str
	ATTORNEY_NUMBER: str | None = None 

class GOODS_OUT_schema(AbsModel):
	GOODS_OUT_ID: int = -1
	GOODS_IN_ID: int  
	DOCUMENT_OUT_ID: int 
	SHOP_NOMENCLATURE_ID: int 
	COST: float 
	DISCOUNT: int 
	GOODS_COUNT: float 
	GOODS_COUNT_FACT: float 
	GOODS_COUNT_RETURN: Decimal | None = None
	GUARANTE: int 
	DISCOUNT_FIX: Decimal | None = None 
	POSITION_NUMBER: int  
	ACTION_GOODS_ID: int | None = None 
	DISCOUNT_MANUAL: int | None = 0
	CORRECTION_SUMMA: Decimal | None = None 
	ACTION_PROMOTION_ID: int | None = None 
	TRANSFER_STATE: int | None = None 
	REQUEST_EMPLOYEE_ID: int | None = None 
	CONFIRMATION_EMPLOYEE_ID: int | None = None 

class GOODS_IN_schema(AbsModel):
	GOODS_IN_ID: int = -1
	GOODS_IN_OLD_ID: int | None = None 
	GOODS_IN_PREV_ID: int | None = None 
	STORE_ID: int 
	DOCUMENT_IN_ID: int 
	SHOP_NOMENCLATURE_ID: int 
	UNIT_ID: int 
	GTD_NUMBER: str | None = None 
	GOODS_COUNT: Decimal  
	COST1: Decimal 
	COST2: Decimal  
	GOODS_NOTES: str | None = None 
	IS_SALED: int | None = 0
	POSITION_NUMBER: int 

class DOCUMENT_CARGO_schema(AbsModel):
	DOCUMENT_CARGO_ID: int = -1
	DOCUMENT_OUT_ID: int 
	SENDER_ID: int = 1
	SENDER_CONTACT_ID: int = 4458
	SENDER_REQUISITE_ID: int = 2
	RECEIVER_ID: int 
	RECEIVER_CONTACT_ID: int | None = None
	RECEIVER_REQUISITE_ID: int | None = None
	ADDON_NUMBER: str | None = None
	ADDON_DATE: str | None = None
	UPDATE_SENDER: int = 0
	UPDATE_RECEIVER: int  = 0
	PAYER_ID: int 
	PAYER_CONTACT_ID: int | None = None
	PAYER_REQUISITE_ID: int | None = None
	UPDATE_PAYER: int = 0
	USE_MAIN_PAYMENT: int = 0
	SHIPMENT_DOC_POSITIONS: str | None = None
	SHIPMENT_DOC_NUMBER: str | None = None
	SHIPMENT_DOC_DATE: str | None = None
	SHIPMENT_DOC_NAME: str | None = None

