from pydantic import BaseModel, Field
from typing import Final, Optional, TypeVar, Generic


class DocumentConfig:
    

class DirectoryRegistry(BaseModel):
    ID: Optional[int] = Field(default=None, ge=1, alias="DIRECTORY_REGISTRY_ID")
    METATABLE_ID: int = Field(..., ge=12, le=44, alias="METATABLE_ID")

class DocumentRegistry(BaseModel):
    ID: Optional[int] = Field(default=None, ge=1, alias="DOCUMENT_REGISTRY_ID")
    METATABLE_ID: int
    DOCUMENT_TYPE_ID_CACHE: int
    
    __meta__= {
        "TABLE_NAME": "DOCUMENT_REGISTRY",
        "GEN_NAME": "GEN_DOCUMENT_REGISTRY",
        "PRIMARY_KEY": "DOCUMENT_REGISTRY_ID"
    }


class DocumentCalculation(BaseModel):
    ID = Optional[int]
    title: str
    descript: str
    doc_reg_id: int
    DOCUMENT_TYPE_ID_CACHE: int
