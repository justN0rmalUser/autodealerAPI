import fdb
from autodealerAPI import DatabaseConfig

FIND_TABLE = """
SELECT
    TRIM(rf.RDB$FIELD_NAME) AS column_name,
    TRIM(t.RDB$TYPE_NAME) AS data_type,
    f.RDB$FIELD_LENGTH AS field_length,
    f.RDB$FIELD_SCALE AS field_scale,
    f.RDB$FIELD_SUB_TYPE AS field_subtype,
    CASE 
        WHEN rf.RDB$NULL_FLAG = 1 THEN 0 
        ELSE 1
    END AS is_nullable,
    TRIM(f.RDB$DEFAULT_SOURCE) AS default_value,
    rf.RDB$FIELD_POSITION AS ordinal_position
FROM 
    RDB$RELATION_FIELDS rf
    JOIN RDB$FIELDS f ON rf.RDB$FIELD_SOURCE = f.RDB$FIELD_NAME
    JOIN RDB$RELATIONS r ON rf.RDB$RELATION_NAME = r.RDB$RELATION_NAME
    JOIN RDB$TYPES t ON f.RDB$FIELD_TYPE = t.RDB$TYPE 
        AND t.RDB$FIELD_NAME = 'RDB$FIELD_TYPE'
WHERE 
    TRIM(rf.RDB$RELATION_NAME) = '{TABLE_NAME}'
    AND (r.RDB$SYSTEM_FLAG IS NULL OR r.RDB$SYSTEM_FLAG = 0)
ORDER BY 
    rf.RDB$FIELD_POSITION;
"""


cfg = DatabaseConfig()
con = fdb.connect(
    dsn = cfg.db_path,
    user = cfg.username,
    password = cfg.password
)

t = con.trans()
curs = t.cursor()

while tab := input("Введите имя таблицы для генерации схемы: "):
    curs.execute(FIND_TABLE.format(TABLE_NAME=tab))
    with open(r"C:\Program Files\_Scripts\_auxiliary-soft\autodealerAPI\src\autodealerAPI\utils\tables_property.py", 'a', encoding="utf-8") as FILE:
        FILE.write(f"class {tab}_schema(Enum):\n")
        data = sorted(curs.fetchall(), key=lambda item: item[-1])
        for column in data:
            NAME, TYPE, BYTE_LENGTH, FIELD_SCALE, SUB_TYPE_FLAG, IS_NULLABLE, DEFAULT_VALUE, ORDINAL_POSITION = column
            if TYPE in ("BLOB", "TEXT"):
                continue
            if TYPE in ("LONG", "INT64", "SHORT"):
                if int(SUB_TYPE_FLAG):
                    type_data = "Decimal"
                else:
                    type_data = "int"
            else:
                type_data = "str"

            FILE.write(f"\t{NAME}: {type_data} ")
            if int(IS_NULLABLE):
                FILE.write("| None ")
            if DEFAULT_VALUE:
                FILE.write(f"= {DEFAULT_VALUE[8:]}")
            FILE.write("\n")
        FILE.write("\n")
            
            