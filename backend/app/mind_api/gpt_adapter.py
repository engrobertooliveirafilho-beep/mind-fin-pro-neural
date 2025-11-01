import asyncio
class GPTAdapter:
    async def generate(self, profile, context):
        await asyncio.sleep(0.2)
        return {"type":"text","model":"gpt","content":f"Coach para {profile.get('name','usuÃ¡rio')}: {context.get('prompt','')}"}
