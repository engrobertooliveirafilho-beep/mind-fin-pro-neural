from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
router = APIRouter()
# Armazenamento em memória (DEV)
_USERS: Dict[str, dict] = {}  # key: email -> {"name":..., "email":..., "password":..., "bio":..., "ai_profile":...}
class SignupIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    bio: Optional[str] = ""
    ai_profile: Optional[str] = ""
class LoginIn(BaseModel):
    email: EmailStr
    password: str
@router.post("/", status_code=201)
def signup(payload: SignupIn):
    email = payload.email.lower()
    if email in _USERS:
        # conflito = 409
        raise HTTPException(status_code=409, detail="email já cadastrado")
    _USERS[email] = payload.dict()
    # retorna mínimo
    u = _USERS[email].copy()
    u.pop("password", None)
    return u
@router.post("/login")
def login(payload: LoginIn):
    email = payload.email.lower()
    u = _USERS.get(email)
    if not u or u.get("password") != payload.password:
        raise HTTPException(status_code=401, detail="credenciais inválidas")
    # token fake de DEV: "dev:<email>"
    return {"access_token": f"dev:{email}", "token_type": "bearer"}
@router.get("/me")
def me(Authorization: Optional[str] = Header(None)):
    if not Authorization or not Authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = Authorization.split(" ", 1)[1]
    if not token.startswith("dev:"):
        raise HTTPException(status_code=401, detail="invalid token")
    email = token.split("dev:", 1)[1]
    u = _USERS.get(email)
    if not u:
        raise HTTPException(status_code=401, detail="user not found")
    out = u.copy()
    out.pop("password", None)
    return out
