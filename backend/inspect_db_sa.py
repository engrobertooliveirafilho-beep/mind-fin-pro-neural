from sqlalchemy import inspect
from app.database import engine
ins = inspect(engine)
print("ENGINE URL:", engine.url)
print("Tabelas:", ins.get_table_names())
print("users cols:", [(c["name"], str(c["type"])) for c in ins.get_columns("users")])
