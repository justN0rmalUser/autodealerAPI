from enum import Enum
from dataclasses import dataclass

dataclass(frozen=True)
class Metatable:
    DOCUMENT_OUT_HEADER = 12
    SHOP_NOMENCLATURE = 13
    DOCUMENT_IN = 14
    SHOP_NOMENCLATURE_ATTRIBUTE = 17
    DOCUMENT_OUT_HEADER_ATTRIBUTE = 28
    DOCUMENT_IN_ATTRIBUTE = 29
    SERVICE_CALCULATION_ITEM = 42
    GOODS_IN_ATTRIBUTE = 43
    GOODS_IN = 44
