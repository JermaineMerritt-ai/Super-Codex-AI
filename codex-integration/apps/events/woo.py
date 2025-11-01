from fastapi import APIRouter, Request, HTTPException

router = APIRouter(prefix="/api/events", tags=["events"])

@router.post("/woo")
async def woo_event(req: Request):
    secret = req.headers.get("X-WC-Webhook-Signature")
    if not secret or secret != "YOUR_SHARED_SECRET":
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await req.json()
    # Map to Capsule run
    # flow_id = "woo_capsule_001"
    # await run_flow(get_flow(flow_id), {"type": "product_purchased", "payload": payload}, dry_run=False)
    return {"status": "accepted"}
