from autodealerAPI import Connection


con = Connection()
trans = con.transaction()
with trans.start_transaction(type_api="high", read_only=True) as t:
    t.