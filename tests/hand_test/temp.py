from autodealerAPI import Connection, DatabaseConfig, AcceptedTables as AT


con = Connection(DatabaseConfig())
trans = con.transaction()
with trans.start_transaction(type_api="high", read_only=True) as t:
    docs = t.create_document_out()
    t.fill_document_out(docs["D"])