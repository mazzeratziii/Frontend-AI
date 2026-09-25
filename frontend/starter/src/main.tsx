import React from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function StarterBoundary() {
  return (
    <main>
      <h1>Implementation workspace</h1>
      <p>The coding agent must implement the task from the supplied condition artifacts.</p>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<StarterBoundary />);