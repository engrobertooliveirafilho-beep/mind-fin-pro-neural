from sqlalchemy import inspect
from app.database import Base, engine
from app.models.user import User

print("DATABASE_URL(reset):", engine.url)
Base.metadata.create_all(bind=engine)

ins = inspect(engine)
print("Tabelas:", ins.get_table_names())
print("users cols:", [(c["name"], str(c["type"])) for c in ins.get_columns("users")])
print("ORM columns:", [c.key for c in User.__table__.columns])
