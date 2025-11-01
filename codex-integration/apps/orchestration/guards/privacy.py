from apps.connector.utils.config import get_policies

def redact(data: dict) -> dict:
	policies = get_policies()
	if policies["privacy"]["pii_minimization"]:
		for f in policies["privacy"]["redact_fields"]:
			if f in data:
				data[f] = "***redacted***"
	return data
