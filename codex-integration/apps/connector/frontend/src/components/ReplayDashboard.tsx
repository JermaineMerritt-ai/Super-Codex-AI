import React, { useEffect, useState } from "react";

export function ReplayDashboard() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => { fetch("/replay").then(r=>r.json()).then(setItems); }, []);
  return (
    <div className="p-2 border rounded">
      <h3 className="font-semibold mb-2">Replay Deck</h3>
      <table className="w-full text-sm">
        <thead><tr><th>ID</th><th>Flow</th><th>Status</th><th>Attempts</th><th>Action</th></tr></thead>
        <tbody>
          {items.map(i => (
            <tr key={i.id}>
              <td>{i.id}</td><td>{i.flow_id}</td><td>{i.status}</td><td>{i.attempts}</td>
              <td><button className="px-2 py-1 border rounded" onClick={() => fetch(`/replay/${i.id}/redrive`, { method: "POST" })}>Re-drive</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
