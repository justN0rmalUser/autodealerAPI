from autodealerAPI import Connection


def main():
    con = Connection()

    with con.transaction().pool() as tr:
        tr.