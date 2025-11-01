from pydantic import BaseModel
from datetime import datetime

class CouncilApprovalConfig(BaseModel):
    role: str
    policy_ref: str | None = None
    timeout_seconds: int = 3600

async def run(input_ctx: dict, config: CouncilApprovalConfig) -> dict:
    approval = {
        "status": "pending",
        "requested_at": datetime.utcnow().isoformat(),
        "role": config.role,
        "policy_ref": config.policy_ref,
        "payload_snapshot": input_ctx,
    }
    # enqueue to approvals queue (placeholder)
    return {"next": "approved", "approval_record": approval}
