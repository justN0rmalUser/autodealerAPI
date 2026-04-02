from pydantic import BaseModel
from decimal import Decimal
import re

from ....utils.dop_data.fmt_FirmCode import fmt_code, fmt_firm


class std:    
    @classmethod
    def firm(cls, value: str) -> int:
        """
        Ищет ID поставщика деталей
        """
        result = fmt_firm.get(value)
        if result is None:
            raise ValueError("ID фирмы не найдено")
        return result
    
    @classmethod
    def code(cls, value: str) -> str:
        result = fmt_code.get(value, value)
        return result
    
    @classmethod
    def price(cls, value: str | float) -> float:
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
            return float(result)
        elif isinstance(value, float):
            return float(value)
        raise TypeError("Не подходящий тип значения! Допустимые: str | float!")
        
    @classmethod
    def count(cls, value: str | int | float) -> int:
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
            return float(result)
        elif isinstance(value, int):
            return value
        else:
            return value
        raise TypeError("Не подходящий тип значения! Допустимые: str | float | int!")
    
    @classmethod
    def name(cls, value: str) -> str:
        value = value.lower().strip()
        for el in "\\|/-;:":
            value = value.replace(el, '')
        return value
        