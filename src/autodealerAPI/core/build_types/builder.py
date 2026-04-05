from .types.schemas.product_schema import Product
from typing import overload
from .models import AcceptedTables


class Build:
    @overload
    def table(schema: AcceptedTables, data: dict): ...
    @overload
    def table(schema: AcceptedTables, data: str): ...

    @staticmethod
    def table(schema: AcceptedTables, data: dict | str | None = None):
        if isinstance(data, dict):
            validated_model = schema.value.model_validate(data)
            return (schema.name, validated_model.model_dump(exclude_none=True))
        validated_model = schema.value.model_validate_json(data)
        return (schema.name, validated_model.model_dump_json(exclude_none=True))


    @staticmethod
    def product(data: dict) -> dict:
        validated_model = Product.model_validate(data)
        return validated_model.model_dump(exclude_none=True)
