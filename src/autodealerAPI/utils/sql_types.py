from autodealerAPI.utils.consts import ACCEPTED_TABLE_NAME
from pydantic import BaseModel, field_validator, ValidationError


class InsertQueryConfig(BaseModel):
    name: str
    colomns: dict[str, str | int | float]
    
    @field_validator("name", mode="before")
    def __is_upper(cls, value: str):
        if value not in ACCEPTED_TABLE_NAME:
            raise ValidationError("Таблица не найдена!")
        return value.strip()
    
    @field_validator("colomns", mode="before")
    def __is_upper_keys(cls, value: dict[str, str | int | float]):
        if not all(map(lambda x: x.upper() == x, value)):
            raise ValidationError("Наименование ключей должно быть в верхнем регистре!")
        return value


class GenPrimaryIdConfig(BaseModel):
    gen_name: str

    @field_validator("gen_name", mode="before")
    def __is_upper(cls, value: str):
        if value not in ACCEPTED_TABLE_NAME: #FIXME
            raise ValidationError("Таблица не найдена!")
        return value
