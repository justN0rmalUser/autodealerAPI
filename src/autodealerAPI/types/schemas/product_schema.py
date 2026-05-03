import sqlite3 as lite
from pydantic import BaseModel, Field, computed_field

from autodealerAPI.utils.functions.standard import std
from autodealerAPI.utils.literals.sqls import FindProduct


AUXILIARY_DB = "C:\\Program Files\\_Scripts\\_auxiliary-soft\\outer_data\\format.db"


class Product(BaseModel):
    raw_name: str = Field(validation_alias="name", min_length=1)
    raw_firm: str = Field(validation_alias="firm")
    raw_code: str = Field(validation_alias="code")
    raw_count: float = Field(validation_alias="count", gt=0)
    raw_price: float = Field(validation_alias="price", gt=0)


    @computed_field
    @property
    def name(self) -> str:
        return std.name(self.raw_name)

    @computed_field
    @property
    def count(self) -> float | int:
        return std.numeric(self.raw_count)

    @computed_field
    @property
    def price(self) -> float:
        return std.numeric(self.raw_price)

    @computed_field
    @property
    def shop_nom_ids(self) -> tuple[int] | None:
        with lite.connect(AUXILIARY_DB) as db:
            data = db.execute(
                FindProduct.GET_SNID_SQL, 
                (std.text(self.raw_firm), std.text(self.raw_code))
            ).fetchall()
            
        if data is None:
            return None
        return tuple(int(string[0]) for string in data)
        

    @computed_field
    @property
    def firm_id(self) -> int:
        with lite.connect(AUXILIARY_DB) as db:
            if self.shop_nom_ids is None or len(self.shop_nom_ids) != 1:
                data = db.execute(
                    FindProduct.SEEK_FIRM_BY_RAW,
                    (std.text(self.raw_firm), )
                ).fetchone()
            else:
                data = db.execute(
                    FindProduct.SEEK_FIRM_BY_SNID,
                    (self.shop_nom_ids[0], )
                ).fetchone()

        if data is not None:
            return int(data[0])
        raise Exception("Неизвестная фирма!")

    @computed_field
    @property
    def code(self) -> str:
        with lite.connect(AUXILIARY_DB) as db:
            if self.shop_nom_ids is None or len(self.shop_nom_ids) != 1:
                data = db.execute(
                    FindProduct.SEEK_CODE_BY_RAW,
                    (std.text(self.raw_code), )
                ).fetchone()
            else:
                data = db.execute(
                    FindProduct.SEEK_CODE_BY_SNID,
                    (self.shop_nom_ids[0], )
                ).fetchone()

        return data[0] if data is not None else self.raw_code
