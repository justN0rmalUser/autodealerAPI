import re
from datetime import date


class std:
    @staticmethod
    def text(value: str) -> str:
        value = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ]", '', value.upper())
        return value

    @staticmethod
    def numeric(value: str | float | int) -> float | int:
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
        elif isinstance(value, float) or isinstance(value, int):
            return value
        raise TypeError("Не подходящий тип значения! Допустимые: str | float!")

    @staticmethod
    def name(value: str) -> str:
        value = value.lower().strip()
        for el in "\\|/-;:":
            value = value.replace(el, '')
        return value


def parse_date_interval(iso_interval: str):
    start, end = iso_interval.split('|')
    return date.fromisoformat(start), date.fromisoformat(end)