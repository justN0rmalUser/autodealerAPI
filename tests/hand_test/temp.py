from autodealerAPI import Connection, DatabaseConfig, AcceptedTables as AT


con = Connection(DatabaseConfig())
trans = con.transaction()
with trans.start_transaction(type_api="high", read_only=True) as t:
    doc = t.new()