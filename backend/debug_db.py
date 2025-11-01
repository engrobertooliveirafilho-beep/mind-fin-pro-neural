from sqlalchemy import create_engine, inspect
from app.database import engine
from app.database import Base
from app.models.user import User

print("ENGINE URL =", engine.url)

# garante que as tabelas do Base existem
Base.metadata.create_all(bind=engine)

insp = inspect(engine)
print("Tabelas:", insp.get_table_names())
print("Colunas de users:",
      [(c["name"], c["type"]) for c in insp.get_columns("users")])
