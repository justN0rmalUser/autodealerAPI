from autodealerAPI.core.build_types.types.standard import std
from autodealerAPI.utils.match_attribute import store_attribute
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
    name: str = Field(default_factory=std.name, min_length=1, max_length=99)
    raw_firm: str = Field(validation_alias="firm")
    raw_code: str = Field(validation_alias="code")
    count: float = Field(default_factory=std.numeric, gt=0)
    price: float = Field(default_factory=std.numeric, gt=0)

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