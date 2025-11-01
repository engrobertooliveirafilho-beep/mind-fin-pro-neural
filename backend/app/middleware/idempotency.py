from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import Response
# Simulação mínima de idempotência para rodar ambiente dev
class IdempotencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # apenas proxy transparente no modo DEV
        response: Response = await call_next(request)
        response.headers["X-Idempotency"] = "ok-dev"
        return response
