import asyncio

class MindLinkService:
    async def generate(self, prompt: str):
        await asyncio.sleep(1)
        return f"[IA Neural] Resposta processada: {prompt}"
