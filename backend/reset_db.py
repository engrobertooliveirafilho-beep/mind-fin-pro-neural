from app.database import Base, engine
from app.models.user import User  # garante que a tabela users com bio/ai_profile entra no metadata
print("Dropping all…"); Base.metadata.drop_all(bind=engine)
print("Creating all…"); Base.metadata.create_all(bind=engine)
print("OK")
