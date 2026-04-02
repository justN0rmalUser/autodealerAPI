from autodealerAPI.core.build_types.types.standard import std
from autodealerAPI.utils.match_attribute import store_attribute
from typing import TYPE_CHECKING
from pydantic import BaseModel, Field, computed_field


if TYPE_CHECKING:
    from autodealerAPI.core.build_types.types.standard import Decimal

    
class Product(BaseModel):
    name: str = Field(default_factory=std.name, min_length=1, max_length=99)
    firm: str
    code: str = Field(default_factory=std.code)
    count: float = Field(gt=0)
    price: float = Field(gt=0)

    
    @computed_field
    @property
    def firm_id(self) -> int:
        return std.firm(self.firm)
    
    @computed_field
    @property
    def shop_nom_tree_id(self) -> int:
        return store_attribute(self.name)