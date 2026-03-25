from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    db_path: str = "C:\\Program Files (x86)\\AutoDealer\\AutoDealer\\Database\\AutoDealer.fdb"
    username: str = "SYSDBA"
    password: str = "masterkey"

    @classmethod
    def from_json(cls):
        """
        docstring
        """
        pass
        #TODO