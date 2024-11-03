import React, { useState } from "react";
import { dummyCalculation } from "../api/services";

const Dummy: React.FC = () => {
  const [x1, setX1] = useState<number>(0);
  const [x2, setX2] = useState<number>(0);
  const [result, setResult] = useState<number | null>(null);

  const handleCalculate = async () => {
    const response = await dummyCalculation(x1, x2);
    setResult(response.data.y);
  };

  return (
    <div>
      <h2>Dummy Calculation</h2>
      <input
        type="number"
        placeholder="x1"
        onChange={(e) => setX1(Number(e.target.value))}
      />
      <input
        type="number"
        placeholder="x2"
        onChange={(e) => setX2(Number(e.target.value))}
      />
      <button onClick={handleCalculate}>Calculate</button>
      {result !== null && <p>Result: {result}</p>}
    </div>
  );
};

export default Dummy;
