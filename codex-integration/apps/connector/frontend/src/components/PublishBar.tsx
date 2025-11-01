import React from "react";
import { saveFlow, publishFlow, runFlow } from "../services/flows";

export function PublishBar({ flowId, payload }: { flowId: string; payload: any }) {
  return (
    <div className="flex gap-2">
      <button className="px-3 py-2 border rounded" onClick={() => saveFlow(payload)}>Save</button>
      <button className="px-3 py-2 border rounded" onClick={() => publishFlow(flowId)}>Seal</button>
      <button className="px-3 py-2 border rounded" onClick={() => runFlow(flowId, { type: "capsule_published" }, true)}>Dry Run</button>
    </div>
  );
}
