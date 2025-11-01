from fastapi import APIRouter, Header, HTTPException
import psutil, time
from prometheus_client import CollectorRegistry, Gauge, generate_latest

router = APIRouter()

@router.get("/")
async def public_metrics(authorization: str | None = Header(None)):
    # ProteÃ§Ã£o simples por token
    if authorization != "Bearer METRICS_TOKEN":
        raise HTTPException(401, "NÃ£o autorizado")
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "ts": int(time.time()),
    }

@router.get("/prom")
async def prom_metrics(authorization: str | None = Header(None)):
    if authorization != "Bearer METRICS_TOKEN":
        raise HTTPException(401, "NÃ£o autorizado")
    reg = CollectorRegistry()
    g_cpu = Gauge("cpu_percent","CPU %", registry=reg)
    g_ram = Gauge("ram_percent","RAM %", registry=reg)
    g_cpu.set(psutil.cpu_percent())
    g_ram.set(psutil.virtual_memory().percent)
    return generate_latest(reg)
