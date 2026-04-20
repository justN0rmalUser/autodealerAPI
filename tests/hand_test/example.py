from autodealerAPI import Connection
from autodealerAPI.config import DatabaseConfig
from pypika.functions import CurDate


db_cfg: DatabaseConfig = DatabaseConfig.from_ini(
    r"tests\hand_test\config.ini", 
    path_key="a", 
    user_key="b", 
    pass_key="c"
)

try:
    connect = Connection(db_cfg)
    transact = connect.transaction()
    
    with connect.single_transaction(type_api="high", read_only=True) as tr:
        tr.create_calculation(title="a", descript="ds", metatable_id=3, document_type_id=2)
except Exception as exc:
    logger: Exception = exc
    raise 