from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MetaModel(BaseModel):
    GENERATOR: Optional[str] = Field(..., pattern=r'^GEN_[A-Z]+(_[A-Z]+)*$')
    PRIMARY_KEY: Optional[str] = Field(..., pattern=r'^[A-Z]+(_[A-Z]+)*_ID$')


class DirectoryRegistryModel(MetaModel):
    METATABLE_ID: int = Field(..., ge=12, le=44)
    
class DocumentRegistryModel(MetaModel):
    METATABLE_ID: int = Field(..., ge=12, le=44)
    DOCUMENT_TYPE_ID_CACHE: int = Field(default=26, ge=1)
    
class ServiceCalculationModel(MetaModel):
    NAME: str
    NOTES: str
    DOCUMENT_REGISTRY_ID: int = Field(..., ge=1)
    DOCUMENT_TYPE_ID: int = Field(default=26, ge=1)
    FLAG: int = Field(default=16)
    
class ServiceCalculationGoodsModel(MetaModel):
    SERVICE_CALCULATION_ITEM_ID: int = Field(..., ge=1)
    SHOP_NOMENCLATURE_ID: int = Field(..., ge=1)
    GOODS_COUNT: int = Field(..., ge=0)
    COST: float = Field(..., ge=0)
    POSITION: int = Field(..., ge=1)
    
class AcceptedTables(Enum):
    DIRECTORY_REGISTRY = DirectoryRegistryModel
    DOCUMENT_REGISTRY = DocumentRegistryModel
    SERVICE_CALCULATION_ITEM = ServiceCalculationModel
    SERVICE_CALCULATION_GOODS = ServiceCalculationGoodsModel
    
    
    
print(AcceptedTables.DIRECTORY_REGISTRY in AcceptedTables)