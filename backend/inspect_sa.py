from sqlalchemy import inspect
from app.database import engine
i = inspect(engine)
print("DB URL:", engine.url)
print("Tabelas:", i.get_table_names())
if "users" in i.get_table_names():
    cols = [(c["name"], str(c["type"])) for c in i.get_columns("users")]
    print("users cols:", cols)
