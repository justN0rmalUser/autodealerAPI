# from autodealerAPI import DatabaseConfig
from autodealerAPI import DatabaseConfig


config = DatabaseConfig.from_json("tempos.json", path_key="db_path", user_key="username", pass_key="pasword")
print(config.db_path, config.username, config.password)