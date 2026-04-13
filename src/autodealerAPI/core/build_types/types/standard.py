import re

from ....utils.dop_data.fmt_FirmCode import fmt_code, fmt_firm


class std:
    @classmethod
    def text(cls, value: str) -> str:
        value = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]", '', value.upper())
        return value

    
    @classmethod
    def numeric(cls, value: str | float | int) -> float | int:
        """Цена товара

        Args:
            value (str | float): Значение цены

        Raises:
            TypeError: При недопустимом типе

        Returns:
            float: готовая для бд запись
        """
        if isinstance(value, str):
            result: str = value.replace(',', '.')
            result: str = re.sub(r"/[^0-9.]/g", '', value)
            return float(result)
        elif isinstance(value, float):
            return float(value)
        elif isinstance(value, int):
            return value
        raise TypeError("Не подходящий тип значения! Допустимые: str | float!")


    @classmethod
    def name(cls, value: str) -> str:
        value = value.lower().strip()
        for el in "\\|/-;:":
            value = value.replace(el, '')
        return value
        