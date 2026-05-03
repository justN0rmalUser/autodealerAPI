"""Валидация данных для БД"""

from typing import Any
import logging

from autodealerAPI.types.models import AcceptedTables
from autodealerAPI.types.schemas.product_schema import Product


logger = logging.getLogger(__name__)


class Build:
    @staticmethod
    def table(schema: AcceptedTables, data: dict | str) -> tuple[str, dict[str, Any]]:
        if isinstance(data, dict):
            validated_model = schema.value.model_validate(data)
            return (schema.name, validated_model.model_dump(exclude_none=True))
        validated_model = schema.value.model_validate_json(data)
        return (schema.name, validated_model.model_dump(exclude_none=True))

    @staticmethod
    def product(data: dict) -> dict:
        logger.debug(f"Валидация модели: <{data}>")
        validated_model = Product.model_validate(data)
        logger.info(f"Модель валидирована, результат: <{validated_model}>")
        return validated_model.model_dump()
