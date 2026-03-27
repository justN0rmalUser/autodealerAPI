from autodealerAPI import Connection
from autodealerAPI.config import DatabaseConfig
import fdb


db_cfg: DatabaseConfig = DatabaseConfig.from_ini(
    r"tests\hand_test\config.ini", 
    path_key="a", 
    user_key="b", 
    pass_key="c"
)


# try:
#     connect = Connection(db_cfg)
#     trans = connect.transaction(is_readonly=True)
    
#     with trans.pool() as tran:
#         pass
    
# except Exception as exc:
#     logger = exc
