from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# opcional: confirma que as rotas estÃ£o sendo importadas corretamente
from app.routers import users, auth, ai, metrics

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(metrics.router)
