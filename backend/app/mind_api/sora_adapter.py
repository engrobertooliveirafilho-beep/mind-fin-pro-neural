import asyncio
class SoraAdapter:
    async def generate(self, profile, context):
        await asyncio.sleep(0.2)
        return {"type":"video","model":"sora","status":"queued","prompt":context.get("prompt","")}
