import React from "react";
export function Inspector({ selectedNode, onUpdate }: any) {
  if (!selectedNode) return <div className="p-2 border rounded">Select a node</div>;
  const cfg = selectedNode.data?.config || {};
  return (
    <div className="p-2 border rounded">
      <h3 className="font-semibold">{selectedNode.data?.label}</h3>
      <label className="block">Label<input className="border p-1 w-full" defaultValue={selectedNode.data?.label} onChange={e => onUpdate({ label: e.target.value })} /></label>
      <label className="block">Endpoint<input className="border p-1 w-full" defaultValue={cfg.endpoint} onChange={e => onUpdate({ config: { ...cfg, endpoint: e.target.value } })} /></label>
    </div>
  );
}
