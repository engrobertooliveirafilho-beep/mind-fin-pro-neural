from typing import Dict, Any
from app.mind_api.core import MindAPI

class MindLinkService:
    def __init__(self):
        self.mind = MindAPI()

    async def generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        profile = payload.get("profile", {})
        context = payload.get("context", {})
        intent  = payload.get("intent", "text")
        return await self.mind.generate_response(profile, context, intent)
