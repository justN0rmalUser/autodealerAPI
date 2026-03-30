from autodealerAPI.utils.accepted_tables import ACCEPTED_TABLE_NAME
from pydantic import BaseModel, field_validator, ValidationError, ConfigDict
from pypika.functions import CurTimestamp, CurDate


class InsertUpdateConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str
    columns: dict[str, str | int | float | CurTimestamp | CurDate]
    
    @field_validator("name", mode="before")
    def __is_upper(cls, value: str):
        if value not in ACCEPTED_TABLE_NAME:
            raise ValidationError("Таблица не найдена!")
        return value
    
    @field_validator("columns", mode="before")
    def __is_upper_keys(cls, value: dict[str, str | int | float]):
        if not all(key.isupper() for key in value):
            raise ValidationError("Наименование ключей должно быть в верхнем регистре!")
        return value

