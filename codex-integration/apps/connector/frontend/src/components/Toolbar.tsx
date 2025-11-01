import React from "react";
import { saveFlow, publishFlow, runFlow } from "../services/flows";

export function Toolbar({ flowId, payload }: { flowId: string; payload: any }) {
  return (
    <div className="flex gap-2">
      <button onClick={async () => { await saveFlow(payload); }} className="px-3 py-2 border rounded">Save</button>
      <button onClick={async () => { await publishFlow(flowId); }} className="px-3 py-2 border rounded">Seal</button>
      <button onClick={async () => { await runFlow(flowId, { type: "capsule_published" }, true); }} className="px-3 py-2 border rounded">Dry Run</button>
    </div>
  );
}
