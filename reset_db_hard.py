import os, sqlite3
from sqlalchemy import inspect
from app.database import Base, engine
from app.models.user import User  # garante user com bio/ai_profile importado

db_path = r"C:/MIND_MVP_BUILD/MIND_FIN_PRO/backend/mindfin.db"
if os.path.exists(db_path):
    os.remove(db_path)
print("Removido:", db_path)

print("Criando tabelas…")
Base.metadata.create_all(bind=engine)

# Conferir via SQLAlchemy
ins = inspect(engine)
print("ENGINE URL:", engine.url)
print("Tabelas:", ins.get_table_names())
print("users cols:", [ (c['name'], str(c['type'])) for c in ins.get_columns('users') ])
