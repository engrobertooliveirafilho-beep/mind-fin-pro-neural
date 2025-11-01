from sqlalchemy import inspect
from app.database import engine
print("DB:", engine.url)
ins = inspect(engine)
print("tables:", ins.get_table_names())
print("users:", [ (c["name"], str(c["type"])) for c in ins.get_columns("users") ])
