from ...config import DatabaseConfig
from .standard import std
import sqlite3 as sql
import fdb


AUXILIARY_DB = "C:\\Program Files\\_Scripts\\_auxiliary-soft\\outer_data\\format.db"

SIQ = """SELECT 
    SHOP_NOMENCLATURE_ID, 
    CODE,
    NUMBER_MANUFACTURE,
    PRODUCER_ID 
FROM SHOP_NOMENCLATURE
WHERE (CODE IS NOT NULL OR NUMBER_MANUFACTURE IS NOT NULL) AND PRODUCER_ID IS NOT NULL AND SHOP_NOMENCLATURE_ID > ?"""

def update_db():
    cfg = DatabaseConfig().model_dump()

    lite_con = sql.connect(AUXILIARY_DB)
    fdb_con = fdb.connect(cfg["db_path"], cfg["username"], cfg["password"])
            
    lite_cur = lite_con.cursor()
    fdb_cur = fdb_con.cursor()

    with lite_con as ltr:
        with fdb_con as rtr:
            maximum_snid = lite_cur.execute("SELECT MAX(SNID) FROM identify_product").fetchone()[0]
            
            if maximum_snid is None:
                raise Exception("Ошибка в format db, максималка - None")
            
            iterat = fdb_cur.execute(SIQ, (int(maximum_snid), )).fetchall()

            if not iterat:
                return
            
            for snid, code, num_man, prod in iterat:
                if (code and num_man) and code == num_man:
                    lite_cur.execute("INSERT INTO identify_product VALUES(?, ?, ?)", (snid, code, prod))
                    if not (lite_cur
                            .execute("SELECT CODE FROM code WHERE code.FORMATTED_CODE = ?", (fmt_code := std.text(code), ))
                            .fetchone()):
                        lite_cur.execute("INSERT INTO code VALUES(?, ?)", (fmt_code, code))
                    continue

                if code:
                    lite_cur.execute("INSERT INTO identify_product VALUES(?, ?, ?)", (snid, code, prod))
                    if not (lite_cur
                            .execute("SELECT CODE FROM code WHERE code.FORMATTED_CODE = ?", (fmt_code := std.text(code), ))
                            .fetchone()):
                        lite_cur.execute("INSERT INTO code VALUES(?, ?)", (fmt_code, code))
                        

                if num_man:
                    lite_cur.execute("INSERT INTO identify_product VALUES(?, ?, ?)", (snid, num_man, prod))
                    if not (lite_cur
                            .execute("SELECT CODE FROM code WHERE code.FORMATTED_CODE = ?", (fmt_code := std.text(num_man), ))
                            .fetchone()):
                        lite_cur.execute("INSERT INTO code VALUES(?, ?)", (fmt_code, num_man))

            rtr.commit()
            ltr.commit()