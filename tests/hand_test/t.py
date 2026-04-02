from autodealerAPI.core.build_types.types.schemas.product_schema import Product
from typing import overload
from autodealerAPI.core.build_types.models import AcceptedTables


class Build:
    @overload
    def table(schema: AcceptedTables, data: dict): ...
    @overload
    def table(schema: AcceptedTables, data: str): ...

    @staticmethod
    def table(schema: AcceptedTables, data: dict | str):
        if isinstance(data, dict):
            validated_model = schema.value.model_validate(data)
            return validated_model.model_dump(exclude_none=True)
        validated_model = schema.value.model_validate_json(data)
        return validated_model.model_dump_json(exclude_none=True)


    @overload
    def product(schema: Product, data: dict): ...
    @overload
    def product(schema: Product, data: str): ...

    @staticmethod
    def product(schema: Product, data: dict | str):
        if isinstance(data, dict):
            validated_model = schema.model_validate(data)
            return validated_model.model_dump(exclude_none=True)
        validated_model = schema.model_validate_json(data)
        return validated_model.model_dump_json(exclude_none=True)


class BuildedTable:
    def __init__(self):
        pass

print(Build.table(AcceptedTables.SHOP_NOMENCLATURE_ATTRIBUTE, {"DIRECTORY_REGISTRY_ID":'a'}))