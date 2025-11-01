from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from sqlalchemy import text
from app.database import engine
from app.middleware.idempotency import IdempotencyMiddleware
from app.routes import users as users_router
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID") or str(uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response
app = FastAPI(title="MindFin API", version="0.1.0")
# Middlewares
app.add_middleware(RequestIDMiddleware)
app.add_middleware(IdempotencyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Saúde
@app.get("/health")
async def health():
    return {"status": "ok"}
@app.get("/readyz")
async def readyz():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
# Rotas de usuário (signup/login/me)
app.include_router(users_router.router, prefix="/users", tags=["users"])
