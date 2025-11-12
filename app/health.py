# app/health.py
from fastapi import APIRouter
import os, shutil
import httpx

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/live")
def live(): return {"status":"live"}

@router.get("/ready")
def ready():
    total, used, free = shutil.disk_usage("/")
    return {"status":"ready", "disk_free_bytes": free}

@router.get("/deps")
def deps():
    return {"fastapi":"ok","axiom_flame":"ok"}  # extend with real checks

@router.get("/axiom")
async def axiom():
  base = os.getenv("AXIOM_BASE","http://localhost:5010")
  try:
    async with httpx.AsyncClient(timeout=5) as c:
      r = await c.get(f"{base}/health")
    return {"axiom":"ok","status_code":r.status_code,"response":r.json()}
  except Exception as e:
    return {"axiom":"down","error":str(e)}