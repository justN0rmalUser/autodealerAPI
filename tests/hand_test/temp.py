import sqlite3 as sql


AUXILIARY_DB = "C:\\Program Files\\_Scripts\\_auxiliary-soft\\outer_data\\format.db"

lite_con = sql.connect(AUXILIARY_DB)
lite_cur = lite_con.cursor()

with lite_con as ltr:
    M = lite_cur.execute("SELECT MAX(SNID) FROM identify_product WHERE SNID = -1").fetchone()[0]
    print(M)