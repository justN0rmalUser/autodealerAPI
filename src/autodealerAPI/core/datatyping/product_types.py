from autodealerAPI.utils.standard import std
from autodealerAPI.utils.match_attribute import store_attribute
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from autodealerAPI.utils.standard import Decimal


class Product:
    __slots__ = (
        "__input", "__firm_key", "__code_key", "__price_key", "__count_key", "__name_key", # Служебные
        "shop_nom_id", "shop_nom_tree_id" # Опционально: ID товара в shop_nom и его метка в разделе 
    )
    
    def __init__(self, product: dict[str, str], *, firm_key="firm", code_key="code", price_key="price", count_key="count", name_key="name") -> None:
        self.__input = product
        self.__firm_key = firm_key
        self.__code_key = code_key
        self.__price_key = price_key
        self.__count_key = count_key
        self.__name_key = name_key
        
    @property
    def firm(self) -> str:
        value: str | None = self.__input.get(self.__firm_key)
        if value:
            return value
        raise KeyError("Ключ (фирма) не найден!")
    
    @property
    def firm_id(self) -> int:
        value: str | None = self.__input.get(self.__firm_key)
        if value:
            return std.firm(value)
        raise KeyError("Ключ (фирма) не найден!")
     
    @property
    def code(self) -> str:
        value: str | None = self.__input.get(self.__code_key)
        if value:
            return std.code(value)
        raise KeyError("Ключ (код) не найден!")
    
    @property
    def price(self) -> Decimal:
        value: str | None = self.__input.get(self.__price_key)
        if value:
            return std.price(value)
        raise KeyError("Ключ (цена) не найден!")
    
    @property
    def count(self) -> Decimal | int:
        value: str | None = self.__input.get(self.__count_key)
        if value:
            return std.count(value)
        raise KeyError("Ключ (количество) не найден!")
    
    @property
    def name(self) -> str:
        value: str | None = self.__input.get(self.__name_key)
        if value:
            return std.name(value)
        raise KeyError("Ключ (имя) не найден!")

    @property
    def shop_nom_tree_id(self):
        return store_attribute(self.name)
    