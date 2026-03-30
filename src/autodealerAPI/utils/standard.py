from pydantic import BaseModel
from decimal import Decimal
import re


class std(BaseModel):    
    @classmethod
    def firm(cls, value: str) -> int:
        """
        Ищет ID поставщика деталей
        """
        pass #TODO
        return -1
    
    @classmethod
    def code(cls, value: str) -> str:
        return value
    
    @classmethod
    def price(cls, value: str | float) -> Decimal:
        """Цена товара

        Args:
            value (str | float): Значение цены

        Raises:
            TypeError: При недопустимом типе

        Returns:
            Decimal: готовая для бд запись
        """
        if isinstance(value, str):
            result: str = value.replace(',', '.')
            result: str = re.sub(r"/[^0-9.]/g", '', value)
            return Decimal(result)
        elif isinstance(value, float):
            return Decimal.from_float(value)
        raise TypeError("Не подходящий тип значения! Допустимые: str | float!")
        
    @classmethod
    def count(cls, value: str | int | float) -> Decimal | int:
        """Количество товара

        Args:
            value (str | float | int): Значение количества

        Raises:
            TypeError: При недопустимом типе

        Returns:
            Decimal: готовая для бд запись
            int: уже преобразованный тип, просто пробрасывается
        """
        if isinstance(value, str):
            result: str = value.replace(',', '.')
            result: str = re.sub(r"/[^0-9.]/g", '', value)
            return Decimal(result)
        elif isinstance(value, float):
            return Decimal.from_float(value)
        elif isinstance(value, int):
            return value
        raise TypeError("Не подходящий тип значения! Допустимые: str | float | int!")
    
    @classmethod
    def name(cls, value: str) -> str:
        value = value.lower().strip()
        for el in "\\|/-;:":
            value = value.replace(el, '')
        return value
        