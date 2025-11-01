import React, { useState } from "react";
import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";
import { Toolbar } from "./components/Toolbar";
import { Inspector } from "./components/Inspector";
import UploadWidget from "./components/UploadWidget";

const initialNodes = [
  { id: "1", type: "input", data: { label: "Trigger: Capsule Published", config: { event: "capsule_published" } }, position: { x: 0, y: 0 } },
  { id: "2", data: { label: "Action: Notify Council", config: { endpoint: "/notify" } }, position: { x: 250, y: 100 } },
  { id: "3", data: { label: "Replay: Archive Flow", config: { storage: "Codex Archive" } }, position: { x: 500, y: 200 } }
];

const initialEdges = [
  { id: "e1-2", source: "1", target: "2" },
  { id: "e2-3", source: "2", target: "3" }
];

export default function App() {
  const [nodes, setNodes] = useState<any[]>(initialNodes);
  const [edges, setEdges] = useState<any[]>(initialEdges);
  const [selected, setSelected] = useState<any>(null);

  const flowPayload = {
    capsule: { id: "capsule_001", version: 1, title: "Publish → Notify → Archive", sector: "governance", owner: "Custodian" },
    nodes: nodes.map(n => ({ id: n.id, type: (n.type === "input" ? "trigger" : n.type || "action"), data: n.data })),
    edges: edges.map(e => ({ source: e.source, target: e.target }))
  };

  const updateSelected = (patch: any) => {
    setNodes(nodes.map(n => n.id === selected.id ? { ...n, data: { ...n.data, ...patch } } : n));
  };

  return (
    <div className="grid grid-cols-4 gap-4 p-4">
      <div className="col-span-3">
        <Toolbar flowId="capsule_001" payload={flowPayload} />
        <UploadWidget />
        <div style={{ height: "70vh" }}>
          <ReactFlow nodes={nodes} edges={edges} onNodesChange={setNodes} onEdgesChange={setEdges} onNodeClick={(_, n) => setSelected(n)}>
            <Controls />
            <Background />
          </ReactFlow>
        </div>
      </div>
      <Inspector selectedNode={selected} onUpdate={updateSelected} />
    </div>
  );
}
