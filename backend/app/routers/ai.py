from fastapi import APIRouter, Depends, HTTPException
from app.service.mindlink import MindLinkService
from app.core.security import auth_guard

router = APIRouter()
mind = MindLinkService()

@router.post("/generate")
async def generate_ai(data: dict, user=Depends(auth_guard)):
    if not data.get("intent"):
        data["intent"] = "text"
    resp = await mind.generate(data)
    return {"ok": True, "data": resp}
