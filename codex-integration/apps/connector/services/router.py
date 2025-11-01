import asyncio
from apps.connector.utils.config import get_settings
from apps.orchestration.engine import run_workflow

async def route_event(canon_event: dict) -> dict:
	settings = get_settings()
	# Attach correlation id
	canon_event.setdefault("meta", {})["correlation_id"] = canon_event["data"].get("order_id")
	# Send to orchestration
	result = await run_workflow(canon_event)
	# Optionally enqueue to event store / Redis stream
	await asyncio.sleep(0)  # placeholder
	return {"id": result.get("workflow_id")}
