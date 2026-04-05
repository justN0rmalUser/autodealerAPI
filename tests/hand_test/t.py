from pypika import Query, Table

fields = {"a":1,"b":2}

q = Query.update(
    t := Table("selfNMAE")
).set("AAA", 12).where(
    t.field(1) == 1
)

for i in 0,1,2:
    q = q.set("AAA", 12)

q.where(
    t.field(1) == 1
)

print(str(q))

