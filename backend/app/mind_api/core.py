from typing import Any, Dict
from app.mind_api.adapters.gpt_adapter import GPTAdapter
from app.mind_api.adapters.sora_adapter import SoraAdapter
from app.mind_api.adapters.openart_adapter import OpenArtAdapter
from app.mind_api.adapters.profit_adapter import ProfitAdapter

class MindAPI:
    def __init__(self):
        self.gpt = GPTAdapter()
        self.sora = SoraAdapter()
        self.openart = OpenArtAdapter()
        self.profit = ProfitAdapter()

    async def generate_response(self, profile: Dict[str, Any], context: Dict[str, Any], intent: str) -> Dict[str, Any]:
        # Roteamento simples por intent; ajuste depois conforme regras
        if intent in ("text", "coach", "insight"):
            return await self.gpt.generate(profile, context)
        if intent in ("video", "sora"):
            return await self.sora.generate(profile, context)
        if intent in ("image", "openart"):
            return await self.openart.generate(profile, context)
        if intent in ("finance", "profit"):
            return await self.profit.generate(profile, context)
        # Fallback â†’ GPT
        return await self.gpt.generate(profile, context)
