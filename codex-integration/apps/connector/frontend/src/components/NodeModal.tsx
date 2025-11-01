import React from "react";

export function NodeModal({ node, onClose, onSave }: any) {
  const [label, setLabel] = React.useState(node.data?.label || "");
  const [endpoint, setEndpoint] = React.useState(node.data?.config?.endpoint || "");
  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center">
      <div className="bg-white p-4 rounded w-[420px]">
        <h3 className="font-semibold">Edit Node</h3>
        <label className="block mt-2">Label<input className="border p-1 w-full" value={label} onChange={e=>setLabel(e.target.value)} /></label>
        <label className="block mt-2">Endpoint<input className="border p-1 w-full" value={endpoint} onChange={e=>setEndpoint(e.target.value)} /></label>
        <div className="mt-4 flex gap-2">
          <button className="px-3 py-2 border rounded" onClick={onClose}>Cancel</button>
          <button className="px-3 py-2 border rounded" onClick={() => onSave({ label, config: { endpoint } })}>Save</button>
        </div>
      </div>
    </div>
  );
}
