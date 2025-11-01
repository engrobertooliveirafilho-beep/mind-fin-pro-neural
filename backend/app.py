import os
import json
import base64
import logging
from datetime import datetime
from hashlib import sha256

from fastapi import FastAPI, WebSocket
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# -----------------------------------------------------------------------------
# Logger
# -----------------------------------------------------------------------------
root_logger = logging.getLogger("mind")
root_logger.setLevel(logging.INFO)
if not root_logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(h)

# -----------------------------------------------------------------------------
# Métricas
# -----------------------------------------------------------------------------
REQS = Counter("mind_requests_total", "Total requests", ["route"])
LAT = Histogram("mind_request_latency_seconds", "Latency (s)", ["route"])

# -----------------------------------------------------------------------------
# Criptografia AES-256 (chave 32 bytes, IV 16 bytes)
# -----------------------------------------------------------------------------
KEY = sha256(os.getenv("LOG_AES_KEY", "mindfin_dev_key").encode("utf-8")).digest()
IV  = sha256(os.getenv("LOG_AES_IV",  "mindfin_dev_iv").encode("utf-8")).digest()[:16]

def aes256_encrypt(s: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded = padder.update(s.encode("utf-8")) + padder.finalize()
    enc = Cipher(algorithms.AES(KEY), modes.CBC(IV)).encryptor()
    ct = enc.update(padded) + enc.finalize()
    return base64.b64encode(ct).decode("utf-8")

def aes256_decrypt(token_b64: str) -> str:
    ct = base64.b64decode(token_b64)
    dec = Cipher(algorithms.AES(KEY), modes.CBC(IV)).decryptor()
    padded = dec.update(ct) + dec.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded) + unpadder.finalize()
    return data.decode("utf-8")

# -----------------------------------------------------------------------------
# FastAPI
# -----------------------------------------------------------------------------
app = FastAPI(title="MIND FIN PRO API", version="0.2.0")

class SimInput(BaseModel):
    income: float
    expenses: float
    debt: float
    risk_profile: str | None = None
    mood: str | None = None

@app.get("/debug/crypto")
def debug_crypto():
    return JSONResponse({
        "aes_key_len": len(KEY),
        "aes_iv_len": len(IV),
        "otel_enabled": False,
        "otel_endpoint": None
    })

@app.get("/admin/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/simulate/performance")
def simulate(data: SimInput):
    REQS.labels(route="/simulate/performance").inc()
    with LAT.labels(route="/simulate/performance").time():
        score = max(
            0.0,
            min(
                100.0,
                (data.income - data.expenses) / max(1, data.income) * 100
                - (data.debt / max(1, data.income)) * 10,
            ),
        )
        plan = {
            "score": round(score, 2),
            "actions": [
                "Reduzir 10% de gastos variáveis",
                "Quitar dívidas >2% a.m. primeiro",
                "Automatizar aporte 5% da renda em reserva",
            ],
            "narrative": "Fluxo positivo moderado. Priorize amortização e crie colchão.",
        }

    root_logger.info(json.dumps({
        "event": "simulate_performance",
        "score": plan["score"],
        "user_encrypted": aes256_encrypt(f"{data.risk_profile or ''}|{data.mood or ''}"),
        "ts": datetime.utcnow().isoformat(),
    }, ensure_ascii=False))

    return JSONResponse(plan)

@app.websocket("/ws/ai")
async def ws_ai(ws: WebSocket):
    await ws.accept()
    for chunk in (
        "Conectado. IA carregando...",
        "Analisando dados...",
        "Detectando padrões...",
        "Plano pronto.",
    ):
        await ws.send_text(chunk)
    await ws.close()

# -----------------------------------------------------------------------------
# Scheduler
# -----------------------------------------------------------------------------
scheduler = AsyncIOScheduler()

def task_learning():
    root_logger.info(json.dumps(
        {"event": "bg_learning_tick", "ts": datetime.utcnow().isoformat()},
        ensure_ascii=False
    ))

scheduler.add_job(task_learning, "interval", seconds=30)

@app.on_event("startup")
async def on_start():
    root_logger.info(json.dumps({"aes_key_len": len(KEY), "aes_iv_len": len(IV)}))
    scheduler.start()
