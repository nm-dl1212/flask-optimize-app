import React, { useState } from "react";
import { optimize } from "../api/services";

const Optimize: React.FC = () => {
  const [initialX1, setInitialX1] = useState<number>(0);
  const [initialX2, setInitialX2] = useState<number>(0);
  const [nTrials, setNTrials] = useState<number>(10);
  const [result, setResult] = useState<any>(null);

  const handleOptimize = async () => {
    const response = await optimize(initialX1, initialX2, nTrials);
    setResult(response.data);
  };

  return (
    <div>
      <h2>Optimization</h2>
      <input
        type="number"
        placeholder="Initial x1"
        onChange={(e) => setInitialX1(Number(e.target.value))}
      />
      <input
        type="number"
        placeholder="Initial x2"
        onChange={(e) => setInitialX2(Number(e.target.value))}
      />
      <input
        type="number"
        placeholder="Number of Trials"
        onChange={(e) => setNTrials(Number(e.target.value))}
      />
      <button onClick={handleOptimize}>Optimize</button>
      {result && (
        <div>
          <p>Min Result: {result.min_result}</p>
          <p>All Results: {JSON.stringify(result.results)}</p>
        </div>
      )}
    </div>
  );
};

export default Optimize;
