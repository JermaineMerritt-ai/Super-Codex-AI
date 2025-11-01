import React from "react";
import { saveFlow } from "../services/flows";

export function RemixButton({ original, mutate }: { original: any; mutate: (c:any)=>any }) {
  const remix = async () => {
    const cloned = JSON.parse(JSON.stringify(original));
    cloned.capsule.id = `${cloned.capsule.id}_remix`;
    cloned.capsule.version = (cloned.capsule.version || 1) + 1;
    const remixed = mutate(cloned);
    await saveFlow(remixed);
  };
  return <button className="px-3 py-2 border rounded" onClick={remix}>Remix Capsule</button>;
}
