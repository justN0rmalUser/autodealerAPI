from pypika import Table, Query
from pypika.functions import Max


class SubQuery:
    def __init__(self):
        self.query: str | None = None

    @classmethod
    def NUMBER(cls):
        obj = cls()
        T = Table("DOCUMENT_OUT_HEADER")
        obj.query = Query.from_(T).select(Max(T.NUMBER)).where(T.DOCUMENT_TYPE_ID == 7)
        return obj
