export async function saveFlow(payload: any) {
  const res = await fetch("/flows", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
  return res.json();
}

export async function publishFlow(id: string) {
  const res = await fetch(`/flows/${id}/publish`, { method: "POST" });
  return res.json();
}

export async function runFlow(flow_id: string, event: any, dry_run = true) {
  const res = await fetch(`/runs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ flow_id, event, dry_run })
  });
  return res.json();
}
