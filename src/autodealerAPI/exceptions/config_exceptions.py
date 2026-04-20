from typing import Any, List, Optional


class ConfigurationError(BaseException):
    """
    Базовое исключение для всех ошибок, связанных с конфигурацией.

    Используется как корневой класс для специфических исключений конфигурации.
    """
    pass


class ConfigurationNotProvidedError(ConfigurationError):
    """Исключение возникает, когда конфигурация не была передана в класс или метод.

    Атрибуты:
        message (str): Сообщение об ошибке.
    """
    def __init__(self, message: str = "Конфигурация не предоставлена"):
        self.message = message
        super().__init__(self.message)


class IncompleteConfigurationError(ConfigurationError):
    """
    Исключение возникает, когда конфигурация не содержит обязательных полей.

    Attributes:
        missing_keys (List[str]): Список отсутствующих ключей.
        message (str): Сообщение об ошибке.
    """
    def __init__(self, missing_keys: List[str], message: Optional[str] = None):
        self.missing_keys = missing_keys
        if message is None:
            keys_str = ", ".join(f"'{key}'" for key in missing_keys)
            self.message = f"Конфигурация неполная. Отсутствуют ключи: {keys_str}"
        else:
            self.message = message
        super().__init__(self.message)


class InvalidConfigurationValueError(ConfigurationError):
    """
    Исключение возникает, когда значение конфигурации имеет недопустимый тип или формат.

    Атрибуты:
        key (str): Ключ конфигурации, вызвавший ошибку.
        expected_type (Any): Ожидаемый тип данных.
        actual_value (Any): Полученное значение.
    """
    def __init__(self, key: str, expected_type: Any, actual_value: Any):
        self.key = key
        self.expected_type = expected_type
        self.actual_value = actual_value
        self.message = (
            f"Недопустимое значение для ключа '{key}'. "
            f"Ожидался тип {expected_type}, получено {type(actual_value).__name__}"
        )
        super().__init__(self.message)


class ConfigurationFileNotFoundError(ConfigurationError):
    """
    Исключение возникает, когда файл конфигурации не найден по указанному пути.

    Атрибуты:
        path (str | Path): Путь к файлу с конфигурацией.
    """
    def __init__(self, path: str):
        self.path = path
        self.message = f"Файл конфигурации не найден по пути: {path}"
        super().__init__(self.message)


class ConfigurationParsingError(ConfigurationError):
    """
    Исключение возникает при ошибке парсинга файла конфигурации (JSON, YAML и т.д.).

    Attributes:
        reason (str): Причина ошибки парсинга.
    """
    def __init__(self, reason: str):
        self.reason = reason
        self.message = f"Ошибка парсинга конфигурации: {reason}"
        super().__init__(self.message)
