from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user import Post  # Post está no mesmo arquivo que criamos
from app.database import Base
from sqlalchemy import text

# Usa o mesmo DB do Alembic (SQLite local)
ENGINE = create_engine("sqlite:///./mindfin.db", future=True)

def ensure_schema():
    # Garantia extra (não deve ser necessário pois já migramos)
    Base.metadata.create_all(ENGINE)

def seed():
    with Session(ENGINE) as s:
        # Usuário
        email = "boss@mind.com"
        u = s.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if u is None:
            u = User(email=email, password_hash="bcrypt:demo", name="Chefao", bio="Owner")
            s.add(u)
            s.flush()

        # Posts (somente se não houver nenhum)
        has_post = s.execute(select(Post).limit(1)).scalar_one_or_none()
        if not has_post:
            s.add_all([
                Post(author_id=u.id, title="Primeiro post", content="Mind Fin Pro rodando no SQLite."),
                Post(author_id=u.id, title="Roadmap", content="Sprint 0: feed, auth, IA simulada, sockets.")
            ])
        s.commit()

if __name__ == "__main__":
    ensure_schema()
    seed()
    print("seed ok")
