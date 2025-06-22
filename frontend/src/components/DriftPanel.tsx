import React, { useEffect, useState } from "react";

interface DriftedGlyph {
  name: string;
  categories: string[];
  drift_score: number;
  cluster: number;
}

export const DriftPanel: React.FC = () => {
  const [drifted, setDrifted] = useState<DriftedGlyph[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showGene, setShowGene] = useState(true);

  useEffect(() => {
    fetch("/api/drift/status?sigil=default")
      .then((res) => res.json())
      .then((data) => {
        setDrifted(data.drifted || []);
        setTotal(data.total || 0);
        setLoading(false);
      });
  }, []);

  const getColor = (categories: string[]) => {
    if (categories.includes("Rapid Drift")) return "#e57373";
    if (categories.includes("Drifting")) return "#ffd54f";
    if (categories.includes("Unlinked")) return "#64b5f6";
    if (categories.includes("Stale")) return "#bdbdbd";
    return "#fff";
  };

  return (
    <div style={{ padding: 16, background: "#222", color: "#fff", borderRadius: 8 }}>
      <h2>Symbolic Drift Monitor</h2>
      <div style={{ marginBottom: 8 }}>
        <label>
          <input type="checkbox" checked={showGene} onChange={() => setShowGene((v) => !v)} /> Show Gene Overlay
        </label>
      </div>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <>
          <div style={{ marginBottom: 8 }}>
            <b>❗ Drifted Glyphs:</b> {drifted.length} / {total}
          </div>
          <table style={{ width: "100%", background: "#333", borderRadius: 4 }}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Categories</th>
                <th>Drift Score</th>
                <th>Cluster</th>
              </tr>
            </thead>
            <tbody>
              {drifted.map((g) => (
                <tr key={g.name} style={{ background: getColor(g.categories) }}>
                  <td>{g.name}</td>
                  <td>{g.categories.join(", ")}</td>
                  <td>{g.drift_score.toFixed(2)}</td>
                  <td>{g.cluster}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div style={{ marginTop: 12 }}>
            <b>Legend:</b>
            <span style={{ color: "#e57373", marginLeft: 8 }}>■ Rapid Drift</span>
            <span style={{ color: "#ffd54f", marginLeft: 8 }}>■ Drifting</span>
            <span style={{ color: "#64b5f6", marginLeft: 8 }}>■ Unlinked</span>
            <span style={{ color: "#bdbdbd", marginLeft: 8 }}>■ Stale</span>
          </div>
          {showGene && (
            <div style={{ marginTop: 16, background: "#444", padding: 8, borderRadius: 4 }}>
              <b>Gene Suggestion:</b> {drifted.length > 0 ? "Consider merging, evolving, or compressing drifted glyphs." : "No drift detected."}
            </div>
          )}
        </>
      )}
    </div>
  );
}; 