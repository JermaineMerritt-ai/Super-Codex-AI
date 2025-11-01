import React from "react";
import ReactFlow, { Controls, Background, addEdge, Connection } from "reactflow";
import "reactflow/dist/style.css";
import { useFlowStore } from "../store/useFlowStore";

export function Canvas() {
  const { nodes, edges, setNodes, setEdges } = useFlowStore();
  const onConnect = (conn: Connection) => setEdges(addEdge(conn, edges));
  return (
    <div style={{ height: "80vh" }}>
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={setNodes} onEdgesChange={setEdges} onConnect={onConnect}>
        <Controls />
        <Background variant="dots" gap={16} size={1} />
      </ReactFlow>
    </div>
  );
}
