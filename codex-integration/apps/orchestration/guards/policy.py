from apps.connector.utils.config import get_policies

def apply_policies(event: dict, workflow: dict):
	policies = get_policies()
	if event["type"] in policies["approvals"]["council_required_events"]:
		workflow.setdefault("approvals", {})["mode"] = "council_required"
