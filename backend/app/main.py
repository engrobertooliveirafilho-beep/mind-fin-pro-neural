from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import SecurityMiddleware

app = FastAPI(title="MIND FIN PRO")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from app.core.config import settings
if settings.REDIS_URL:
    app.add_middleware(SecurityMiddleware)

@app.get("/health")
def health_root():
    return {"status": "ok"}

# Registre routers reais aqui (sem import em routers/__init__.py)
try:
    from app.routers import users, posts, health
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(posts.router, prefix="/posts", tags=["posts"])
except Exception:
    # Em fase de estabilizaÃ§Ã£o, nÃ£o derruba o /health
    pass




