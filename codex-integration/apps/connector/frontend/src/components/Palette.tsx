import React, { useEffect, useState } from "react";

export function Palette() {
  const [nodeTypes, setNodeTypes] = useState<any[]>([]);
  useEffect(() => {
    fetch("/flows/nodes").then(r => r.json()).then(setNodeTypes);
  }, []);
  return (
    <div className="grid grid-cols-2 gap-2">
      {nodeTypes.map((n) => (
        <button key={n.type} className="border p-2 rounded">{n.type}</button>
      ))}
    </div>
  );
}
