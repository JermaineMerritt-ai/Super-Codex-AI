import uuid
from apps.orchestration.guards.policy import apply_policies
from apps.orchestration.guards.privacy import redact
from apps.orchestration.workflows.loader import load_workflow

async def run_workflow(event: dict) -> dict:
	wf = load_workflow(event["type"])
	ctx = {"state": "pending", "workflow_id": str(uuid.uuid4()), "history": []}

	event["data"] = redact(event["data"])
	apply_policies(event, wf)

	for step in wf.get("steps", []):
		ctx["history"].append(step["name"])
		# Execute side-effects here (e.g., call payment API; reserve inventory)
		# Placeholder:
		if step.get("effect") == "notify":
			pass
	ctx["state"] = "settled"
	return ctx
