# Simple in-memory flow store for orchestration

_flows = {}

def save_flow(flow: dict):
    fid = flow["capsule"]["id"]
    _flows[fid] = flow
    return fid

def get_flow(fid: str):
    return _flows.get(fid)

# Optionally, preload with example flows or add more management functions as needed
