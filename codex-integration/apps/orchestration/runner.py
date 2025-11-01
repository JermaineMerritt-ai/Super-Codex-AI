
from typing import Dict, List, Any
import uuid

def build_adjacency(edges: List[Dict[str, Any]]):
    adj = {}
    for e in edges:
        adj.setdefault(e["source"], []).append(e)
    return adj


def eval_expr(expr: str, ctx: dict) -> bool:
    # Safe mini-evaluator: supports "context.key == 'value'" and booleans
    if expr.lower() in ("true", "1"): return True
    if expr.lower() in ("false", "0", ""): return False
    try:
        left, op, right = expr.split(" ", 2)
        # Resolve "context.foo"
        if left.startswith("context."):
            key = left.split(".", 1)[1]
            val = ctx.get(key)
            if op == "==": return str(val) == right.strip("'\"")
            if op == "!=": return str(val) != right.strip("'\"")
    except Exception:
        return False
    return False

async def run_flow(flow: Dict[str, Any], event: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
    nodes = {n["id"]: n for n in flow["nodes"]}
    adj = build_adjacency(flow["edges"])
    starts = [nid for nid, n in nodes.items() if n["type"] == "trigger"]

    ctx = {
        "run_id": str(uuid.uuid4()),
        "event": event,
        "history": [],
        "flags": {},          # set by condition nodes
        "recognition": [],
        "contributors": []
    }

    queue = starts[:]
    visited = set()

    while queue:
        nid = queue.pop(0)
        if nid in visited: 
            continue
        node = nodes[nid]
        await handle_node(node, ctx, dry_run)
        visited.add(nid)

        for edge in adj.get(nid, []):
            cond = edge.get("condition")
            if cond and not eval_expr(cond, ctx):
                continue
            queue.append(edge["target"])

    ctx["status"] = "dry_run" if dry_run else "executed"
    return ctx

async def handle_node(node: Dict[str, Any], ctx: Dict[str, Any], dry_run: bool):
    t = node["type"]
    data = node.get("data", {})
    label = data.get("label", t)
    ctx["history"].append({"node": node["id"], "type": t, "label": label})

    if t == "condition":
        # Example: set flag from role check
        expr = data.get("expr", "")
        ctx["flags"]["condition_met"] = eval_expr(expr, ctx)
    elif t == "action" and not dry_run:
        # Example action: notify council via webhook
        if data.get("endpoint") == "/notify":
            # perform HTTP call (placeholder)
            pass
    elif t == "recognition":
        ctx["recognition"].append({
            "agent": data.get("agent", "unknown"),
            "role": data.get("role", "contributor"),
            "message": data.get("message", "")
        })
        ctx["contributors"].append(data.get("agent"))
    elif t == "replay":
        ctx["replay"] = {"storage": data.get("storage", "Codex Replay Deck"), "mode": "narrated"}
