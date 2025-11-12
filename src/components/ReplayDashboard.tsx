// src/components/ReplayDashboard.tsx
import { useEffect, useState } from "react";

export default function ReplayDashboard() {
  const [events, setEvents] = useState<any[]>([]);
  useEffect(() => {
    const ws = new WebSocket("wss://your-domain/ws/ceremony");
    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data);
      setEvents((prev) => [data, ...prev].slice(0, 100));
    };
    return () => ws.close();
  }, []);
  return (
    <div>
      <h3>Ceremonial Updates</h3>
      <ul>{events.map((e, i) => <li key={i}>{JSON.stringify(e)}</li>)}</ul>
    </div>
  );
}