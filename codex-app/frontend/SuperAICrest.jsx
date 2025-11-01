import React, { useState, useEffect } from "react";
import "./SuperAICrest.css";

// SVG Crest (can be replaced with animated SVG if desired)
const CrestSVG = ({ isActive }) => (
  <svg
    className={isActive ? "superai-crest active" : "superai-crest"}
    xmlns="http://www.w3.org/2000/svg"
    width="80"
    height="80"
    viewBox="0 0 80 80"
  >
    <rect width="100%" height="100%" fill="black" rx="16" ry="16" />
    <text
      x="50%"
      y="50%"
      dominantBaseline="middle"
      textAnchor="middle"
      fontFamily="serif"
      fontSize="32"
      fill="gold"
    >
      ⚜️
    </text>
  </svg>
);

// Super Action AI Avatar component
const SuperAICrest = ({ isActive, cycle, custodian }) => (
  <div className="superai-avatar-container">
    <CrestSVG isActive={isActive} />
    <div className="superai-avatar-meta">
      <div className="superai-avatar-label">Jermaine Super Action AI</div>
      <div className="superai-avatar-cycle">Cycle: {cycle}</div>
      <div className="superai-avatar-custodian">Custodian: {custodian}</div>
    </div>
  </div>
);

export default SuperAICrest;
