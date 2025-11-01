import asyncio
class OpenArtAdapter:
    async def generate(self, profile, context):
        await asyncio.sleep(0.2)
        return {"type":"image","model":"openart","url":"mock://image","prompt":context.get("prompt","")}
