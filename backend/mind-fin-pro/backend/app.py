# app.py — MIND FIN PRO (versão limpa, SEM OpenTelemetry)
# Substitua integralmente seu app.py por este arquivo.

import base64
import json
import logging
import os
import time
from datetime import datetime
from typing import Optional

# Scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
# Crypto (AES-256-CBC demo)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, Response
# Prometheus
from prometheus_client import (CONTENT_TYPE_LATEST, Counter, Histogram,
                               generate_latest)
from pydantic import BaseModel

# ------------------------------------------------------------------------------
# Logging básico
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("mind")


# ------------------------------------------------------------------------------
# Prometheus métrica básica
# ------------------------------------------------------------------------------
REQS = Counter("mind_requests_total", "Total requests", ["route"])
LAT = Histogram("mind_request_latency_seconds", "Latency in seconds", ["route"])


# ------------------------------------------------------------------------------
# AES-256 helpers (DEMO)
# ------------------------------------------------------------------------------
KEY = (os.getenv("LOG_AES_KEY") or "this_is_32_bytes_key_for_demo_!").encode()[:32]
IV = (os.getenv("LOG_AES_IV") or "this_is_16_bytes!").encode()[:16]


def aes256_encrypt(s: str) -> str:
    padder = padding.PKCS7(128).padder()
    pt = padder.update(s.encode("utf-8")) + padder.finalize()
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(pt) + encryptor.finalize()
    return base64.b64encode(ct).decode("utf-8")


# ------------------------------------------------------------------------------
# FastAPI
# ------------------------------------------------------------------------------
app = FastAPI(title="MIND FIN PRO API")

# CORS para o UI local (React / Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------------------------
# Middleware p/ métricas por rota
# ------------------------------------------------------------------------------
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    route = request.url.path
    start = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    finally:
        LAT.labels(route=route).observe(time.perf_counter() - start)
        REQS.labels(route=route).inc()


# ------------------------------------------------------------------------------
# Modelos
# ------------------------------------------------------------------------------
class SimInput(BaseModel):
    income: float
    expenses: float
    debt: float
    risk_profile: Optional[str] = None
    mood: Optional[str] = None


# ------------------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------------------
@app.get("/admin/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/debug/crypto")
def debug_crypto(echo: str = "ping"):
    enc = aes256_encrypt(echo)
    return JSONResponse({"ok": True, "echo": echo, "encrypted": enc})


@app.post("/simulate/performance")
def simulate(data: SimInput):
    # cálculo de score simples e determinístico
    score = max(
        0.0,
        min(
            100.0,
            (data.income - data.expenses) / max(1.0, data.income) * 100.0
            - (data.debt / max(1.0, data.income)) * 10.0,
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

    # log seguro com user info cifrada (DEMO)
    log.info(
        json.dumps(
            {
                "event": "simulate_performance",
                "user_encrypted": aes256_encrypt(f"{data.risk_profile}|{data.mood}"),
                "score": plan["score"],
            },
            ensure_ascii=False,
        )
    )
    return JSONResponse(plan)


@app.websocket("/ws/ai")
async def ws_ai(ws: WebSocket):
    await ws.accept()
    try:
        # handshake curto
        await ws.send_text("Conectado. Envie uma mensagem.")
        msg = await ws.receive_text()
        await ws.send_text(f"echo:{msg}")
    finally:
        await ws.close()


# ------------------------------------------------------------------------------
# Scheduler
# ------------------------------------------------------------------------------
scheduler = AsyncIOScheduler()


def task_learning():
    log.info(
        json.dumps({"event": "bg_learning_tick", "ts": datetime.utcnow().isoformat()})
    )


scheduler.add_job(task_learning, "interval", seconds=30)


@app.on_event("startup")
async def on_start():
    scheduler.start()
    log.info("Scheduler iniciado.")


@app.on_event("shutdown")
async def on_shutdown():
    try:
        scheduler.shutdown(wait=False)
    finally:
        log.info("Scheduler finalizado.")
