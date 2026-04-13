from pypika import Query, Table
from pypika.terms import Term, LiteralValue


query = Query.from_(
    table := Table("SDK")
).select(
    table.star
).where(
    LiteralValue("ID > NONES")
)

print(str(query))