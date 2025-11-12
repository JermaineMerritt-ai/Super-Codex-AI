// src/lib/ws.ts
export function connectCeremonyWS(onEvent: (e:any)=>void) {
  let retry = 1000;
  const open = () => {
    const ws = new WebSocket(`ws://localhost:8010/ws/ceremony`);
    ws.onmessage = (m) => onEvent(JSON.parse(m.data));
    ws.onclose = () => setTimeout(open, retry = Math.min(retry * 2, 15000));
  };
  open();
}