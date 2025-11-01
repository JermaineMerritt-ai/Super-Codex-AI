import yaml, os, functools

@functools.lru_cache
def get_settings() -> dict:
	with open(os.path.join("config", "settings.yaml")) as f:
		return yaml.safe_load(f)

@functools.lru_cache
def get_policies() -> dict:
	with open(os.path.join("config", "policies.yaml")) as f:
		return yaml.safe_load(f)
