from pypika import Table, Query
from pypika.functions import Max

T = Table("DOCUMENT_OUT_HEADER")
print(str(Query.from_(T).select(Max(T.NUMBER)).where(T.DOCUMENT_TYPE_ID == 7)))