import { useState } from "react";

export default function Refiner() {
  const [script, setScript] = useState("");
  const [comments, setComments] = useState("");
  const [rating, setRating] = useState(3);
  const [result, setResult] = useState("");

  async function handleRefine() {
    const res = await fetch("/api/refine-script", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ script, feedback: { rating, comments } })
    });
    const data = await res.json();
    setResult(data.refined_script);
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">🔁 Script Refiner</h1>
      <textarea rows={6} value={script} onChange={e => setScript(e.target.value)} className="w-full p-2 border" placeholder="Paste your script here..." />
      <textarea rows={2} value={comments} onChange={e => setComments(e.target.value)} className="w-full p-2 border mt-2" placeholder="What needs improvement?" />
      <input type="range" min={1} max={5} value={rating} onChange={e => setRating(Number(e.target.value))} className="w-full mt-2" />
      <button onClick={handleRefine} className="mt-4 bg-blue-600 text-white px-4 py-2 rounded">Refine</button>
      {result && (
        <div className="mt-4 p-4 border bg-gray-100">
          <h2 className="font-bold">Refined Script:</h2>
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
} 