from app.database import SessionLocal
from app.models.user import User
from app.models.post import Post
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

def get_or_create_user(email: str, name: str, password: str) -> User:
    u = db.query(User).filter(User.email == email).first()
    if u:
        return u
    u = User(
        name=name,
        email=email,
        password_hash=pwd_context.hash(password),
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

u1 = get_or_create_user("boss@mind.com", "Chefão", "123456")
u2 = get_or_create_user("ana@mind.com", "Ana", "123456")
u3 = get_or_create_user("leo@mind.com", "Leo", "123456")

def add_post(author: User, title: str, content: str) -> None:
    p = Post(title=title, content=content, author_id=author.id)
    db.add(p)
    db.commit()

add_post(u1, "Primeiro post", "Mind Fin Pro no ar")
add_post(u2, "Dica financeira", "Reserva de emergência primeiro")
add_post(u3, "Mindfeed", "Feed inteligente chegando")

print("Seed OK")
