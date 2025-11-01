import yaml, os

def load_workflow(event_type: str) -> dict:
    base = os.path.dirname(__file__)
    path = os.path.join(base, f"{event_type.replace('.', '_')}.yaml")
    if not os.path.exists(path):
        # Minimal default workflow
        return {"steps": [{"name": "validate"}, {"name": "archive"}]}
    with open(path) as f:
        return yaml.safe_load(f)
