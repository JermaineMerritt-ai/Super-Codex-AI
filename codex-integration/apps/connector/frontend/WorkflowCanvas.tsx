import React from "react";
import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";

export function WorkflowCanvas({ nodes, edges, onNodesChange, onEdgesChange, onConnect }) {
  return (
    <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect}>
      <Controls />
      <Background variant="dots" gap={16} size={1} />
    </ReactFlow>
  );
}
