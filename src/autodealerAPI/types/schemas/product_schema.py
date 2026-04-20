from autodealerAPI.utils.functions.standard import std
from pydantic import BaseModel, Field, computed_field
import sqlite3 as lite


GET_SNID_SQL = """SELECT SNID
FROM identify_product
FULL JOIN firm f USING(FIRM_ID)
inner join code c USING(CODE)
WHERE f.FORMATTED_NAME = ? AND c.FORMATTED_CODE = ?
ORDER BY SNID DESC
"""


class Product(BaseModel):
    raw_name: str = Field(validation_alias="name", min_length=1, max_length=99)
    raw_firm: str = Field(validation_alias="firm")
    raw_code: str = Field(validation_alias="code")
    raw_count: float = Field(validation_alias="count", gt=0)
    raw_price: float = Field(validation_alias="price", gt=0)


    @computed_field
    @property
    def name(self):
        return std.name(self.raw_name)

    @computed_field
    @property
    def count(self):
        return std.numeric(self.raw_count)

    @computed_field
    @property
    def price(self):
        return std.numeric(self.raw_price)

    @computed_field
    @property
    def shop_nom_id(self) -> int | None:
        db = lite.connect("C:\\Program Files\\_Scripts\\_auxiliary-soft\\outer_data\\format.db")
        data = db.execute(GET_SNID_SQL, (
            std.text(self.raw_firm),
            std.text(self.raw_code)
            )
        ).fetchone()
        db.close()
        return int(data[0]) if data is not None else None

    @computed_field
    @property
    def firm_id(self) -> int:
        db = lite.connect("C:\\Program Files\\_Scripts\\_auxiliary-soft\\outer_data\\format.db")

        if self.shop_nom_id is None:
            data = db.execute(
                "SELECT FIRM_ID FROM firm WHERE FORMATTED_NAME = ?",
                (std.text(self.raw_firm), )
            ).fetchone()
        else:
            data = db.execute(
                "SELECT FIRM_ID FROM identify_product WHERE SNID = ?",
                (self.shop_nom_id, )
            ).fetchone()

        db.close()

        if data is not None:
            return int(data[0])
        raise Exception("Неизвестная фирма!")

    @computed_field
    @property
    def code(self) -> str:
        db = lite.connect("C:\\Program Files\\_Scripts\\_auxiliary-soft\\outer_data\\format.db")

        if self.shop_nom_id is None:
            data = db.execute(
                "SELECT CODE FROM code WHERE FORMATTED_CODE = ?",
                (std.text(self.raw_code), )
            ).fetchone()
        else:
            data = db.execute(
                "SELECT CODE FROM identify_product WHERE SNID = ?",
                (self.shop_nom_id, )
            ).fetchone()

        db.close()

        return data[0] if data is not None else self.raw_code
