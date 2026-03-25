"""Модуль для подключения к базе данных и создания транзакций"""
import fdb
from .transactions import Transaction
from ..utils.config import DatabaseConfig


class Connection:
    def __init__(self, cfg: DatabaseConfig=DatabaseConfig()):
        self.cfg = cfg
        self.__connect = self._create_connect()
        

    def _create_connect(self):
        con = None
        try:
            con = fdb.connect(
                dsn=self.cfg.db_path, 
                user=self.cfg.username,
                password=self.cfg.password
            )
        except Exception:
            if con and not con.closed:
                con.close()
            raise
        else:
            con.begin()
            return con


    def transaction(self):
        try:
            if not self.__connect:
                raise ConnectionError("Отсутствует подключение к основной базе данных")

            return Transaction(self.__connect)
        except Exception:
            # TODO
            raise