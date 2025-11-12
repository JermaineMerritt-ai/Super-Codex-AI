from fastapi import APIRouter, Request, Header, HTTPException
from ..services.token_service import issue_token
import hmac, hashlib, json, os, yaml


router = APIRouter()
WEBHOOK_SECRET = os.getenv("WOO_WEBHOOK_SECRET")

# Load role map from YAML
def load_role_map(path=os.path.join(os.path.dirname(__file__), "sku_role_map.yaml")):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("mappings", {})

ROLE_MAP = load_role_map()

@router.post("/codex/webhook/woocommerce")
async def woocommerce_order_webhook(
    request: Request,
    x_wc_webhook_signature: str = Header(None)
):
    body = await request.body()

    # Verify signature
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_wc_webhook_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = json.loads(body)

    # Extract order info
    order_id = payload.get("id")
    customer_email = payload.get("billing", {}).get("email")
    total = payload.get("total")
    line_items = payload.get("line_items", [])

    assigned_roles = []
    for item in line_items:
        sku = item.get("sku")
        if sku in ROLE_MAP:
            assigned_roles.append(ROLE_MAP[sku])

    issued_tokens = []
    for role in assigned_roles:
        token = issue_token(customer_email, role, order_id)
        issued_tokens.append(token.dict())

    return {
        "status": "processed",
        "order_id": order_id,
        "tokens": issued_tokens
    }
