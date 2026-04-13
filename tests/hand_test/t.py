import sqlite3 as sql
from autodealerAPI import Connection, DatabaseConfig
import re

SIQ = """SELECT SHOP_NOMENCLATURE_ID, CODE, PRODUCER_ID FROM SHOP_NOMENCLATURE
WHERE CODE IS NOT NULL AND PRODUCER_ID IS NOT NULL
ORDER BY CODE ASC OFFSET 568 ROWS"""

lcon = sql.connect(r"C:\Program Files\_Scripts\_auxiliary-soft\autodealerAPI\src\autodealerAPI\utils\dop_data\format.db")
lcu = lcon.cursor()

fcon = Connection(DatabaseConfig())
with fcon.single_transaction(type_api="basic", read_only=True) as tr:
    fcur = tr._cursor()
    iterat = fcur.execute(SIQ).iter()
    for snid, code, prod in iterat:
        lcu.execute("INSERT INTO identify_product VALUES(?, ?, ?)", (snid, code, prod))
lcon.commit()

fcon.close()
lcon.close()